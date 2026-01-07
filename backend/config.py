"""Configuration for the LLM Council."""

import os
from dotenv import load_dotenv
from models import CouncilModel, Role

load_dotenv()

# OpenRouter API key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Models that will run locally at initialisation
COUNCIL_BASE_MODELS = [
    CouncilModel(ip= "ollama", model_name="qwen2.5:1.5b", role=Role.CHAIRMAN),
    CouncilModel(ip= "ollama", model_name="llama3.2:1b", role=Role.COUNCILOR, prompt="Tu es une IA d'analyse de biais, tu dois identifier, dans chaque requête, les biais congitifs pouvant être présent.", custom_name="C1" ),
    CouncilModel(ip= "ollama", model_name="gemma3:1b", role=Role.COUNCILOR, prompt="Tu es une IA d'analyse de biais, tu dois identifier, dans chaque requête, les biais congitifs pouvant être présent.", custom_name="C2" )
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
