"""Configuration for the LLM Council, updated."""

import os
from dotenv import load_dotenv
from models import CouncilModel, Role

load_dotenv()

# ============================================================================
# DISTRIBUTED ARCHITECTURE CONFIGURATION
# ============================================================================
# Local PC: Chairman LLM (synthesis only)
# > Configure the local chairman in the FIRST model in COUNCIL_BASE_MODELS
# > To use local container, use the IP : ollama
# > Adjust the port if necessary
#
# Remote PC: Council LLMs (multiple models for initial responses and peer review)
# > Configure the remote llms in the 1+ models in COUNCIL_BASE_MODELS
# > Indicate the remote ip : 10.0.0.X or 172.20.10.X or 192.168.0.X depending on network config
# > Adjust the port if necessary
# ============================================================================

# Constants, can be defined by an .env file
CHAIRMAN_IP = os.getenv("CHAIRMAN_IP", "ollama")  # Host IP, local container with ollama for chairman
OLLAMA_PORT = int(os.getenv("OLLAMA_PORT", "11434")) # Default ollama port

# All models used in the council, specify connection settings
COUNCIL_MODELS = [

    # Chairman model (host only)
    CouncilModel(
        ip="ollama", # Local ollama container (resolved with docker dns)
        port=OLLAMA_PORT,
        model_name="llama3.2:1b",
        role=Role.CHAIRMAN
    ),

    # Council models (remote or host)
    CouncilModel(
        ip="ollama", # Set the IP of a remote  PC with running ollama
        port=OLLAMA_PORT,
        model_name="qwen3:0.6b",
        role=Role.COUNCILOR

    ),
    CouncilModel(
        ip="ollama", # Set the IP of a remote PC with running ollama
        port=OLLAMA_PORT,
        model_name="gemma3:1b",
        role=Role.COUNCILOR

    ),
    CouncilModel(
        ip="ollama", # Set the IP of a remote PC with running ollama
        port=OLLAMA_PORT,
        model_name="qwen3:1.7b",
        role=Role.COUNCILOR
    )
]

# Data directory for conversation storage
DATA_DIR = "data/conversations"

PROMPT_INJECTION_STAGE_1 = """Tu es une IA d'analyse de bias cognitifs. 
La liste des biais à identifier sont les suivants :  
    - Biais de confirmation 
    - Biais de cadrage
    - Généralisation hâtive
    - Faux dilemme
    - Pente savonneuse
    - Biais d'ancrage
    - Preuve sociale
    - Argument d'autorité
    - Effet de halo
    - Biais in-group/out-group
    - Attaque Ad Hominem
    - Appel à la peur
    - Appel à l'émotion
    - Biais de négativité
    - Effet de victime identifiée
    - Culpabilisation
    - Biais des coûts irrécupérables
    - Aversion à la perte
    - Biais de statu quo
    - Effet de rareté
    - Optimisme irréaliste

Effectue maintenant une analyse des biais contenus dans le message suivant : 
"""

PROMPT_INJECTION_STAGE_3 = """
    Réalise une synthèse des biais cognitifs observés et attribue une note de dangerosité pour chacun d'entre eux.
    Ta réponse doit être synthétique, sous forme de bullet points.
"""