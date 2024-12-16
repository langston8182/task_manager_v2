from typing import TypedDict

from graph.models.Task import Task
from graph.models.UserRequest import UserRequest


class GraphState(TypedDict):
    connected_user: str
    question: str
    user_request: UserRequest
    task: Task
    ui_response: str
