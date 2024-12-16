from typing import Any, Dict

from graph.chains.create_task import create_task_chain
from graph.models.GraphState import GraphState


def create_task(state: GraphState) -> Dict[str, Any]:
    responsable = state["user_request"].responsable
    question = state["question"]
    task = create_task_chain.invoke({"question": question, "responsable": responsable})

    return {"task": task}
