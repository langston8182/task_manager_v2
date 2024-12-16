from langchain_openai import ChatOpenAI

from tools.get_secrets import get_key_value

llm = ChatOpenAI(temperature=0, model="gpt-4o-mini", api_key=get_key_value("OPENAI_API_KEY"))