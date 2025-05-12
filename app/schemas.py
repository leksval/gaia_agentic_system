from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Any, Dict

class QueryRequest(BaseModel):
    question: str

class ToolCallRepresentation(BaseModel): # Renamed for clarity
    tool_name: str
    tool_args: Dict[str, Any]
    tool_call_id: Optional[str] = None # Added for better tracking

class ToolObservationRepresentation(BaseModel): # Renamed for clarity
    tool_name: str
    content: str
    tool_call_id: Optional[str] = None # Added for better tracking

class StepDetail(BaseModel):
    type: str # e.g., "llm_thought", "tool_call", "tool_observation", "error_message"
    content: Any

class AgentResponse(BaseModel):
    final_answer: Optional[str] = None
    intermediate_steps: List[StepDetail] = []
    error_message: Optional[str] = None # More prominent error field
    session_id: Optional[str] = None # For future stateful use

class GaiaAnswer(BaseModel):
    """Structured response format for GAIA benchmark questions."""
    answer: str = Field(description="The final answer to the question, based on all available information.")
    reasoning: Optional[str] = Field(default=None, description="The reasoning process that led to the answer.")
    sources: Optional[List[str]] = Field(default_factory=list, description="Sources or references used to derive the answer.")
    
    @field_validator('answer')
    def answer_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Answer cannot be empty")
        return v