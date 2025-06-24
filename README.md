# GAIA: General Artificial Inteligence Agent System
## Description

This project implements a dockerized FastAPI server for easy deployment and environment consistency. 
This AI agent system is designed to tackle complex questions tested on real L1 GAIA benchmark. It uses LangChain for agent creation and LangGraph for workflow orchestration, supports interchangeable LLM backends (OpenRouter cloud models or local Ollama models via LiteLLM), and includes web search and code execution.

**This Minimum Viable Product (MVP) demonstrating core concepts of building modular AI agent systems.**

## Testing demo
https://github.com/user-attachments/assets/86ccc2f3-57fb-400c-b867-6f4e69d4edb6

## Process workflow
Here's a high-level overview of the GAIA Pathfinder Agent API process workflow:

1. **Receive Question**: The API receives a question from a user through an HTTP POST request or via html UI.
2. **Parse Question**: The question is parsed to determine the type of response required (e.g., text, code execution).
3. **Invoke Tool**: Based on the question type, the corresponding tool is invoked:
	* `text_generation_tool` for simple text-based questions
	* `code_execution_tool` for code-related questions ( secure sandboxing)
4. **Execute Tool**:
	* For text generation: Use a language model to generate a response.
	* For code execution: Execute the provided code in a secure sandbox environment and return the output.
5. **Format Response**: The tool's output is formatted into a standardized GaiaAnswer format, including answer text, metadata, and optional attachments (e.g., images).
6. **Return Response**: The formatted response is returned to the user through an HTTP response.

**Optional Steps**

1. **State Management**: If conversational state management is enabled, the API stores and retrieves context from previous interactions to inform future responses.
2. **Error Handling**: If errors occur during tool invocation or execution, error handling mechanisms are triggered to provide a graceful fallback or informative error message.

This process workflow can be further refined as needed based on specific requirements and implementation details.

## Table of Contents

