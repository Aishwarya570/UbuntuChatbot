from fastapi import FastAPI
from pydantic import BaseModel
from utils.chatbot import Chatbot

# Initialize FastAPI and chatbot
app = FastAPI()
chatbot = Chatbot()

# Request model
# class QueryRequest(BaseModel):
#     question: str

from fastapi import FastAPI
from fastapi.responses import StreamingResponse, JSONResponse
from utils.chatbot import Chatbot

app = FastAPI()
chatbot = Chatbot()

@app.post("/ask/")
async def ask_question(question: str, stream: bool = False):
    """Handles user queries and returns chatbot responses.
    
    - If `stream=True`, returns **streaming response**.
    - Otherwise, returns a **standard JSON response** (for Swagger UI).
    """

    try:
        # Ensure chatbot.ask() is a generator
        response_generator = chatbot.ask_in_api(question)
        
        # If chatbot.ask() returned None, handle it
        if response_generator is None:
            return JSONResponse(content={"error": "No response generated."}, status_code=500)

        # Streaming Response
        if stream:
            return StreamingResponse(response_generator, media_type="text/plain")

        # Standard JSON Response
        response_text = "".join(response_generator)  # Convert generator to string
        return JSONResponse(content={"answer": response_text})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)




@app.get("/")
def home():
    return {"message": "Chatbot API is running!"}

