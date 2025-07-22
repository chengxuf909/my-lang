from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
from langchain.chat_models import init_chat_model

model = init_chat_model("gpt-4.1-mini", model_provider="openai")

from langchain_core.messages import HumanMessage, SystemMessage


def main():
    messages = [
        SystemMessage("Translate the following from English into Italian"),
        HumanMessage("hi!"),
    ]
    resp = model.invoke(messages)
    print(resp)
    

if __name__ == "__main__":
    main()
    
