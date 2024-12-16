import datetime

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from graph.models.Task import Task
from tools.get_secrets import get_key_value
from tools.llm import llm

load_dotenv()

structured_prompt = llm.with_structured_output(Task)
prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Heure actuelle : {current_time}
            Tu dois ici construire une tâche en rapport avec la requête de l'utilisateur.
            La question est {question}.
            Voici le responsable de la tâche : {responsable}.
            """,
        )
    ]
).partial(current_time=datetime.datetime.now().isoformat())

create_task_chain = prompt_template | structured_prompt
