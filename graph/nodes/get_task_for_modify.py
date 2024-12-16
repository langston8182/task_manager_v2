from typing import Any, Dict

from graph.chains.get_task_for_modify import create_task_for_modify_chain
from graph.chains.rag_retrieval import retrieval_chain
from graph.models.GraphState import GraphState


def get_task_for_modify(state: GraphState) -> Dict[str, Any]:
    question = state["question"]
    connected_user = state["connected_user"]
    result = retrieval_chain.invoke(
        input={"input": f"{question}\nJe m'appelle {connected_user}"}
    )
    content = result["context"][0].page_content
    id = result["context"][0].metadata["_id"]
    task = create_task_for_modify_chain.invoke({"context": content, "id": id})

    return {"task": task}
