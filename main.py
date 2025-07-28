import os
from typing import List, Dict
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from groq import Client

app = FastAPI()

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# add_middle
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for simplicity; adjust as needed
    allow_credentials = True, # Allow credentials if needed
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

class userInput(BaseModel):
    message: str # User's input message
    role: str = 'user'  # Default role is 'user'
    conversation_id: str  # Required for conversation tracking

class conversation:
    def __init__(self):
        self.messages: List[Dict[str,str]] = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]
        self.active : bool = True

#In-memory conversation management
conversations: Dict[str, conversation] = {} 

def query_groq_api(conversations: conversation) -> str:
    try:
        completion = Client.chat.completions.create(
            model="llama3-8b-8192",
            messages=conversation.messages,
            max_tokens=1024,
            temperature=1,
            top_p = 1,
            stream= True,
            stop = None
        )
        response = ""
        for chunk in completion:
            response += chunk.choices[0].delta.content or ""
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying Groq API: {str(e)}")

def get_or_create_conversation(conversation_id: str) -> conversation:
    if conversation_id not in conversations:
        conversations[conversation_id] = conversation()
    return conversations[conversation_id]

@app.post("/chat")
async def chat(input: userInput):
    #retrieve or create a conversation
    conv = get_or_create_conversation(input.conversation_id)
    
    if not conv.active:
        raise HTTPException(status_code=400, detail="Conversation is no longer active.")  
    
    try:
        conversation.messages.append({"role": input.role, "content": input.message})
        response = query_groq_api(conv)
        conversation.messages.append({"role": "assistant", "content": response})
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
