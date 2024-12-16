from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from graph.models.Task import Task
from tools.llm import llm

load_dotenv()

structured_prompt = llm.with_structured_output(Task)
prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Tu dois ici construire une tâche en rapport au contexte.
            Voici le contexte : \n{context}.\n
            Voici l'identifiant de la tâche : {id}.
            """,
        )
    ]
)

create_task_for_delete_chain = prompt_template | structured_prompt
