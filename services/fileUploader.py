import os
from pathlib import Path
from openai import OpenAI
from data.models.meal_types import MealType

client = OpenAI()

_PROJECT_DIR = Path(__file__).resolve().parent.parent
TXT_EXPORTS_DIR = _PROJECT_DIR / "data" / "txt exports"

def set_up_vector_store():
    # Get existing files in OpenAI
    existing_files = {f.filename: f.id for f in client.files.list()}
    file_streams = []
    file_ids = []

    # Prepare files for upload or reuse existing IDs
    for meal_type in MealType:
        file_path = TXT_EXPORTS_DIR / f"{meal_type}.txt"
        if file_path.exists():
            file_name = file_path.name
            if file_name not in existing_files:
                file_streams.append(open(file_path, "rb"))
                print(f"Prepared {file_name} for upload")
            else:
                file_ids.append(existing_files[file_name])
                print(f"File {file_name} already exists with ID: {existing_files[file_name]}")

    # Create or reuse vector store
    vector_stores = client.vector_stores.list()
    vector_store = next((vs for vs in vector_stores.data if vs.name == "GrandmasMeals"), None)
    if not vector_store:
        vector_store = client.vector_stores.create(name="GrandmasMeals")
        print(f"Created vector store with ID: {vector_store.id}")
    else:
        print(f"Using existing vector store with ID: {vector_store.id}")

    # Upload new files if any
    if file_streams:
        file_batch = client.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store.id,
            files=file_streams
        )
        print(f"Upload status: {file_batch.status}, File counts: {file_batch.file_counts}")
        # Add newly uploaded file IDs to the list
        uploaded_file_ids = [f.id for f in file_batch.files] if hasattr(file_batch, 'files') else []
        file_ids.extend(uploaded_file_ids)
        for f in file_streams:
            f.close()  # Clean up file handles

    # Check existing files in the vector store and add missing ones
    current_file_ids = {f.file_id for f in client.vector_stores.files.list(vector_store_id=vector_store.id).data}
    missing_file_ids = set(file_ids) - current_file_ids
    if missing_file_ids:
        client.vector_stores.file_batches.create(
            vector_store_id=vector_store.id,
            file_ids=list(missing_file_ids)
        )
        print(f"Added missing files to vector store: {missing_file_ids}")

    return vector_store.id