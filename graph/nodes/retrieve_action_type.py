from typing import Any, Dict

from graph.chains.retrieve_action_type import retrieval_action_type_chain
from graph.models.GraphState import GraphState


def retrieve_action_type(state: GraphState) -> Dict[str, Any]:
    question = state["question"]
    connected_user = state["connected_user"]
    user_request = retrieval_action_type_chain.invoke(
        {"question": question, "connected_user": connected_user}
    )
    return {"user_request": user_request}
