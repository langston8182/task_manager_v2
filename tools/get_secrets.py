import json
import os

import boto3

secrets_cache = None


def get_secret(secret_name, region_name):
    """
    Récupérer les clés depuis AWS Secrets Manager.
    """
    # Créer un client AWS Secrets Manager
    global secrets_cache
    if secrets_cache is not None:
        return secrets_cache
    client = boto3.client(
        "secretsmanager",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=region_name,
    )

    try:
        # Récupérer le secret
        response = client.get_secret_value(SecretId=secret_name)
        # Si le secret est un JSON, le décoder
        secret = response["SecretString"]
        secrets_cache = json.loads(secret)
        return secrets_cache
    except Exception as e:
        print(f"Erreur lors de la récupération du secret : {e}")
        return None


def get_key_value(key_name: str) -> str:
    secrets = get_secret("task_manager_secret", "eu-west-3")
    if secrets:
        return secrets[key_name]


# Exemple d'utilisation
if __name__ == "__main__":
    region = "eu-west-3"
    secret_name = "task_manager_secret"  # Nom du secret
    secrets = get_secret(secret_name, region)
    open_api_key = get_key_value("OPEN_API_KEY")
    print("OPEN_API_KEY :", open_api_key)

    if secrets:
        print("Clés récupérées :", secrets)
        print("OPEN_API_KEY :", secrets["OPEN_API_KEY"])
        print("ATLAS_CONNECTION_STR :", secrets["ATLAS_CONNECTION_STR"])
