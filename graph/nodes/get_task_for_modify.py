from typing import Any, Dict

from graph.chains.get_task_for_modify import create_task_for_modify_chain
from graph.chains.rag_retrieval import retrieval_chain
from graph.models.GraphState import GraphState


def get_task_for_modify(state: GraphState) -> Dict[str, Any]:
    """
    Récupère une tâche à modifier à partir de la question et de l'utilisateur connecté,
    en utilisant une chaîne de récupération, puis génère la tâche modifiable via `create_task_for_modify_chain`.

    :param state: Un objet GraphState contenant au moins 'question' et 'connected_user'.
    :return: Un dictionnaire contenant la tâche à modifier ou un message d'erreur.
    """

    question = state.get("question")
    if question is None:
        return {"task": None, "error": "Aucune question fournie dans l'état."}

    connected_user = state.get("connected_user")
    if connected_user is None:
        return {"task": None, "error": "Aucun utilisateur connecté fourni dans l'état."}

    # Invocation de la chaîne de récupération
    result = retrieval_chain.invoke(
        input={"input": f"{question}\nJe m'appelle {connected_user}"}
    )

    context = result.get("context")
    if not context or len(context) == 0:
        return {"task": None, "error": "Aucun contexte retourné par la chaîne de récupération."}

    first_context = context[0]
    content = getattr(first_context, "page_content", None)
    metadata = getattr(first_context, "metadata", {})
    task_id = metadata.get("_id")

    if not content or not task_id:
        return {"task": None, "error": "Informations nécessaires (contenu ou ID) manquantes."}

    # Création de la tâche à modifier
    task = create_task_for_modify_chain.invoke({"context": content, "id": task_id})

    return {"task": task}
