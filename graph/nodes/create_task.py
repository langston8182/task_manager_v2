from typing import Any, Dict

from graph.chains.create_task import create_task_chain
from graph.models.GraphState import GraphState


def create_task(state: GraphState) -> Dict[str, Any]:
    """
    Crée une tâche à partir de l'état fourni en utilisant create_task_chain.

    :param state: Un objet GraphState contenant au moins 'user_request' et 'question'.
    :return: Un dictionnaire contenant la tâche créée.
    """
    responsable = getattr(state["user_request"], "responsable", None)
    question = state.get("question")

    # Vérification optionnelle si les valeurs sont définies
    if question is None or responsable is None:
        raise ValueError("La 'question' et le 'responsable' doivent être fournis dans l'état.")

    task = create_task_chain.invoke({"question": question, "responsable": responsable})

    return {"task": task}
