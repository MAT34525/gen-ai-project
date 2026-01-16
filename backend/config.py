"""Configuration for the LLM Council."""

import os
from dotenv import load_dotenv
from models import CouncilModel, Role

load_dotenv()

# ============================================================================
# DISTRIBUTED ARCHITECTURE CONFIGURATION (2-PC Setup)
# ============================================================================
# PC1: Chairman LLM (synthesis only)
# PC2: Council LLMs (multiple models for initial responses and peer review)
#
# Configure the IPs below or use environment variables:
# - CHAIRMAN_IP: IP address of PC running the Chairman LLM
# - COUNCIL_IP: IP address of PC running the Council LLMs
# ============================================================================

# Chairman configuration (runs on PC1)
CHAIRMAN_IP = os.getenv("CHAIRMAN_IP", "localhost")  # PC1 IP
CHAIRMAN_PORT = int(os.getenv("CHAIRMAN_PORT", "11434"))
CHAIRMAN_MODEL = os.getenv("CHAIRMAN_MODEL", "qwen2.5:1.5b")

# Council configuration (runs on PC2)
COUNCIL_IP = os.getenv("COUNCIL_IP", "localhost")  # PC2 IP
COUNCIL_PORT = int(os.getenv("COUNCIL_PORT", "11434"))

# Models that will run locally at initialization
COUNCIL_BASE_MODELS = [
    # Chairman model (PC1)
    CouncilModel(
        ip=CHAIRMAN_IP,
        port=CHAIRMAN_PORT,
        model_name=CHAIRMAN_MODEL,
        role=Role.CHAIRMAN
    ),
    # Council models (PC2) - using base models without custom prompts for now

    CouncilModel(
        ip=COUNCIL_IP,
        port=COUNCIL_PORT,
        model_name="llama3.2:1b",
        role=Role.COUNCILOR

    ),
    CouncilModel(
        ip=COUNCIL_IP,
        port=COUNCIL_PORT,
        model_name="gemma2:2b",
        role=Role.COUNCILOR

    ),
    CouncilModel(
        ip=COUNCIL_IP,
        port=COUNCIL_PORT,
        model_name="phi3:3.8b",
        role=Role.COUNCILOR
    )
]

# Data directory for conversation storage
DATA_DIR = "data/conversations"

# Liste des biais cognitif étudiés et recherchés
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
