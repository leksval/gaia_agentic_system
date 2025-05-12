# app/tools.py
import json
import logging
from typing import Dict, Any, Type

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

# Import settings for API keys etc.
from .config import settings

# --- Basic Logging Setup ---
logger = logging.getLogger(__name__) # Gets logger named 'app.tools'

# --- Tool Input Definitions ---
class WebSearchInput(BaseModel):
    query: str = Field(description="The search query string to find information on the web.")

class CodeExecutionInput(BaseModel):
    code: str = Field(description="A snippet of Python code to execute for calculation or simple data manipulation. The code should aim to `print()` its result to be captured.")

# --- LangChain Tool Implementations ---
class WebSearchTool(BaseTool):
    name: str = "web_search"
    description: str = "Useful tool to search the web for information based on a query."
    args_schema: Type[BaseModel] = WebSearchInput
    
    def _run(self, query: str) -> str:
        logger.info(f"Executing web_search_tool with query: '{query}'")
        # Access config via settings object
        if not settings.tavily_api_key:
            logger.warning("TAVILY_API_KEY not set. Using mocked search results.")
            # ... (mock logic) ...
            if "capital of france" in query.lower(): return "The capital of France is Paris."
            return f"Mocked search results for: {query}. (TAVILY_API_KEY not set)"
        try:
            # Import locally to avoid dependency error if Tavily isn't installed/used
            from tavily import TavilyClient
            tavily = TavilyClient(api_key=settings.tavily_api_key) # Use settings
            response = tavily.search(query=query, search_depth="basic", max_results=3)
            results = json.dumps([{"url": res["url"], "content": res["content"]} for res in response.get("results", [])])
            logger.info(f"Web search successful.")
            return results
        except ImportError:
            logger.error("Tavily client library not found. Please install tavily-python.")
            return "Error: Tavily client library not installed."
        except Exception as e:
            logger.error(f"Error during Tavily search: {e}", exc_info=True)
            return f"Error during Tavily search: {str(e)}"

class CodeExecutionTool(BaseTool):
    name: str = "code_execution"
    description: str = "Executes a given snippet of Python code, useful for calculations or simple data manipulations."
    args_schema: Type[BaseModel] = CodeExecutionInput
    
    def _run(self, code: str) -> str:
        logger.info(f"Executing code_execution_tool.")
        logger.warning("SECURITY WARNING: Using simplified sandbox. Use proper sandboxing in production.")
        resolved_code = code.strip()
        try:
            if resolved_code.startswith("print("):
                try:
                    inner_content_str = resolved_code[len("print("):-1]
                    if (inner_content_str.startswith("'") and inner_content_str.endswith("'")) or \
                       (inner_content_str.startswith('"') and inner_content_str.endswith('"')):
                        result = inner_content_str[1:-1]
                    else:
                        result = str(eval(inner_content_str, {"__builtins__": {}}, {}))
                    logger.info(f"Code execution (print) successful.")
                    return result
                except Exception as e_print:
                    logger.error(f"Error evaluating print content: {e_print}", exc_info=True)
                    return f"Error evaluating print content: {str(e_print)}"
            else:
                result = str(eval(resolved_code, {"__builtins__": {}}, {}))
                logger.info(f"Code execution (eval) successful.")
                return f"Execution Result: {result}"
        except Exception as e:
            logger.error(f"Error executing code: {e}", exc_info=True)
            return f"Error executing code: {str(e)}."

# Create tool instances
web_search_tool = WebSearchTool()
code_execution_tool = CodeExecutionTool()

# List of available tools
TOOLS = [web_search_tool, code_execution_tool]