- [Quick Start](#quick-start)
- [Features](#features)
- [Project Structure](#project-structure)
- [Architecture](#architecture)
  - [Key Architectural Points](#key-architectural-points)
  - [Structured Output Handling](#structured-output-handling)
  - [Expected Response Format](#expected-response-format)
- [Setup and Installation](#setup-and-installation)
  - [Prerequisites](#prerequisites)
  - [Configuration](#configuration)
- [Dependencies](#dependencies)
- [Running the Application](#running-the-application)
- [🚨 Security Warning](#-security-warning)
- [Testing](#testing)
- [Future Improvements](#future-improvements)
- [License](#license)


## Quick Start

Get up and running with GAIA Pathfinder Agent API in minutes:

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-directory>
   ```

2. **Create a minimal .env file**
   ```bash
   echo "LLM_PROVIDER=openrouter
   OPENROUTER_API_KEY=your-openrouter-key
   OPENROUTER_MODEL_NAME=openai/gpt-3.5-turbo" > .env
   ```

3. **Build and run with Docker**
   ```bash
   docker build -t gaia-agent-api .
   docker run --rm -p 8000:8000 --env-file .env gaia-agent-api
   ```

4. **Test the API**
   ```bash
   curl -X POST "http://localhost:8000/invoke" \
        -H "Content-Type: application/json" \
        -d '{"question": "What is the capital of France?"}'
   ```

5. **Open the web interface**
   
   Open `tests/gaia/test_api.html` in your browser to test with a user-friendly interface

## Features

*   **AI Agent:** Uses LangChain's `AgentExecutor` for reasoning and LangGraph for workflow orchestration.
*   **LLM Flexibility:** Supports OpenRouter and local Ollama models via LangChain's integration with LiteLLM. Configurable via environment variables.
*   **Tool Usage:** Includes basic web search (Tavily) and Python code execution tools implemented as LangChain tools.
*   **Structured Output:** Leverages Pydantic models (`GaiaAnswer`) with multiple approaches to ensure structured responses from the LLM.
*   **API Server:** Built with FastAPI, providing asynchronous request handling and automatic OpenAPI documentation (`/docs`).
*   **Configuration:** Uses Pydantic Settings (`config.py`) to manage configuration via `.env` files and environment variables.
*   **Containerization:** Dockerized for consistent builds and deployment (`Dockerfile`).
*   **Modularity:** Code is organized into distinct components (API, Agent, Tools, Config, Schemas).

## Project Structure

```
.
├── Dockerfile                      # Defines the Docker image build process
├── requirements.txt                # Python dependencies
├── .dockerignore                   # Specifies files/dirs to exclude from Docker image
├── .env                            # Local configuration (API keys, etc.) - NOT version controlled
├── README.md                       # Project documentation (this file)
├── app/                            # Main application package
│   ├── __init__.py                 # Makes 'app' a Python package
│   ├── main.py                     # FastAPI application setup, endpoints, and routing
│   ├── agent.py                    # LangChain Agent initialization and LangGraph orchestration logic
│   ├── tools.py                    # Implementation of LangChain tools (web search, code exec)
│   ├── schemas.py                  # Pydantic models for FastAPI request/response bodies
│   └── config.py                   # Pydantic Settings model for loading configuration from .env/environment
└── tests/                          # Test directory
    └── gaia/                       # GAIA benchmark test suite
        ├── gaia_test_questions.js  # Predefined GAIA test questions
        ├── test_api.html           # Simple HTML page for testing the API
        └── test_api.py             # Automated test script for the API
```

## Architecture

### Key Architectural Points

*   **Agent Framework:** Utilizes LangChain for agent creation and LangGraph for workflow orchestration, leveraging Pydantic for structured data handling (tools and responses).
*   **Configuration:** Centralized and type-safe configuration loading using Pydantic Settings.
*   **API Design:** FastAPI with Pydantic schemas ensures robust request/response handling and automatic documentation.
*   **Modularity:** Separation of concerns between API, agent logic, tools, and configuration.
*   **LLM Abstraction:** Uses LangChain's integration with LiteLLM to support different LLM providers (OpenRouter, Ollama) through configuration.
*   **Workflow Management:** Uses LangGraph for creating a directed graph of agent and tool nodes, enabling complex reasoning flows.
*   **State Tracking:** Maintains conversation state and tracks intermediate steps for debugging and transparency.
*   **Termination Logic:** Implements proper end conditions to ensure the agent workflow terminates correctly.
*   **Memory Management:** Uses LangGraph's memory checkpointer to maintain state between steps and across sessions.
*   **Structured Output Handling:** Multiple approaches for ensuring structured outputs:
  * Function calling for OpenAI-compatible models
  * Post-processing with regex for other models
  * Fallback mechanisms for error handling

### Structured Output Handling

The system uses several approaches to ensure structured outputs in the GaiaAnswer format:

1. **Function Calling (OpenAI-compatible models)**: For models that support function calling, we use LangChain's function calling capabilities to directly request responses in the GaiaAnswer format.

2. **Post-Processing**: For other models or as a fallback, we use regex-based post-processing to extract structured information from the model's output.

3. **Fallback Mechanisms**: If structured parsing fails, we fall back to using the raw output while maintaining the expected response format.

This ensures consistent API responses regardless of the underlying LLM provider.

### Expected Response Format (GaiaAnswer)

The API returns responses in a structured format defined by the GaiaAnswer schema. Here's a sample GAIA test question and the expected response format:

#### Sample GAIA Question

```
What would happen if all insects on Earth disappeared overnight?
```

#### Expected Response Structure (GaiaAnswer format)

```json
{
  "answer": "If all insects on Earth disappeared overnight, it would trigger a catastrophic ecological collapse with far-reaching consequences. Pollination would immediately be disrupted, threatening 75-80% of wild plants and many agricultural crops. Food webs would collapse as insects are primary consumers and food sources for many animals. Decomposition processes would slow dramatically, leading to accumulation of dead organic matter. Aquatic ecosystems would be severely impacted as many insects have aquatic larval stages. Human food security would be threatened, with potential crop failures leading to widespread famine. The economic impact would be enormous, with estimates suggesting insect ecological services are worth over $57 billion annually in the US alone. In summary, insect extinction would likely lead to ecosystem collapse, mass extinction of dependent species, and potentially threaten human civilization.",
  
  "reasoning": "To analyze this question, I need to consider the ecological roles insects play and the cascading effects of their removal. Insects are crucial for: 1) Pollination of flowering plants, 2) Being primary consumers in food webs, 3) Serving as food sources for many animals, 4) Decomposition of organic matter, 5) Soil health maintenance, 6) Aquatic ecosystem functioning. Their sudden disappearance would disrupt all these processes simultaneously, leading to system-wide ecological collapse. The effects would compound over time, with initial failures in pollination and predator starvation, followed by longer-term issues with waste accumulation and soil degradation.",
  
  "sources": [
    "https://www.sciencedirect.com/science/article/pii/S0006320719317823",
    "https://www.pnas.org/content/118/2/e2023989118",
    "https://www.biologicaldiversity.org/campaigns/saving-the-insects/pdfs/Insect-Apocalypse-and-Food-Security-FINAL.pdf"
  ]
}
```

This structured format allows the system to:

1. Provide a comprehensive answer to the question
2. Show the reasoning process that led to the answer
3. Cite sources that support the information provided

The GAIA Pathfinder Agent API is designed to process complex questions and return structured responses in this format, regardless of which underlying LLM provider is used (OpenRouter or Ollama).

## Setup and Installation

### Prerequisites

*   Docker installed and running.
*   Python 3.9+ (for potential local development outside Docker).
*   An `.env` file created in the project root (see Configuration).
*   (Optional) Ollama installed and running locally if using the `ollama` provider.
*   (Optional) API Key for Tavily Search if using the `web_search_tool`.
*   API Key for OpenRouter if using the `openrouter` provider.
*   Required Python packages: fastapi, uvicorn, pydantic, pydantic-settings, litellm, langgraph, langchain, langchain-core, langchain-openai, langchain-community (see requirements.txt).

### Configuration

1.  Clone the repository:
    ```bash
    git clone <your-repo-url>
    cd <your-repo-directory>
    ```
2.  Create a `.env` file in the project root directory. Copy the contents from the example below and fill in your credentials and desired settings:
    ```env
    # --- Choose LLM Provider ---
    # Set to openrouter or ollama
    LLM_PROVIDER=openrouter

    # --- OpenRouter Configuration (if LLM_PROVIDER=openrouter) ---
    OPENROUTER_API_KEY=sk-or-your-openrouter-key
    # Available models:
    # OPENROUTER_MODEL_NAME=google/gemini-2.5-pro-preview
    # OPENROUTER_MODEL_NAME=anthropic/claude-3-haiku-20240307
    # OPENROUTER_MODEL_NAME=mistral/mistral-7b-instruct-v0.2
    OPENROUTER_MODEL_NAME=openai/gpt-3.5-turbo
    # OPENROUTER_BASE_URL=https://openrouter.ai/api/v1 # Default usually fine

    # --- Ollama Configuration (if LLM_PROVIDER=ollama) ---
    OLLAMA_MODEL_NAME=llama3:8b-instruct
    # Adjust if your Ollama is not accessible via default Docker host mapping
    OLLAMA_BASE_URL=http://host.docker.internal:11434

    # --- Tool Configuration ---
    # TAVILY_API_KEY=tvly-your-tavily-api-key # Required for web_search_tool

    # --- Agent Configuration ---
    MAX_AGENT_ITERATIONS=7
    ```

## Dependencies

The project uses several key dependencies:

* **FastAPI**: Web framework for building APIs
* **Pydantic**: Data validation and settings management
* **LangChain**: Agent creation, tool definition, and LLM integration
* **LangGraph**: Workflow orchestration and state management
* **LiteLLM**: LLM provider abstraction
* **Tavily**: Web search capability

All dependencies are specified with version constraints in `requirements.txt` to ensure compatibility.

## Running the Application

1.  **Build the Docker Image:**
    ```bash
    docker build -t gaia-agent-api .
    ```

2.  **Run the Docker Container:**
    *   Make sure your `.env` file exists in the root directory where you run the `docker run` command OR pass variables directly.
    *   The command below uses `--env-file` to load variables from your `.env` file into the container.
    ```bash
    docker run --rm -p 8000:8000 \
      --env-file .env \
      gaia-agent-api
    ```
    *   *(Alternative - passing specific variables explicitly)*:
    ```bash
    # docker run --rm -p 8000:8000 \
    #   -e LLM_PROVIDER="openrouter" \
    #   -e OPENROUTER_API_KEY="sk-or-your-key" \
    #   -e OPENROUTER_MODEL_NAME="openai/gpt-3.5-turbo" \
    #   -e TAVILY_API_KEY="tvly-your-key" \
    #   gaia-agent-api
    ```

    **Note**: When using environment variables in the `.env` file, make sure to omit comments on the same line as values to ensure proper parsing. This is especially important for:
    - Integer values like `MAX_AGENT_ITERATIONS`
    - String values that are used for comparison like `LLM_PROVIDER`
    - API keys and URLs
    
    When running with Docker using `--env-file`, be aware that Docker might preserve quotes in environment variables. The application has been updated to handle this case by stripping quotes from values where necessary.

3.  **Access the API:**
    *   Open your browser to `http://localhost:8000/docs` for the interactive FastAPI documentation.
    *   Send a POST request to `http://localhost:8000/invoke` using `curl` or a tool like Postman:
        ```bash
        curl -X POST "http://localhost:8000/invoke" \
             -H "Content-Type: application/json" \
             -d '{"question": "What is the capital of France?"}'
        ```
    *   Check the health endpoint: `http://localhost:8000/health`
    *   Use the included `tests/gaia/test_api.html` file to test the API from a browser

## Testing

The project includes a set of GAIA test questions and automated testing scripts to validate the API's functionality and response format.

### GAIA Test Questions

The `tests/gaia/` directory contains:

- 6 predefined GAIA test questions covering different domains of knowledge
- Expected responses in the GaiaAnswer format
- A web interface for manual testing

### Running Tests

1. Start the GAIA Pathfinder Agent API server:
   ```bash
   python -m app.main
   ```

2. Use one of the following methods to test the API:

   * **Web Interface**: Open `tests/gaia/test_api.html` in a browser


## License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
