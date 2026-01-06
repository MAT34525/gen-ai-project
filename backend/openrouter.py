"""OpenRouter API client for making LLM requests."""

import httpx
from typing import List, Dict, Any, Optional

from models import CouncilModel

#code matheo
import asyncio

async def query_model(model: CouncilModel, messages: List[Dict[str, str]]) -> Optional[Dict[str, Any]]:
    # code origine
    """
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": messages,
    }

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                OPENROUTER_API_URL,
                headers=headers,
                json=payload
            )
            response.raise_for_status()

            data = response.json()
            message = data['choices'][0]['message']

            return {
                'content': message.get('content'),
                'reasoning_details': message.get('reasoning_details')
            }

    except Exception as e:
        print(f"Error querying model {model}: {e}")
        return None
    """
    
    #code matheo
    """Envoie une requête à l'instance Ollama locale."""

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "model": model.model_name,
        "messages": messages,
        "stream": False  # On désactive le streaming pour récupérer la réponse complète
    }

    try:
        async with httpx.AsyncClient() as client:
            
            url: str = f"http://{model.ip}:{model.port}/api/chat"

            # Augmenter le timeout car les modèles locaux peuvent mettre du temps à répondre
            response = await client.post(
                url, 
                json=payload,
                headers=headers,
                timeout=60.0 
            )

            response.raise_for_status()

            data = response.json()

            return {
                'content': data['message']['content'],
                'reasoning_details': None
            }
    except Exception as e:
        print(f"Erreur lors de la requête vers {model}: {e}")
        return None


async def query_models_parallel(models: List[CouncilModel], messages: List[Dict[str, str]]) -> Dict[str, Optional[Dict[str, Any]]]:
    #code origine

    # Create tasks for all models
    tasks = [query_model(model, messages) for model in models]

    # Wait for all to complete
    responses = await asyncio.gather(*tasks)

    # Map models to their responses
    resp = {model.model_name: response for model, response in zip(models, responses)}

    return resp
