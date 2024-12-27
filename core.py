from tools.env_manager import load_aws_env
load_aws_env()
from dotenv import load_dotenv

from graph.graph import app
import logging

# Chargement des environnements et configuration des logs
load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def run_llm(question: str, username: str) -> str:
    """
        Exécute la fonction LLM avec une question et un utilisateur donné.

        Args:
            question (str): La question à poser au modèle LLM.
            username (str): Le nom de l'utilisateur connecté.

        Returns:
            str: La réponse formattée depuis le LLM.
        """
    logging.info("Invocation de run_llm avec question='%s' et username='%s'", question, username)
    try:
        if not question.strip():
            raise ValueError("La question ne peut pas être vide.")

        if not username.strip():
            raise ValueError("Le nom d'utilisateur ne peut pas être vide.")

        result = app.invoke(input={"question": question, "connected_user": username})
        response = result.get("ui_response", "Aucune réponse trouvée.")
        logging.info("Réponse obtenue: %s", response)
        return response
    except ValueError as ve:
        logging.error("Validation Error: %s", str(ve))
        return str(ve)
    except Exception as e:
        logging.error("Erreur lors de l'exécution de run_llm: %s", str(e))
        return "Une erreur est survenue lors du traitement de votre demande."


if __name__ == "__main__":
    # run_llm(question="Je dois réparer la voiture pour demain")
    run_llm(
        question="Quelles sont les taches de virginie ?",
        username="Cyril",
    )
    # run_llm(question="Virginie dois faire la vaisselle dans 2 jours", username="Cyril")
    # run_llm(question="Je dois mettre la poubelle dans 2 jours", username="Cyril")
    # run_llm(question="Quelles sont toutes mes taches ?", username="Cyril")
    # run_llm(question="Supprime ma tâche ou je dois réparer la voiture", username="Cyril")
    # run_llm(question="Modifie la tache ou je dois réparer la voiture pour la faire dans 30 jours et assigne la tache a Virginie", username="Cyril")
    # print()
