import datetime

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from graph.models.Task import Task
from graph.models.UserRequest import UserRequest
from tools.llm import llm

load_dotenv()

structured_prompt = llm.with_structured_output(UserRequest)
actor_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Tu es perspicace et tu as un raisonnement logique, dis moi quel type d'action tu veux effectuer en fonction de la question de l'utilisateur.\n
            Est ce que selon toi il s'agit d'une action de type "ajouter", "supprimer", "modifier" ou "consulter" ?\n
            - Ajouter : pour ajouter une tâche dans la base de données (exemple : "Je dois repasser le linge pour demain.")
            - Modifier : pour modifier une tâche dans la base de données (exemple : "Modifie la tâche de Virginie ...")
            """,
        ),
        (
            "human",
            "Question de l'utilisateur : {question}\nje m'appelle {connected_user}.",
        ),
    ]
)

retrieval_action_type_chain = actor_prompt_template | structured_prompt
