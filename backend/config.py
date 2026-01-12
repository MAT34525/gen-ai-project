"""Configuration for the LLM Council."""

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
# > Configure the remote lls in the 1+ models in COUNCIL_BASE_MODELS
# > Indicate the remote ip : 10.0.0.X or 172.20.10.X or 192.168.0.X depending on network config
# > Adjust the port if necessary
# ============================================================================

# Constants, can be defined by an .env file
CHAIRMAN_IP = os.getenv("CHAIRMAN_IP", "ollama")  # PC1 IP, local container use the ollama name
OLLAMA_PORT = int(os.getenv("OLLAMA_PORT", "11434"))

# Models that will run locally at initialization
COUNCIL_BASE_MODELS = [

    # Chairman model (PC1)
    CouncilModel(
        ip="ollama", # Local ollama container (resolved with docker dns)
        port=OLLAMA_PORT,
        model_name="llama3.2:1b",
        role=Role.CHAIRMAN
    ),

    # Council models (PC2) - using base models without custom prompts for now
    CouncilModel(
        ip="<other PC local ip>", # Set the IP of a remote PC with running ollama
        port=OLLAMA_PORT,
        model_name="llama3.2:1b",
        role=Role.COUNCILOR
    ),
    CouncilModel(
        ip="<other PC local ip>", # Set the IP of a remote PC with running ollama
        port=OLLAMA_PORT,
        model_name="gemma2:2b",
        role=Role.COUNCILOR
    ),
    CouncilModel(
        ip="<other PC local ip>",
        port=OLLAMA_PORT,
        model_name="phi3:3.8b",
        role=Role.COUNCILOR
    )
]

# Data directory for conversation storage
DATA_DIR = "data/conversations"

# Promp for bias analysis
CATEGORIES_BIAIS_ESSENTIELS = """
    Logique & Information: 
        Biais de confirmation (ne retient que ce qui l'arrange),
        Biais de cadrage (présentation trompeuse), 
        Généralisation hâtive,
        Faux dilemme (blanc ou noir),
        Pente savonneuse (exagération des conséquences),
        Biais d'ancrage (focalisation sur le premier chiffre/idée)
    
    Influence Sociale & Autorité: 
        Preuve sociale (tout le monde le fait),
        Argument d'autorité (c'est vrai car le chef le dit),
        Effet de halo (jugement global basé sur une qualité),
        Biais in-group/out-group (nous vs eux),
        Attaque Ad Hominem (attaque la personne, pas l'idée)
    
    Émotion & Manipulation: 
        Appel à la peur,
        Appel à l'émotion,
        Biais de négativité,
        Effet de victime identifiée,
        Culpabilisation
    
    Décision & Argent: 
        Biais des coûts irrécupérables (on a trop investi pour arrêter),
        Aversion à la perte,
        Biais de statu quo (peur du changement),
        Effet de rareté (vite, il n'en reste plus !),
        Optimisme irréaliste
"""

# Prompt injection for bias analysis
PROMPT_PRE_INJECTION = f"""
Rôle : Expert en analyse critique.
    Tâche : Analyse le texte pour trouver UNIQUEMENT ces biais : 
    
Biais :
{CATEGORIES_BIAIS_ESSENTIELS}

Instructions :

Sois critique : ne signale un biais que s'il est évident, mais signale tout les biais que tu trouve.
Répond au format attendu.  


Exemple de format attendu :
    biais_trouves : 
        nom : Nom du biais exact,
        citation : La phrase du texte concernée,
        explication : Pourquoi c'est un biais en 1 phrase,
        gravité : "Faible/Moyen/Élevé" (en prenant en compte si le biais est utilisé de manière positive/négative)
"""
