"""Configuration for the LLM Council."""

import os
from dotenv import load_dotenv
from models import CouncilModel, Role

load_dotenv()

# OpenRouter API key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Models that will run locally at initialisation
COUNCIL_BASE_MODELS = [
    CouncilModel(ip= "ollama", model_name="qwen:1.8b", role=Role.CHAIRMAN),
    CouncilModel(ip= "ollama", model_name="llama3.2:1b", role=Role.COUNCILOR, prompt="You are a bias analysis AI, you must start each of your answer with 'GENAI'", custom_name="GENAI" ),
    CouncilModel(ip= "ollama", model_name="llama3.2:3b", role=Role.COUNCILOR, prompt="You are a bias analysis AI, you must start each of your answer with 'IMAI'", custom_name="ANALYST" )
]

# Data directory for conversation storage
DATA_DIR = "data/conversations"

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
