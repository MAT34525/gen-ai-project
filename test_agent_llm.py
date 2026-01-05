import requests
import json

# --- CONFIGURATION ---
OLLAMA_URL = 'http://localhost:11434/api/generate'
MODEL = "qwen2.5:3b"

# --- LISTE OPTIMISÉE (Biais détectables textuellement) ---
# J'ai regroupé les biais par "nature" de l'erreur pour aider le modèle.
CATEGORIES_BIAIS_ESSENTIELS = {
    "🧠 Logique & Information": [
        "Biais de confirmation (ne retient que ce qui l'arrange)",
        "Biais de cadrage (présentation trompeuse)", 
        "Généralisation hâtive",
        "Faux dilemme (blanc ou noir)",
        "Pente savonneuse (exagération des conséquences)",
        "Biais d'ancrage (focalisation sur le premier chiffre/idée)"
    ],
    "🗣️ Influence Sociale & Autorité": [
        "Preuve sociale (tout le monde le fait)",
        "Argument d'autorité (c'est vrai car le chef le dit)",
        "Effet de halo (jugement global basé sur une qualité)",
        "Biais in-group/out-group (nous vs eux)",
        "Attaque Ad Hominem (attaque la personne, pas l'idée)"
    ],
    "💔 Émotion & Manipulation": [
        "Appel à la peur",
        "Appel à l'émotion",
        "Biais de négativité",
        "Effet de victime identifiée",
        "Culpabilisation"
    ],
    "💰 Décision & Argent": [
        "Biais des coûts irrécupérables (on a trop investi pour arrêter)",
        "Aversion à la perte",
        "Biais de statu quo (peur du changement)",
        "Effet de rareté (vite, il n'en reste plus !)",
        "Optimisme irréaliste"
    ]
}

# --- FONCTIONS ---

def analyse_categorie(nom_categorie, liste_biais, texte):
    """Interroge Ollama pour une catégorie spécifique"""
    
    prompt = f"""
    Rôle : Expert en analyse critique.
    Tâche : Analyse le texte pour trouver UNIQUEMENT ces biais : {', '.join(liste_biais)}.
    
    Instructions :
    1. Sois critique : ne signale un biais que s'il est évident.
    2. Réponds au format JSON strict.

    Format JSON attendu :
    {{
        "biais_trouves": [
            {{
                "nom": "Nom du biais exact",
                "citation": "La phrase du texte concernée",
                "explication": "Pourquoi c'est un biais en 1 phrase",
                "gravite": "Faible/Moyen/Élevé"
            }}
        ]
    }}

    Texte : "{texte}"
    """

    try:
        response = requests.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": prompt,
            "format": "json",
            "stream": False,
            "options": {"temperature": 0.1, "num_ctx": 4096}
        })
        response.raise_for_status()
        return json.loads(response.json()['response'])
    except Exception as e:
        return {"biais_trouves": []}

def synthese_finale(liste_complete_resultats):
    """Génère le rapport final"""
    
    # On transforme la liste technique en texte pour le prompt
    donnees_pour_synthese = json.dumps(liste_complete_resultats, ensure_ascii=False)
    
    prompt = f"""
    Rôle : Juge impartial.
    Données : Voici les biais détectés dans un texte : {donnees_pour_synthese}
    
    Tâche : Rédige un avis de fiabilité court et percutant.
    
    Format de sortie (Markdown) :
    1. Titre : "VERDICT DE L'AGENT"
    2. Score de fiabilité / 100.
    3. Analyse : Résume pourquoi le texte est biaisé ou fiable.
    4. Conseil : Que doit faire le lecteur ?
    """

    try:
        response = requests.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        })
        return response.json()['response']
    except Exception:
        return "Erreur de synthèse."

# --- MAIN ---

def lancer_agent(texte):
    print(f"\n🤖 Analyse en cours sur : \"{texte[:60]}...\"\n")
    
    tous_les_biais_detectes = [] # Liste plate pour l'affichage final
    resultats_par_cat = {}      # Dictionnaire pour la synthèse

    # 1. SCAN PAR CATÉGORIE
    for categorie, liste in CATEGORIES_BIAIS_ESSENTIELS.items():
        print(f"   Scanning : {categorie}...", end=" ", flush=True)
        
        resultat = analyse_categorie(categorie, liste, texte)
        biais = resultat.get('biais_trouves', [])
        
        if biais:
            print(f"⚠️  {len(biais)} trouvé(s)")
            tous_les_biais_detectes.extend(biais)
            resultats_par_cat[categorie] = biais
        else:
            print("✅ RAS")

    # 2. AFFICHAGE DE LA LISTE DÉTAILLÉE
    if tous_les_biais_detectes:
        print("\n" + "="*60)
        print("📋 DÉTAIL DES BIAIS DÉTECTÉS")
        print("="*60)
        for b in tous_les_biais_detectes:
            print(f"\n🔴 BIAIS : {b['nom']}")
            print(f"   📝 Citation : \"{b['citation']}\"")
            print(f"   💡 Explication : {b['explication']}")
            print(f"   🔥 Gravité : {b['gravite']}")
            print("-" * 30)
    else:
        print("\n✅ Aucun biais majeur détecté dans le détail.")

    # 3. SYNTHÈSE
    print("\n" + "="*60)
    print("🧠 SYNTHÈSE INTELLIGENTE")
    print("="*60)
    rapport = synthese_finale(tous_les_biais_detectes)
    print(rapport)

# --- TEST ---
texte_demo = """
Au début de l'invasion de l'Ukraine, un pilote de chasse ukrainien anonyme aurait abattu à lui seul 6 avions russes en une journée. L'histoire a été relayée par des comptes officiels et des médias majeurs.
"""
if __name__ == "__main__":
    lancer_agent(texte_demo)