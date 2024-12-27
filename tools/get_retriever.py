import os
from dotenv import load_dotenv
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings
from pymongo import MongoClient
from tools.get_secrets import get_key_value

# Charger les variables d'environnement
load_dotenv()

# Initialisation des embeddings OpenAI
embeddings = OpenAIEmbeddings(api_key=get_key_value("OPENAI_API_KEY"))

# Récupération des paramètres MongoDB
mongo_connection_str = get_key_value("ATLAS_CONNECTION_STR")
db_name = os.environ.get("ATLAS_MONGODB_DB")
collection_name = os.environ.get("ATLAS_COLLECTION_NAME")
index_name = os.environ.get("ATLAS_INDEX_NAME")

# Validation des paramètres requis
if not all([mongo_connection_str, db_name, collection_name, index_name]):
    raise ValueError("Tous les paramètres MongoDB nécessaires ne sont pas définis dans les variables d'environnement ou les secrets.")

# Initialisation du client MongoDB
try:
    cluster = MongoClient(mongo_connection_str)
    mongo_collection = cluster[db_name][collection_name]
except Exception as e:
    raise ConnectionError(f"Erreur lors de la connexion à MongoDB : {str(e)}")

# Création de l'instance MongoDBAtlasVectorSearch
try:
    mongo_vector_store = MongoDBAtlasVectorSearch(
        connection_string=mongo_connection_str,
        database_name=db_name,
        collection=mongo_collection,
        embedding=embeddings,
        index_name=index_name,
    )
except Exception as e:
    raise RuntimeError(f"Erreur lors de l'initialisation de MongoDBAtlasVectorSearch : {str(e)}")

# Configuration du récupérateur avec des paramètres ajustables
retriever = mongo_vector_store.as_retriever(search_kwargs={"k": 50})
