#!/usr/bin/env python3
"""
GAIA Pathfinder Agent API Test Script

This script tests the GAIA Pathfinder Agent API by sending each of the
predefined GAIA test questions and validating the response format.
"""

import json
import requests
import time
import sys
import argparse
from typing import List, Dict, Any, Optional

# GAIA test questions
GAIA_TEST_QUESTIONS = [
    {
        "id": 1,
        "question": "What would happen if all insects on Earth disappeared overnight?",
        "description": "Ecological impact assessment"
    },
    {
        "id": 2,
        "question": "How might quantum computing affect modern cryptography?",
        "description": "Technology impact analysis"
    },
    {
        "id": 3,
        "question": "What are the potential long-term consequences of ocean acidification?",
        "description": "Environmental science"
    },
    {
        "id": 4,
        "question": "How does chronic sleep deprivation affect cognitive function and overall health?",
        "description": "Health and neuroscience"
    },
    {
        "id": 5,
        "question": "What would be the economic and social implications of universal basic income?",
        "description": "Economics and social policy"
    },
    {
        "id": 6,
        "question": "How might artificial general intelligence change human society?",
        "description": "AI and future studies"
    }
]

def test_api_health(base_url: str) -> bool:
    """Test if the API is healthy and running."""
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"API Health: {health_data}")
            return health_data.get("status") == "healthy" and health_data.get("agent_status") == "initialized"
        return False
    except requests.RequestException as e:
        print(f"Error checking API health: {e}")
        return False

def validate_gaia_answer(response_data: Dict[str, Any]) -> List[str]:
    """Validate that the response follows the GaiaAnswer format."""
    errors = []
    
    # Check required fields
    if "answer" not in response_data:
        errors.append("Missing required field: 'answer'")
    elif not response_data["answer"] or not isinstance(response_data["answer"], str):
        errors.append("Field 'answer' must be a non-empty string")
    
    # Check optional fields
    if "reasoning" in response_data and not isinstance(response_data["reasoning"], (str, type(None))):
        errors.append("Field 'reasoning' must be a string or null")
    
    if "sources" in response_data:
        if not isinstance(response_data["sources"], list):
            errors.append("Field 'sources' must be an array")
        else:
            for i, source in enumerate(response_data["sources"]):
                if not isinstance(source, str):
                    errors.append(f"Source at index {i} must be a string")
    
    return errors

def test_question(base_url: str, question: Dict[str, Any], verbose: bool = False) -> Dict[str, Any]:
    """Test a single GAIA question and return the results."""
    print(f"\nTesting Question {question['id']}: {question['description']}")
    print(f"Question: {question['question']}")
    
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{base_url}/invoke",
            json={"question": question["question"]},
            headers={"Content-Type": "application/json"}
        )
        
        elapsed_time = time.time() - start_time
        
        if response.status_code != 200:
            return {
                "question_id": question["id"],
                "success": False,
                "error": f"HTTP Error: {response.status_code}",
                "elapsed_time": elapsed_time
            }
        
        response_data = response.json()
        
        if verbose:
            print("\nResponse:")
            print(json.dumps(response_data, indent=2))
        
        validation_errors = validate_gaia_answer(response_data)
        
        if validation_errors:
            return {
                "question_id": question["id"],
                "success": False,
                "error": f"Validation errors: {', '.join(validation_errors)}",
                "elapsed_time": elapsed_time
            }
        
        # Check response quality (basic checks)
        answer_length = len(response_data.get("answer", ""))
        has_reasoning = bool(response_data.get("reasoning", ""))
        has_sources = len(response_data.get("sources", [])) > 0
        
        print(f"Response received in {elapsed_time:.2f} seconds")
        print(f"Answer length: {answer_length} characters")
        print(f"Has reasoning: {has_reasoning}")
        print(f"Number of sources: {len(response_data.get('sources', []))}")
        
        return {
            "question_id": question["id"],
            "success": True,
            "elapsed_time": elapsed_time,
            "answer_length": answer_length,
            "has_reasoning": has_reasoning,
            "has_sources": has_sources
        }
        
    except requests.RequestException as e:
        return {
            "question_id": question["id"],
            "success": False,
            "error": f"Request error: {str(e)}",
            "elapsed_time": time.time() - start_time
        }

def main():
    parser = argparse.ArgumentParser(description="Test the GAIA Pathfinder Agent API")
    parser.add_argument("--base-url", default="http://localhost:8000", help="Base URL of the API")
    parser.add_argument("--question-id", type=int, help="Test only a specific question ID")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show full responses")
    args = parser.parse_args()
    
    print(f"Testing GAIA Pathfinder Agent API at {args.base_url}")
    
    # Check if API is healthy
    if not test_api_health(args.base_url):
        print("API is not healthy. Exiting.")
        sys.exit(1)
    
    # Determine which questions to test
    questions_to_test = []
    if args.question_id:
        question = next((q for q in GAIA_TEST_QUESTIONS if q["id"] == args.question_id), None)
        if question:
            questions_to_test = [question]
        else:
            print(f"Question ID {args.question_id} not found.")
            sys.exit(1)
    else:
        questions_to_test = GAIA_TEST_QUESTIONS
    
    # Run tests
    results = []
    for question in questions_to_test:
        result = test_question(args.base_url, question, args.verbose)
        results.append(result)
    
    # Print summary
    print("\n=== Test Summary ===")
    success_count = sum(1 for r in results if r["success"])
    print(f"Successful tests: {success_count}/{len(results)}")
    
    if success_count < len(results):
        print("\nFailed tests:")
        for result in results:
            if not result["success"]:
                question = next(q for q in GAIA_TEST_QUESTIONS if q["id"] == result["question_id"])
                print(f"  Question {result['question_id']} ({question['description']}): {result.get('error', 'Unknown error')}")
    
    avg_time = sum(r["elapsed_time"] for r in results) / len(results)
    print(f"\nAverage response time: {avg_time:.2f} seconds")
    
    # Return exit code based on success
    return 0 if success_count == len(results) else 1

if __name__ == "__main__":
    sys.exit(main())