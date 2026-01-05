"""Configuration for the LLM Council."""

import os
from dotenv import load_dotenv

load_dotenv()

# OpenRouter API key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Council members - list of OpenRouter model identifiers
COUNCIL_MODELS = [
    "openai/gpt-5.1",
    "google/gemini-3-pro-preview",
    "anthropic/claude-sonnet-4.5",
    "x-ai/grok-4",
]

# Chairman model - synthesizes final response
CHAIRMAN_MODEL = "google/gemini-3-pro-preview"

# OpenRouter API endpoint
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Data directory for conversation storage
DATA_DIR = "data/conversations"

# Ollama pour partie de matheo
OLLAMA_URL = 'http://localhost:11434/api/generate'
OLLAMA_MODEL = "qwen2.5:3b"

# Liste des biais cognitif étudiés et recherchés
CATEGORIES_BIAIS_ESSENTIELS = {
    "Logique & Information": [
        "Biais de confirmation (ne retient que ce qui l'arrange)",
        "Biais de cadrage (présentation trompeuse)", 
        "Généralisation hâtive",
        "Faux dilemme (blanc ou noir)",
        "Pente savonneuse (exagération des conséquences)",
        "Biais d'ancrage (focalisation sur le premier chiffre/idée)"
    ],
    "Influence Sociale & Autorité": [
        "Preuve sociale (tout le monde le fait)",
        "Argument d'autorité (c'est vrai car le chef le dit)",
        "Effet de halo (jugement global basé sur une qualité)",
        "Biais in-group/out-group (nous vs eux)",
        "Attaque Ad Hominem (attaque la personne, pas l'idée)"
    ],
    "Émotion & Manipulation": [
        "Appel à la peur",
        "Appel à l'émotion",
        "Biais de négativité",
        "Effet de victime identifiée",
        "Culpabilisation"
    ],
    "Décision & Argent": [
        "Biais des coûts irrécupérables (on a trop investi pour arrêter)",
        "Aversion à la perte",
        "Biais de statu quo (peur du changement)",
        "Effet de rareté (vite, il n'en reste plus !)",
        "Optimisme irréaliste"
    ]
}
