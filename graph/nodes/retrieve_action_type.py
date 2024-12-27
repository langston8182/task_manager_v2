from typing import Any, Dict

from graph.chains.retrieve_action_type import retrieval_action_type_chain
from graph.models.GraphState import GraphState


def retrieve_action_type(state: GraphState) -> Dict[str, Any]:
    """
    Détermine le type d'action à effectuer en fonction d'une question et d'un utilisateur connecté,
    en invoquant la chaîne `retrieval_action_type_chain`.

    :param state: Un objet GraphState contenant au moins 'question' et 'connected_user'.
    :return: Un dictionnaire contenant l'objet 'user_request'.
    """
    question = state.get("question")
    if question is None:
        return {"user_request": None, "error": "Aucune question fournie dans l'état."}

    connected_user = state.get("connected_user")
    if connected_user is None:
        return {"user_request": None, "error": "Aucun utilisateur connecté fourni dans l'état."}

    user_request = retrieval_action_type_chain.invoke(
        {"question": question, "connected_user": connected_user}
    )

    return {"user_request": user_request}
