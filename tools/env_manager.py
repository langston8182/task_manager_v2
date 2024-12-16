import os

from tools.get_secrets import get_key_value


def load_aws_env():
    os.environ["LANGCHAIN_API_KEY"] = get_key_value("LANGCHAIN_API_KEY")
