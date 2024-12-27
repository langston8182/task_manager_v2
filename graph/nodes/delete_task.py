from typing import Any, Dict

from bson import ObjectId

from graph.models.GraphState import GraphState
from tools.get_retriever import mongo_collection


def delete_task(state: GraphState) -> Dict[str, Any]:
    """
    Supprime une tâche identifiée par son ID depuis la base de données MongoDB.

    :param state: Un objet GraphState contenant au moins un champ 'task' avec un 'id'.
    :return: Un dictionnaire indiquant le succès ou l'échec de l'opération.
    """
    task = state.get("task")
    if not task or not hasattr(task, "id"):
        return {"message": "Échec : Aucun ID de tâche fourni."}

    task_id = getattr(task, "id", None)
    if not task_id:
        return {"message": "Échec : ID de tâche invalide."}

    # Suppression de la tâche
    result = mongo_collection.delete_one({"_id": ObjectId(task_id)})

    if result.deleted_count == 1:
        return {"message": "Tâche supprimée avec succès."}
    else:
        return {"message": "Aucune tâche trouvée avec cet ID."}
