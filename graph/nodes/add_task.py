import json
from time import sleep
from typing import Any, Dict

from langchain_core.documents import Document
from graph.models.GraphState import GraphState
from tools.get_retriever import embeddings, index_name, mongo_collection, mongo_vector_store


def add_task(state: GraphState) -> Dict[str, Any]:
    """
    Ajoute une tâche au store vectoriel Mongo.

    :param state: Un objet GraphState contenant au moins un attribut 'task'.
    :return: Un dictionnaire contenant un message de succès et la tâche ajoutée.
    """
    task = state["task"]

    # Extraire les données de la tâche sous forme de dictionnaire
    # et exclure le champ 'type' si présent
    task_data = {k: v for k, v in vars(task).items() if k != "type"}

    # Convertir en JSON
    json_task = json.dumps(task_data)

    # Créer un Document et l'ajouter à la base vectorielle
    documents = [Document(page_content=json_task)]
    mongo_vector_store.from_documents(
        documents=documents,
        embedding=embeddings,
        collection=mongo_collection,
        index_name=index_name,
    )

    sleep(2)
    # Retourner la réponse
    return {
        "message": "Tache ajoutée avec succès.",
        "task": task
    }
