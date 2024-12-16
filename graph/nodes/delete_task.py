from typing import Any, Dict

from bson import ObjectId

from graph.models.GraphState import GraphState
from tools.get_retriever import mongo_collection


def delete_task(state: GraphState) -> Dict[str, Any]:
    task_id = state["task"].id
    mongo_collection.delete_one({"_id": ObjectId(task_id)})
