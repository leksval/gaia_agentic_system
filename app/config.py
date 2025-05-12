# app/config.py
import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field # Import Field if you use it

# Determine the base directory where the .env file might be located
# This helps find the .env file correctly whether running directly or in Docker
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Settings(BaseSettings):
    # Load .env file if present. `env_file_encoding` ensures correct parsing.
    # Make sure your .env file is in the root directory where you run the app/docker context
    # If .env is elsewhere, adjust `env_file` path accordingly.
    # model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')
    # Updated way for pydantic-settings v2+
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'  # Ignore extra fields that might be in the env
    )

    # --- LLM Provider Selection ---
    llm_provider: str = Field(default="openrouter", description="LLM provider: 'openrouter' or 'ollama'")

    # --- OpenRouter Configuration ---
    openrouter_api_key: Optional[str] = Field(default=None, description="API key for OpenRouter")
    openrouter_model_name: str = Field(default="mistralai/mistral-7b-instruct-v0.2", description="Model name on OpenRouter")
    openrouter_base_url: str = Field(default="https://openrouter.ai/api/v1", description="API base URL for OpenRouter")

    # --- Ollama Configuration ---
    ollama_model_name: str = Field(default="llama3:8b-instruct", description="Model name for local Ollama")
    # Default needs careful consideration based on Docker networking setup
    ollama_base_url: str = Field(default="http://host.docker.internal:11434", description="API base URL for local Ollama (adjust for Docker network)")

    # --- Tool Configuration ---
    tavily_api_key: Optional[str] = Field(default=None, description="API key for Tavily Search")

    # --- Agent Configuration ---
    max_agent_iterations: int = Field(default=7, description="Maximum iterations for agent loops")

    # --- FastAPI/Server Configuration ---
    # These are typically not set via .env but via CMD/runtime flags, shown here for completeness
    # app_host: str = "0.0.0.0"
    # app_port: int = 8000

    # --- Derived Properties/Validation (Optional) ---
    # @computed_field # Requires Pydantic v2+
    # @property
    # def active_llm_model(self) -> str:
    #     if self.llm_provider == "ollama":
    #         return self.ollama_model_name
    #     return self.openrouter_model_name # Default to OpenRouter model

# Create a single instance of the settings to be imported elsewhere
settings = Settings()

# Optional: Add validation logic here if needed, e.g., ensure API key is present if provider is OpenRouter
# from pydantic import model_validator
# @model_validator(mode='after')
# def check_keys(self) -> 'Settings':
#     if self.llm_provider == 'openrouter' and not self.openrouter_api_key:
#         raise ValueError("OPENROUTER_API_KEY must be set when LLM_PROVIDER is 'openrouter'")
#     return self