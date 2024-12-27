from typing import Any, Dict

from graph.chains.get_task_for_delete import create_task_for_delete_chain
from graph.chains.rag_retrieval import retrieval_chain
from graph.models.GraphState import GraphState
from tools.get_retriever import retriever


def get_tasks_for_delete(state: GraphState) -> Dict[str, Any]:
    """
    Récupère une tâche à supprimer en fonction de la question et de l'utilisateur responsable,
    via une chaîne de récupération puis la crée via `create_task_for_delete_chain`.

    :param state: Un objet GraphState contenant au moins 'question', 'user_request.responsable'
                  et 'connected_user'.
    :return: Un dictionnaire contenant la tâche à supprimer.
    """

    question = state.get("question")
    if question is None:
        return {"task": None, "error": "Aucune question fournie dans l'état."}

    user_request = state.get("user_request")
    if not user_request or not hasattr(user_request, "responsable"):
        return {"task": None, "error": "Aucun responsable spécifié dans l'état."}

    responsable = user_request.responsable
    connected_user = state.get("connected_user")  # Si nécessaire par la suite

    # Invocation de la chaîne de récupération
    result = retrieval_chain.invoke(
        input={"input": f"{question}\nJe m'appelle {responsable}"}
    )

    context = result.get("context")
    if not context or len(context) == 0:
        return {"task": None, "error": "Aucun contexte retourné par la chaîne de récupération."}

    # On suppose ici que la chaîne retourne toujours au moins un élément dans le contexte
    first_context = context[0]
    content = getattr(first_context, "page_content", None)
    metadata = getattr(first_context, "metadata", {})
    task_id = metadata.get("_id")

    if not content or not task_id:
        return {"task": None, "error": "Les informations nécessaires (contenu ou ID) n'ont pas pu être récupérées."}

    # Création de la tâche à supprimer
    task = create_task_for_delete_chain.invoke({"context": content, "id": task_id})

    return {"task": task}
