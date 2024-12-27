from asyncio import create_task

from dotenv import load_dotenv
from langgraph.constants import END
from langgraph.graph import StateGraph

from graph.consts import (
    ADD_TASK,
    CREATE_TASK,
    DELETE_TASK,
    GET_ALL_TASKS,
    GET_TASK_FOR_DELETE,
    GET_TASK_FOR_MODIFY,
    GET_TASKS,
    RETRIEVE_ACTION_TYPE,
)
from graph.models.GraphState import GraphState
from graph.nodes.add_task import add_task
from graph.nodes.create_task import create_task
from graph.nodes.delete_task import delete_task
from graph.nodes.get_all_tasks import get_all_tasks
from graph.nodes.get_task_for_delete import get_tasks_for_delete
from graph.nodes.get_task_for_modify import get_task_for_modify
from graph.nodes.get_tasks import get_tasks
from graph.nodes.retrieve_action_type import retrieve_action_type

load_dotenv()


def decide_to_node_on_modification(state: GraphState) -> str:
    """
    Détermine le prochain nœud à visiter dans le graphe
    lors d'une modification de tâche (supprimer ou modifier).

    :param state: L'état du graphe contenant 'user_request'.
    :return: Le nom du prochain nœud.
    """
    user_request = state.get("user_request")
    if not user_request or not hasattr(user_request, "type"):
        return GET_ALL_TASKS

    match user_request.type:
        case "modifier":
            return CREATE_TASK
        case "supprimer":
            return GET_ALL_TASKS
        case _:
            return GET_ALL_TASKS


def decide_to_node_on_startup(state: GraphState) -> str:
    """
    Détermine le prochain nœud à visiter dans le graphe
    au démarrage, en fonction du type d'action souhaitée par l'utilisateur.

    :param state: L'état du graphe contenant 'user_request'.
    :return: Le nom du prochain nœud.
    """
    user_request = state.get("user_request")
    if not user_request or not hasattr(user_request, "type"):
        return GET_TASKS

    match user_request.type:
        case "ajouter":
            return CREATE_TASK
        case "modifier":
            return GET_TASK_FOR_MODIFY
        case "consulter":
            return GET_TASKS
        case "supprimer":
            return GET_TASK_FOR_DELETE
        case _:
            return GET_TASKS


# Création du workflow
workflow = StateGraph(GraphState)

# Ajout des nœuds
workflow.add_node(RETRIEVE_ACTION_TYPE, retrieve_action_type)
workflow.add_node(ADD_TASK, add_task)
workflow.add_node(GET_TASKS, get_tasks)
workflow.add_node(GET_ALL_TASKS, get_all_tasks)
workflow.add_node(CREATE_TASK, create_task)
workflow.add_node(GET_TASK_FOR_DELETE, get_tasks_for_delete)
workflow.add_node(DELETE_TASK, delete_task)
workflow.add_node(GET_TASK_FOR_MODIFY, get_task_for_modify)

# Définition du point d'entrée
workflow.set_entry_point(RETRIEVE_ACTION_TYPE)

# Ajout des conditions de transitions
workflow.add_conditional_edges(
    RETRIEVE_ACTION_TYPE,
    decide_to_node_on_startup,
    {
        CREATE_TASK: CREATE_TASK,
        GET_TASKS: GET_TASKS,
        GET_TASK_FOR_DELETE: GET_TASK_FOR_DELETE,
        GET_TASK_FOR_MODIFY: GET_TASK_FOR_MODIFY,
    },
)

workflow.add_conditional_edges(
    DELETE_TASK,
    decide_to_node_on_modification,
    {
        CREATE_TASK: CREATE_TASK,
        GET_ALL_TASKS: GET_ALL_TASKS,
    },
)

# Ajout des transitions simples
workflow.add_edge(GET_TASK_FOR_DELETE, DELETE_TASK)
workflow.add_edge(GET_TASK_FOR_MODIFY, DELETE_TASK)
workflow.add_edge(CREATE_TASK, ADD_TASK)
workflow.add_edge(ADD_TASK, GET_ALL_TASKS)
workflow.add_edge(GET_ALL_TASKS, END)
workflow.add_edge(GET_TASKS, END)

# Compilation et affichage du graphe
app = workflow.compile()
print(app.get_graph().draw_mermaid())
