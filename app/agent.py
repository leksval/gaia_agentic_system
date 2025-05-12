# app/agent.py
import json
import os
import logging
import traceback
import re
from typing import List, Optional, Dict, Any, Tuple
from uuid import uuid4

from pydantic import BaseModel, Field

# Import LangChain components
from langchain_core.language_models import BaseLanguageModel
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, BaseMessage
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain.chains.llm import LLMChain
from langchain_openai import ChatOpenAI

# Import LangGraph components
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

# Import LiteLLM for model provider abstraction
import litellm

# Schemas and config imports
from .schemas import GaiaAnswer
from .config import settings
from .tools import TOOLS, web_search_tool, code_execution_tool

# Define MAX_AGENT_ITERATIONS constant
MAX_AGENT_ITERATIONS = settings.max_agent_iterations

# Define AgentState class for LangGraph
class AgentState(BaseModel):
    """State object for the LangGraph agent."""
    messages: List[BaseMessage] = Field(default_factory=list)
    current_gaia_question: Optional[str] = None
    iteration: int = 0
    intermediate_steps_log: List[Dict[str, Any]] = Field(default_factory=list)

# --- Basic Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_llm():
    """Initialize and return the LLM based on configuration."""
    provider = settings.llm_provider.lower().strip('"\'')

    if provider == "openrouter":
        logger.info(f"Configuring LLM for OpenRouter.")
        if not settings.openrouter_api_key:
            logger.critical("LLM_PROVIDER is 'openrouter' but OPENROUTER_API_KEY is not set.")
            raise ValueError("OPENROUTER_API_KEY must be set for OpenRouter provider.")

        # Configure litellm for OpenRouter
        os.environ["OPENAI_API_KEY"] = settings.openrouter_api_key
        os.environ["OPENAI_API_BASE"] = settings.openrouter_base_url
        
        model_name = settings.openrouter_model_name
        logger.info(f"Using OpenRouter model: {model_name}")

        # Use ChatOpenAI which is compatible with OpenRouter via LiteLLM
        llm = ChatOpenAI(
            model=model_name,
            openai_api_key=settings.openrouter_api_key,
            openai_api_base=settings.openrouter_base_url
        )

    elif provider == "ollama":
        logger.info(f"Configuring LLM for Ollama.")
        if not settings.ollama_base_url:
            logger.warning(f"OLLAMA_BASE_URL not explicitly set, using default: {settings.ollama_base_url}")

        # Use ChatOpenAI which is compatible with Ollama via LiteLLM
        llm = ChatOpenAI(
            model=settings.ollama_model_name,
            openai_api_key="ollama", # Placeholder, not actually used
            openai_api_base=settings.ollama_base_url
        )
        logger.info(f"Using Ollama model: {settings.ollama_model_name} via {settings.ollama_base_url}")
    else:
        logger.critical(f"Unsupported LLM_PROVIDER in config: '{provider}'. Choose 'openrouter' or 'ollama'.")
        raise ValueError(f"Unsupported LLM_PROVIDER: {provider}")

    return llm

