import requests
from io import BytesIO
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Fetch MongoDB credentials from environment variables
openAI_key = os.getenv("openAI_key")

client = OpenAI(
    api_key=openAI_key,
)

# Upload a file
def create_file(client, file_path):
    if file_path.startswith("http://") or file_path.startswith("https://"):
        # Download the file content from the URL
        response = requests.get(file_path)
        file_content = BytesIO(response.content)
        file_name = file_path.split("/")[-1]
        file_tuple = (file_name, file_content)
        result = client.files.create(
            file=file_tuple,
            purpose="assistants"
        )
    else:
        # Handle local file path
        with open(file_path, "rb") as file_content:
            result = client.files.create(
                file=file_content,
                purpose="assistants"
            )
    print(result.id)
    return result.id

# Replace with your own file path or URL
file_id = create_file(client, "data/Daily Meals Tracker Template - 2025.csv")

#Create a vector store
vector_store = client.vector_stores.create(
    name="knowledge_base"
)
print(vector_store.id)

#Add the file to the vector store
client.vector_stores.files.create(
    vector_store_id=vector_store.id,
    file_id=file_id
)

# Check status - Run this code until the file is ready to be used (i.e., when the status is completed).
""" result = client.vector_stores.files.list(
    vector_store_id=vector_store.id
)
print(result) """

print("\n\n\n\tEND OF LINE")