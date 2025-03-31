import os
from fastapi import FastAPI
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from config import get_config, save_config

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment. Please set it in a .env file.")

app = FastAPI()
client = OpenAI(api_key=api_key)  # Explicitly pass the key
app.state.client = client  # Store client in app state

# Configure CORS settings
origins = [
  "http://localhost", # Add the URL of your Angular frontend
  "http://localhost:4200", # Add the URL of your Angular frontend
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
  allow_headers=["Authorization", "Content-Type"] ## Allow all headers for testing
)

from routers import meal_recommendation # Absolute import
app.include_router(meal_recommendation.router)

from services.fileUploader import set_up_vector_store

def setup_assistant(client):
    config = get_config()
    assistant_id = config.get("assistant_id")

    if assistant_id:
        try:
            assistant = client.beta.assistants.retrieve(assistant_id=assistant_id)
            print(f"Using existing assistant with ID: {assistant_id}")
            vector_store_id = set_up_vector_store(client)
            client.beta.assistants.update(
                assistant_id=assistant_id,
                tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}}
            )
            return assistant_id
        except Exception as e:
            print(f"Error retrieving assistant: {e}")
            assistant_id = None

    assistants = client.beta.assistants.list()
    existing_assistant = next((a for a in assistants.data if a.name == "GrandmasMealAssistant"), None)
    if existing_assistant:
        assistant_id = existing_assistant.id
        print(f"Found existing assistant with ID: {assistant_id}")
        vector_store_id = set_up_vector_store(client)
        client.beta.assistants.update(
            assistant_id=assistant_id,
            tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}}
        )
    else:
        vector_store_id = set_up_vector_store(client)
        assistant = client.beta.assistants.create(
            name="GrandmasMealAssistant",
            instructions="You are a meal recommendation assistant based on my grandmother's cooking. Always give responses in Spanish. Use the provided meal data to suggest meals based on the user's meal type (desayuno, almuerzo, cena, snack, postre, salsa, surprise) and preferences. Include meal description, ingredients, and cooking notes. For 'surprise', pick a random meal type from desayuno, almuerzo, cena, or snack. If no exact match exists, suggest a close alternative with reasoning.",
            model="gpt-4o-mini",
            tools=[{"type": "file_search"}],
            tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}}
        )
        assistant_id = assistant.id
        print(f"Created new assistant with ID: {assistant_id}")

    config["assistant_id"] = assistant_id
    save_config(config)
    return assistant_id

app.state.assistant_id = None

async def startup_event():
  app.state.assistant_id = setup_assistant(client)

app.add_event_handler("startup", startup_event)

@ app.get("/")
async def root():
  return {"message": "Grandma's Meal Recommendation API is running"}

if __name__ == "__main__":
  import uvicorn
  uvicorn.run('main:app', port=8000, reload=True)