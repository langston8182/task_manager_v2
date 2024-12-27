from typing import Any, Dict

from graph.chains.rag_retrieval import retrieval_chain
from graph.models.GraphState import GraphState
from tools.get_retriever import retriever


def get_tasks(state: GraphState) -> Dict[str, Any]:
    """
    Récupère des tâches en fonction d'une question et d'un utilisateur connecté,
    en invoquant une chaîne de récupération de documents.

    :param state: Un objet GraphState contenant au moins 'question' et 'connected_user'.
    :return: Un dictionnaire contenant la réponse utilisateur (ui_response).
    """
    question = state.get("question")
    if question is None:
        return {"ui_response": "Aucune question fournie."}

    connected_user = state.get("connected_user")
    if connected_user is None:
        return {"ui_response": "Aucun utilisateur connecté spécifié."}

    # Invocation de la chaîne de récupération
    result = retrieval_chain.invoke(
        input={"input": f"{question}\nJe m'appelle {connected_user}"}
    )

    answer = result.get("answer", "Aucune réponse disponible.")
    return {"ui_response": answer}
