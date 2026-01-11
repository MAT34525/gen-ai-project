"""Ollama API client for making LLM requests to distributed Ollama instances."""

import httpx
from typing import List, Dict, Any, Optional
import asyncio

from models import CouncilModel


async def query_model(
    model: CouncilModel,
    messages: List[Dict[str, str]],
    timeout: float = 180.0
) -> Optional[Dict[str, Any]]:
    """
    Send a request to a local or remote Ollama instance.
    
    Args:
        model: CouncilModel instance with connection details
        messages: List of message dictionaries with 'role' and 'content'
        timeout: Request timeout in seconds (default: 180s for local LLMs)
    
    Returns:
        Dictionary with 'content' and 'reasoning_details' (None for Ollama)
        Returns None if the request fails
    """
    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "model": model.model_name,
        "messages": messages,
        "stream": False  # Disable streaming to get complete response
    }

    try:
        async with httpx.AsyncClient() as client:
            url = f"http://{model.ip}:{model.port}/api/chat"
            
            response = await client.post(
                url,
                json=payload,
                headers=headers,
                timeout=timeout
            )
            response.raise_for_status()

            data = response.json()

            return {
                'content': data['message']['content'],
                'reasoning_details': None
            }
        
    except httpx.TimeoutException:
        print(f"Timeout error when querying {model.model_name} at {model.ip}:{model.port}")
        return None
    except httpx.HTTPStatusError as e:
        print(f"HTTP error {e.response.status_code} when querying {model.model_name}: {e}")
        return None
    except Exception as e:
        print(f"Error querying {model.model_name} at {model.ip}:{model.port}: {e}")
        return None


async def query_models_parallel(
    models: List[CouncilModel],
    messages: List[Dict[str, str]],
    timeout: float = 180.0
) -> Dict[str, Optional[Dict[str, Any]]]:
    """
    Query multiple Ollama models in parallel across distributed instances.
    
    Args:
        models: List of CouncilModel instances
        messages: List of message dictionaries to send to each model
        timeout: Request timeout in seconds
    
    Returns:
        Dictionary mapping model names to their responses
    """
    # Create tasks for all models
    tasks = [query_model(model, messages, timeout) for model in models]

    # Wait for all to complete
    responses = await asyncio.gather(*tasks)

    # Map models to their responses
    return {model.model_name: response for model, response in zip(models, responses)}


async def check_model_health(model: CouncilModel) -> bool:
    """
    Check if an Ollama instance is reachable and the model is available.
    
    Args:
        model: CouncilModel instance to check
    
    Returns:
        True if the model is available, False otherwise
    """
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            url = f"http://{model.ip}:{model.port}/api/tags"
            response = await client.get(url)
            response.raise_for_status()
            
            data = response.json()
            # Check if the model exists in the list of available models
            available_models = [m['name'] for m in data.get('models', [])]
            return model.model_name in available_models
    except Exception as e:
        print(f"Health check failed for {model.model_name} at {model.ip}:{model.port}: {e}")
        return False
