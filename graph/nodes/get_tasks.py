from typing import Any, Dict

from graph.chains.rag_retrieval import retrieval_chain
from graph.models.GraphState import GraphState
from tools.get_retriever import retriever


def get_tasks(state: GraphState) -> Dict[str, Any]:
    question = state["question"]
    connected_user = state["connected_user"]
    result = retrieval_chain.invoke(
        input={"input": f"{question}\nJe m'appelle {connected_user}"}
    )

    return {"ui_response": result["answer"]}
