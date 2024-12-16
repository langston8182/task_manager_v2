from dotenv import load_dotenv

from graph.graph import app
from tools.env_manager import load_aws_env

load_aws_env()
load_dotenv()

def run_llm(question: str, username: str) -> str:
    result = app.invoke(
        input = {"question": question, "connected_user": username}
    )
    return result["ui_response"]

if __name__ == "__main__":
    #run_llm(question="Je dois réparer la voiture pour demain")
    run_llm(question="Supprime la tache ou virginie doit aller chez le medecin", username="Cyril")
    #run_llm(question="Virginie dois faire la vaisselle dans 2 jours", username="Cyril")
    #run_llm(question="Je dois mettre la poubelle dans 2 jours", username="Cyril")
    #run_llm(question="Quelles sont toutes mes taches ?", username="Cyril")
    #run_llm(question="Supprime ma tâche ou je dois réparer la voiture", username="Cyril")
    #run_llm(question="Modifie la tache ou je dois réparer la voiture pour la faire dans 30 jours et assigne la tache a Virginie", username="Cyril")
    #print()
