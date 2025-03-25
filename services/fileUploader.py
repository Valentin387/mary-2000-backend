import os
from pathlib import Path
from openai import OpenAI
from data.models.meal_types import MealType

client = OpenAI()

_PROJECT_DIR = Path(__file__).resolve().parent.parent
TXT_EXPORTS_DIR = _PROJECT_DIR / "data" / "txt exports"

def set_up_vector_store():
    existing_files = {f.filename: f.id for f in client.files.list()}
    file_ids = []

    for meal_type in MealType:
        file_path = TXT_EXPORTS_DIR / f"{meal_type}.txt"
        if file_path.exists():
            file_name = file_path.name
            if file_name not in existing_files:
                with open(file_path, "rb") as f:
                    uploaded_file = client.files.create(file=f, purpose="assistants")
                    file_ids.append(uploaded_file.id)
                    print(f"Uploaded {file_name} with ID: {uploaded_file.id}")
            else:
                file_ids.append(existing_files[file_name])
                print(f"File {file_name} already uploaded, using existing ID: {existing_files[file_name]}")

    vector_stores = client.beta.vector_stores.list()
    vector_store = next((vs for vs in vector_stores.data if vs.name == "GrandmasMeals"), None)
    if not vector_store:
        vector_store = client.beta.vector_stores.create(name="GrandmasMeals")
        print(f"Created vector store with ID: {vector_store.id}")
    else:
        print(f"Using existing vector store with ID: {vector_store.id}")

    current_file_ids = {f.file_id for f in client.beta.vector_stores.files.list(vector_store_id=vector_store.id).data}
    missing_file_ids = set(file_ids) - current_file_ids
    if missing_file_ids:
        client.beta.vector_stores.file_batches.create(
            vector_store_id=vector_store.id,
            file_ids=list(missing_file_ids)
        )
        print(f"Added missing files to vector store: {missing_file_ids}")

    return vector_store.id