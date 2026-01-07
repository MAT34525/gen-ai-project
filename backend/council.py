"""3-stage LLM Council orchestration."""

from typing import List, Dict, Any, Tuple
from openrouter import query_models_parallel, query_model
from config import COUNCIL_BASE_MODELS
from models import Role, ModelType

class Council() :

    def __init__(self) :

        self.models = COUNCIL_BASE_MODELS

        for model in self.models:
            model.pull()

            if model.model_type == ModelType.CUSTOM :
                model.create()
        
        self.chairman = self.models[0]
        self.models = self.models[1:]

        assert self.chairman.model_role == Role.CHAIRMAN

    async def stage1_collect_responses(self, user_query: str) -> List[Dict[str, Any]]:

        messages = [{"role": "user", "content": user_query}]

        # Query all models in parallel
        responses = await query_models_parallel(self.models, messages)

        # Format results
        stage1_results = []
        for model, response in responses.items():
            if response is not None:  # Only include successful responses
                stage1_results.append({
                    "model": model,
                    "response": response.get('content', '')
                })

        return stage1_results


    async def stage2_collect_rankings(
        self,
        user_query: str,
        stage1_results: List[Dict[str, Any]]
    ) -> Tuple[List[Dict[str, Any]], Dict[str, str]]:

        # Create anonymized labels for responses (Response A, Response B, etc.)
        labels = [chr(65 + i) for i in range(len(stage1_results))]  # A, B, C, ...

        # Create mapping from label to model name
        label_to_model = {
            f"Response {label}": result['model']
            for label, result in zip(labels, stage1_results)
        }

        # Build the ranking prompt
        responses_text = "\n\n".join([
            f"Response {label}:\n{result['response']}"
            for label, result in zip(labels, stage1_results)
        ])

        ranking_prompt = f"""Rôle: Juge impartial
    Tu dois évaluer les différentes réponses des modèles d'IA pour la détection des biais cognitif dans une phrase :

    Phrase à analyser : {user_query}

    Voici les réponses des différents modèles (anonymized):

    {responses_text}

    Tes tâches:
    1. En premier, évalue chaques réponses individuellement. Pour chaques réponses, explique ce qui est bien fait et ce qui est est mal fait.
    2. Ensuite, à la fin de chaques réponses, donne une note finale.

    IMPORTANT: La note finale DOIT être EXACTEMENT formattée de cette manière :

    - Commencez par la ligne « CLASSEMENT FINAL : » (en majuscules, avec deux points)
    - Listez ensuite les réponses de la meilleure à la moins bonne sous forme de liste numérotée.
    - Chaque ligne doit contenir : un numéro, un point, un espace, puis UNIQUEMENT le libellé de la réponse (par exemple, « 1. Réponse A »).
    - N'ajoutez aucun autre texte ni explication dans la section du classement.

    Exemple de format correct pour votre réponse COMPLÈTE :

    La réponse A fournit des détails pertinents sur X, mais omet Y…
    La réponse B est exacte, mais manque de profondeur sur Z…
    La réponse C offre la réponse la plus complète…

    NOTE FINALE:
    1. Réponse C
    2. Réponse A
    3. Réponse B
    
    Veuillez maintenant fournir votre évaluation et votre classement :"""

        messages = [{"role": "user", "content": ranking_prompt}]

        # Get rankings from all council models in parallel
        responses = await query_models_parallel(self.models, messages)

        # Format results
        stage2_results = []
        for model, response in responses.items():
            if response is not None:
                full_text = response.get('content', '')
                parsed = Council.parse_ranking_from_text(full_text)
                stage2_results.append({
                    "model": model,
                    "ranking": full_text,
                    "parsed_ranking": parsed
                })

        return stage2_results, label_to_model


    async def stage3_synthesize_final(
        self,
        user_query: str,
        stage1_results: List[Dict[str, Any]],
        stage2_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:

        # Build comprehensive context for chairman
        stage1_text = "\n\n".join([
            f"Model: {result['model']}\nResponse: {result['response']}"
            for result in stage1_results
        ])

        stage2_text = "\n\n".join([
            f"Model: {result['model']}\nRanking: {result['ranking']}"
            for result in stage2_results
        ])

        chairman_prompt = f"""Vous êtes le président d'un conseil de master en droit. Plusieurs modèles d'IA ont analyser les biais cognitifs dans une phrase, puis ont classé leurs réponses respectives.

    Phrase à analyser : {user_query}

    Etape 1 - Réponse individuelle :
    {stage1_text}

    Etape 2 - Classement des pairs :
    {stage2_text}
    
    Votre rôle de président est de synthétiser toutes ces informations afin de fournir une réponse unique, complète et précise à la question initiale de l'utilisateur. Prenez en compte :

    - Les réponses individuelles et les enseignements qu'elles apportent
    - Les classements par les pairs et ce qu'ils révèlent sur la qualité des réponses
    - Les éventuels points de convergence ou de divergence
    
    Fournir une réponse finale claire et bien argumentée qui représente la sagesse collective du conseil :"""

        messages = [{"role": "user", "content": chairman_prompt}]

        # Query the chairman model
        response = await query_model(self.chairman, messages)

        if response is None:
            # Fallback if chairman fails
            return {
                "model": self.chairman.model_name,
                "response": "Error: Impossible de générer la synthèse finale."
            }

        return {
            "model": self.chairman.model_name,
            "response": response.get('content', '')
        }


    def parse_ranking_from_text(ranking_text: str) -> List[str]:
        """
        Parse the FINAL RANKING section from the model's response.

        Args:
            ranking_text: The full text response from the model

        Returns:
            List of response labels in ranked order
        """
        import re

        # Look for "FINAL RANKING:" section
        if "FINAL RANKING:" in ranking_text:
            # Extract everything after "FINAL RANKING:"
            parts = ranking_text.split("FINAL RANKING:")
            if len(parts) >= 2:
                ranking_section = parts[1]
                # Try to extract numbered list format (e.g., "1. Response A")
                # This pattern looks for: number, period, optional space, "Response X"
                numbered_matches = re.findall(r'\d+\.\s*Response [A-Z]', ranking_section)
                if numbered_matches:
                    # Extract just the "Response X" part
                    return [re.search(r'Response [A-Z]', m).group() for m in numbered_matches]

                # Fallback: Extract all "Response X" patterns in order
                matches = re.findall(r'Response [A-Z]', ranking_section)
                return matches

        # Fallback: try to find any "Response X" patterns in order
        matches = re.findall(r'Response [A-Z]', ranking_text)
        return matches


    def calculate_aggregate_rankings(
        self,
        stage2_results: List[Dict[str, Any]],
        label_to_model: Dict[str, str]
    ) -> List[Dict[str, Any]]:
        from collections import defaultdict

        # Track positions for each model
        model_positions = defaultdict(list)

        for ranking in stage2_results:
            ranking_text = ranking['ranking']

            # Parse the ranking from the structured format
            parsed_ranking = Council.parse_ranking_from_text(ranking_text)

            for position, label in enumerate(parsed_ranking, start=1):
                if label in label_to_model:
                    model_name = label_to_model[label]
                    model_positions[model_name].append(position)

        # Calculate average position for each model
        aggregate = []
        for model, positions in model_positions.items():
            if positions:
                avg_rank = sum(positions) / len(positions)
                aggregate.append({
                    "model": model,
                    "average_rank": round(avg_rank, 2),
                    "rankings_count": len(positions)
                })

        # Sort by average rank (lower is better)
        aggregate.sort(key=lambda x: x['average_rank'])

        return aggregate


    async def generate_conversation_title(self, user_query: str) -> str:
        title_prompt = f"""Créez un titre très court (3 à 5 mots maximum) qui résume la phrase suivante.
    Le titre doit être concis et descriptif. N'utilisez ni guillemets ni ponctuation.

    Phrase: {user_query}

    Title:"""

        messages = [{"role": "user", "content": title_prompt}]

        # Use gemini-2.5-flash for title generation (fast and cheap)
        response = await query_model(self.models[0], messages)

        if response is None:
            # Fallback to a generic title
            return "Nouvelle conversation"

        title = response.get('message.content', 'Nouvelle conversation').strip()

        # Clean up the title - remove quotes, limit length
        title = title.strip('"\'')

        # Truncate if too long
        if len(title) > 50:
            title = title[:47] + "..."

        return title


    async def run_full_council(self, user_query: str) -> Tuple[List, List, Dict, Dict]:
        # Stage 1: Collect individual responses
        stage1_results = await self.stage1_collect_responses(user_query)

        # If no models responded successfully, return error
        if not stage1_results:
            return [], [], {
                "model": "error",
                "response": "Aucun modèle n'a réussi à répondre. Veuillez réessayer."
            }, {}

        # Stage 2: Collect rankings
        stage2_results, label_to_model = await self.stage2_collect_rankings(user_query, stage1_results)

        # Calculate aggregate rankings
        aggregate_rankings = self.calculate_aggregate_rankings(stage2_results, label_to_model)

        # Stage 3: Synthesize final answer
        stage3_result = await self.stage3_synthesize_final(
            user_query,
            stage1_results,
            stage2_results
        )

        # Prepare metadata
        metadata = {
            "label_to_model": label_to_model,
            "aggregate_rankings": aggregate_rankings
        }

        return stage1_results, stage2_results, stage3_result, metadata
