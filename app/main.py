import os
import logging
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from uuid import uuid4
import traceback

from .schemas import QueryRequest, AgentResponse, StepDetail, GaiaAnswer # Import GaiaAnswer
from .agent import get_compiled_agent, AgentState, MAX_AGENT_ITERATIONS # Import from agent module
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, BaseMessage
from typing import List, Optional, Dict, Any

# --- Basic Logging Setup ---
# Consistent with agent.py, but could be more specific if needed
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI(
    title="GAIA Pathfinder Agent API (MVP v2)",
    description="An API for a LangGraph agent using OpenRouter LLMs, with enhanced logging and error reporting.",
    version="0.2.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

compiled_agent_graph = None

@app.on_event("startup")
async def startup_event():
    global compiled_agent_graph
    logger.info("FastAPI app startup: Initializing LangGraph agent...")
    try:
        compiled_agent_graph = get_compiled_agent()
        logger.info("LangGraph agent initialized successfully.")
    except Exception as e:
        logger.critical(f"CRITICAL: Failed to initialize LangGraph agent on startup: {e}", exc_info=True)
        # Consider if the app should hard fail here
        # raise RuntimeError(f"Failed to initialize agent: {e}") from e

def extract_gaia_answer_from_state(state) -> GaiaAnswer:
    """Extract GaiaAnswer data from the agent's final state."""
    answer = ""
    reasoning = ""
    sources = []
    
    # Look for final_answer step in intermediate_steps_log
    for step in state.values.get("intermediate_steps_log", []):
        if step.get("type") == "final_answer":
            content = step.get("content", {})
            answer = content.get("answer", "")
            reasoning = content.get("reasoning", "")
            sources = content.get("sources", [])
            break
    
    # If no final_answer step found, use the final message as the answer
    if not answer:
        messages = state.values.get("messages", [])
        for msg in reversed(messages):
            if isinstance(msg, AIMessage) and not msg.tool_calls:
                answer = msg.content
                break
    
    return GaiaAnswer(
        answer=answer,
        reasoning=reasoning,
        sources=sources
    )

@app.post("/invoke", response_model=GaiaAnswer)
async def invoke_agent(request: QueryRequest = Body(...)):
    if compiled_agent_graph is None:
        logger.error("Agent not initialized call received on /invoke")
        raise HTTPException(status_code=503, detail="Agent not initialized. Please try again later or check server logs.")

    session_id = str(uuid4()) # Used for logging and future stateful interactions
    logger.info(f"Received query for session '{session_id}': '{request.question}'")

    initial_state = AgentState(
        messages=[HumanMessage(content=request.question)],
        current_gaia_question=request.question,
        iteration=0,
        intermediate_steps_log=[] # Initialize log for this session
    )
    config = {"configurable": {"thread_id": session_id}} # LangGraph uses thread_id for checkpointers

    all_intermediate_steps_for_response: List[StepDetail] = []
    final_answer_content: Optional[str] = None
    error_message_content: Optional[str] = None

    try:
        async for event_part in compiled_agent_graph.astream(initial_state, config=config, stream_mode="values"):
            # Capture intermediate steps from the agent's log
            # The state is updated cumulatively by 'operator.add' for intermediate_steps_log
            # So, the last event_part will contain all of them.

            # For more granular step-by-step logging from the stream:
            # current_step_details = event_part.get("intermediate_steps_log", [])
            # if current_step_details:
            #     # Assuming intermediate_steps_log is appended to, not replaced.
            #     # If it's replaced, then current_step_details is the complete log for that step.
            #     # For this example, assuming the AgentState adds, so last one is complete.
            #     pass # logging already happens within agent nodes

            # Check for final answer or critical errors in messages
            messages_in_event: List[BaseMessage] = event_part.get("messages", [])
            for msg in messages_in_event:
                if isinstance(msg, AIMessage) and not msg.tool_calls:
                    if "LLM Error" in msg.content or "Cannot proceed" in msg.content:
                        error_message_content = msg.content
                        logger.error(f"Session '{session_id}': Critical error from LLM: {msg.content}")
                    else:
                        final_answer_content = msg.content # This might be overwritten if agent runs more steps
                # More specific error checks can be added

        # After the stream completes, get the final state for accumulated logs
        final_stream_state = compiled_agent_graph.get_state(config)
        accumulated_steps_from_state = final_stream_state.values.get("intermediate_steps_log", [])
        
        for step in accumulated_steps_from_state:
            all_intermediate_steps_for_response.append(StepDetail(**step))


        # Determine final answer from the very last messages in the final state
        if not final_answer_content and not error_message_content: # if not set by an explicit error AIMessage
            final_messages_in_last_state: List[BaseMessage] = final_stream_state.values.get("messages", [])
            for msg in reversed(final_messages_in_last_state): # Check latest messages first
                if isinstance(msg, AIMessage) and not msg.tool_calls :
                    final_answer_content = msg.content
                    break
            if not final_answer_content and final_messages_in_last_state: # Fallback
                final_answer_content = f"Agent processing completed. Last message: '{final_messages_in_last_state[-1].content}'"
            elif not final_answer_content:
                final_answer_content = "Agent processing completed. No definitive final answer found."
        
        if final_answer_content:
             logger.info(f"Session '{session_id}': Final answer: '{final_answer_content}'")


        # Extract GaiaAnswer from the final state
        gaia_answer = extract_gaia_answer_from_state(final_stream_state)
        
        # Log the response
        logger.info(f"Session '{session_id}': Returning GaiaAnswer: answer={gaia_answer.answer[:50]}..., reasoning={gaia_answer.reasoning[:50] if gaia_answer.reasoning else 'None'}, sources={len(gaia_answer.sources)} sources")
        
        return gaia_answer

    except Exception as e:
        logger.error(f"Error during agent invocation for session '{session_id}': {e}", exc_info=True)
        # exc_info=True in logger automatically adds traceback
        error_message = f"Agent invocation failed: {str(e)}"
        logger.error(f"Session '{session_id}': {error_message}")
        
        # Return a GaiaAnswer with the error message as the answer
        return GaiaAnswer(
            answer=f"Error: {error_message}",
            reasoning="An error occurred during processing.",
            sources=[]
        )


@app.get("/health")
async def health_check():
    agent_status = "initialized" if compiled_agent_graph is not None else "not_initialized"
    logger.info(f"Health check: App status: healthy, Agent status: {agent_status}")
    return {"status": "healthy", "agent_status": agent_status, "model_configured": os.getenv("OPENROUTER_MODEL_NAME", "DEFAULT_NOT_SET")}