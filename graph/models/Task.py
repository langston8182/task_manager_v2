from pydantic.v1 import BaseModel, Field


class Task(BaseModel):
    """
    Permet de construire une tâche a réaliser en fonction de la question posée
    """

    id: str = Field(
        description="identifiant de la tâche, peut etre None si la tâche n'existe pas"
    )
    content: str = Field(description="contenu de la tâche")
    due_date: str = Field(description="date limite de la tâche au format ISO")
    responsable: str = Field(description="responsable de la tâche")
    type: str = Field(
        description="Type d'action à effectuer : ajouter, modifier, supprimer, consulter"
    )
