from pathlib import Path
from openai import OpenAI
from data.models.meal_types import MealType
from config import get_config, save_config

_PROJECT_DIR = Path(__file__).resolve().parent.parent
TXT_EXPORTS_DIR = _PROJECT_DIR / "data" / "txt exports"

def set_up_vector_store(client: OpenAI):
    config = get_config()
    vector_store_id = config.get("vector_store_id")

    if vector_store_id:
        try:
            vector_store = client.vector_stores.retrieve(vector_store_id=vector_store_id)
            print(f"Using existing vector store with ID: {vector_store.id}")
            return vector_store.id
        except Exception as e:
            print(f"Error retrieving vector store: {e}")
            vector_store_id = None

    vector_stores = client.vector_stores.list()
    existing_store = next((vs for vs in vector_stores.data if vs.name == "GrandmasMeals"), None)
    if existing_store:
        vector_store_id = existing_store.id
        print(f"Found existing vector store with ID: {vector_store_id}")
    else:
        vector_store = client.vector_stores.create(name="GrandmasMeals")
        vector_store_id = vector_store.id
        print(f"Created new vector store with ID: {vector_store_id}")

    config["vector_store_id"] = vector_store_id
    save_config(config)
    return vector_store_id