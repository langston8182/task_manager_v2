import json
from time import sleep
from typing import Any, Dict

from langchain_core.documents import Document

from graph.models.GraphState import GraphState
from tools.get_retriever import (embeddings, index_name, mongo_collection,
                                 mongo_vector_store)


def add_task(state: GraphState) -> Dict[str, Any]:
    task = state["task"]
    task_to_add = task.copy().__dict__
    task_to_add.pop("type")
    json_task = json.dumps(task_to_add)
    documents = [Document(page_content=json_task)]
    mongo_vector_store.from_documents(
        documents=documents,
        embedding=embeddings,
        collection=mongo_collection,
        index_name=index_name,
    )

    task_json = json.dumps(task.__dict__)

    sleep(2)
    return {"message": "Tache ajoutée avec succès.", "task": task}
