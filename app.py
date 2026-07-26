# from memory.database import init_db

# init_db()
# from agents.research_agent import agent

# response = agent.invoke(
#     {
#         "messages": [
#             {
#                 "role": "user",
#                 "content":"What is my name?"
#             }
#         ]
#     }
# )

# print(response)
from fastapi import FastAPI
from memory.database import init_db
from schemas import ChatRequest
from agents.research_agent import agent

init_db()

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Production Ready Deep Agent is Running 🚀"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": request.message
                }
            ]
        }
    )

    print(response)

    return response