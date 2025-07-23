from dotenv import load_dotenv
import os
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage

from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langserve import add_routes

load_dotenv()
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print(OPENAI_BASE_URL)
print(OPENAI_API_KEY)
# model = init_chat_model("gpt-4.1-mini", model_provider="openai")

# 1. Create prompt template
system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{text}')
])

# 2. Create model
model = ChatOpenAI()

# 3. Create parser
parser = StrOutputParser()

# 4. Create chain
chain = prompt_template | model | parser


app = FastAPI(
  title="LangChain Server",
  version="1.0",
  description="A simple API server using LangChain's Runnable interfaces",
)

# 为根路径添加一个 GET 端点
@app.get("/")
async def redirect_root_to_docs():
    return {"message": "Welcome to the translation server! Visit /docs for API documentation."}

# 5. Adding chain route
add_routes(
    app,
    chain,
    path="/chain",
)


def main():
    messages = [
        SystemMessage("Translate the following from English into Italian"),
        HumanMessage("hi!"),
    ]
    resp = model.invoke(messages)
    print(resp)
    

if __name__ == "__main__":
    # main()
    import uvicorn
    uvicorn.run(app, host="localhost", port=8700)
    
