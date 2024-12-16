from typing import Any, Dict

from graph.chains.rag_retrieval import retrieval_chain
from graph.models.GraphState import GraphState
from tools.get_retriever import retriever


def get_all_tasks(state: GraphState) -> Dict[str, Any]:
    responsable = state["task"].responsable
    question = f"Quelles sont toutes les taches de {responsable} ?"
    result = retrieval_chain.invoke(input={"input": f"{question}"})

    return {"ui_response": result["answer"]}
