import os

from dotenv import load_dotenv
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings
from pymongo import MongoClient

from tools.get_secrets import get_key_value

load_dotenv()

embeddings = OpenAIEmbeddings(api_key=get_key_value("OPENAI_API_KEY"))
mongo_connection_str = get_key_value("ATLAS_CONNECTION_STR")
db_name = os.environ.get("ATLAS_MONGODB_DB")
collection_name = os.environ.get("ATLAS_COLLECTION_NAME")
index_name = os.environ.get("ATLAS_INDEX_NAME")

cluster = MongoClient(mongo_connection_str)
mongo_collection = cluster[db_name][collection_name]

mongo_vector_store = MongoDBAtlasVectorSearch(
    connection_string=mongo_connection_str,
    database_name=db_name,
    collection=mongo_collection,
    embedding=embeddings,
    index_name=index_name,
)
retriever = mongo_vector_store.as_retriever(search_kwargs={"k": 50})