def get_compiled_agent():
    """Creates and compiles a LangGraph agent."""
    logger.info("Creating LangGraph agent...")
    
    # Get the LLM
    llm = get_llm()
    
    # Create a state graph
    workflow = StateGraph(AgentState)
    
    # Define agent node
    def agent_node(state: AgentState) -> AgentState:
        """Core agent node that processes messages and decides next actions."""
        # Check iteration limit
        if state.iteration >= MAX_AGENT_ITERATIONS:
            logger.warning(f"Agent reached maximum iterations ({MAX_AGENT_ITERATIONS}). Stopping.")
            # Add a message indicating we've reached the limit
            state.messages.append(AIMessage(content=f"I've reached the maximum number of steps ({MAX_AGENT_ITERATIONS}). Here's my best answer based on what I've learned so far."))
            # Log this as a step
            state.intermediate_steps_log.append({
                "type": "iteration_limit_reached",
                "content": f"Reached maximum iterations: {MAX_AGENT_ITERATIONS}"
            })
            return state
        
        # Increment iteration counter
        state.iteration += 1
        logger.info(f"Agent iteration {state.iteration}/{MAX_AGENT_ITERATIONS}")
        
        # Get the last message to determine what to do next
        last_message = state.messages[-1] if state.messages else None
        
        try:
            # Process the current question
            question = state.current_gaia_question
            
            # Create a simple prompt template
            prompt = ChatPromptTemplate.from_messages([
                ("system", """You are a helpful AI assistant that can answer questions about a wide range of topics.
                You can search the web for information using the web_search tool, and you can execute code using the code_execution tool.
                Always provide your reasoning process and cite sources when possible."""),
                ("user", "{input}")
            ])
            
            # Create a simple chain
            chain = LLMChain(llm=llm, prompt=prompt)
            
            # Run the chain
            response = chain.run(input=question)
            
            # Try to extract structured components for GaiaAnswer
            try:
                # This is a simplified extraction approach
                answer = response
                reasoning = ""
                sources = []
                
                # Look for reasoning section
                reasoning_match = re.search(r"(?:Reasoning|Thought process|Rationale):\s*(.*?)(?:\n\n|\Z)", 
                                           response, re.DOTALL | re.IGNORECASE)
                if reasoning_match:
                    reasoning = reasoning_match.group(1).strip()
                    
                # Look for sources
                sources_match = re.findall(r"(?:Source|Reference):\s*(https?://\S+)", 
                                         response, re.IGNORECASE)
                if sources_match:
                    sources = sources_match
                    
                # Create a GaiaAnswer object
                gaia_answer = GaiaAnswer(
                    answer=answer,
                    reasoning=reasoning,
                    sources=sources
                )
                
                # Log the structured response
                state.intermediate_steps_log.append({
                    "type": "final_answer",
                    "content": {
                        "answer": gaia_answer.answer,
                        "reasoning": gaia_answer.reasoning,
                        "sources": gaia_answer.sources
                    }
                })
                
                # Add the agent's response to the messages
                ai_message = AIMessage(content=gaia_answer.answer)
                state.messages.append(ai_message)
                
            except Exception as parse_error:
                logger.error(f"Error parsing structured answer: {parse_error}", exc_info=True)
                # Fall back to using the raw output
                gaia_answer = GaiaAnswer(
                    answer=response,
                    reasoning="",
                    sources=[]
                )
                
                state.intermediate_steps_log.append({
                    "type": "final_answer",
                    "content": {
                        "answer": gaia_answer.answer,
                        "reasoning": "",
                        "sources": []
                    }
                })
                
                # Add the agent's response to the messages
                ai_message = AIMessage(content=response)
                state.messages.append(ai_message)
                
        except Exception as e:
            error_msg = f"Error in agent processing: {str(e)}"
            logger.error(error_msg, exc_info=True)
            
            # Add an error message
            state.messages.append(AIMessage(content=f"LLM Error: {error_msg}"))
            
            # Log the error
            state.intermediate_steps_log.append({
                "type": "error_message",
                "content": error_msg
            })
        
        return state
    
    # Add nodes to the graph
    workflow.add_node("agent", agent_node)
    
    # Define the starting point
    workflow.set_entry_point("agent")
    
    # Define end node
    def end_node(state: AgentState) -> AgentState:
        """End node that marks the completion of the agent's work."""
        logger.info("Agent workflow completed.")
        return state
    
    # Add end node to the graph
    workflow.add_node("end", end_node)
    
    # Add edges - simplified to just go from agent to end
    workflow.add_edge("agent", "end")
    
    # Compile the graph with memory checkpointer
    logger.info("Compiling LangGraph agent...")
    memory = MemorySaver()
    compiled_graph = workflow.compile(checkpointer=memory)
    logger.info("LangGraph agent compiled successfully.")
    
    return compiled_graph