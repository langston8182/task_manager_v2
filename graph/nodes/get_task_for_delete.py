from typing import Any, Dict

from graph.chains.get_task_for_delete import create_task_for_delete_chain
from graph.chains.rag_retrieval import retrieval_chain
from graph.models.GraphState import GraphState
from tools.get_retriever import retriever


def get_tasks_for_delete(state: GraphState) -> Dict[str, Any]:
    question = state["question"]
    responsable = state["user_request"].responsable
    connected_user = state["connected_user"]
    result = retrieval_chain.invoke(
        input={"input": f"{question}\nJe m'appelle {responsable}"}
    )
    content = result["context"][0].page_content
    id = result["context"][0].metadata["_id"]
    task = create_task_for_delete_chain.invoke({"context": content, "id": id})

    return {"task": task}
