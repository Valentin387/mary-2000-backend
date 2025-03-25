# mary-2000-backend
Backend for my AI integrated project

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/python-3.12.4-blue.svg?style=for-the-badge&logo=python)
![GitHub last commit](https://img.shields.io/github/last-commit/Valentin387/mary-2000-backend?style=for-the-badge)
![Issues](https://img.shields.io/github/issues/Valentin387/mary-2000-backend?style=for-the-badge)
![Pull Requests](https://img.shields.io/github/issues-pr/Valentin387/mary-2000-backend?style=for-the-badge)

## Context
My grandma is the best cook in the family. I can proudly say that any success brought by any of us is due to the energy and nutrients gotten from her insanely crazy good cuisine. She has over 70 years of experience as a housewife, but she won’t last forever. To preserve the performance and future academic and economic success of the family, I need to learn to cook like her. I know how to use the different tools in a kitchen, so that’s not the problem. The challenge is that all she does comes from her spontaneous generation of unique recipes. For a month and a half, I documented her meals in a structured format saved inside a Google Sheet. I also had to include some legacy recipes where the template is basically: ingredients and cooking process. This project is my attempt to immortalize her culinary genius using technology.

However, it also serves as a fastAPI backend template for any app that involves file searching with LLM's development keys

## Project Overview
This is a FastAPI backend that leverages OpenAI’s Assistants API to recommend meals based on my grandmother’s recipes. It uses a vector store to search through text files derived from her meal documentation, providing meal suggestions and follow-up chat functionality.

## Project Structure
    ```
    ├── Dockerfile
    ├── LICENSE
    ├── Procfile
    ├── README.md
    ├── config.json
    ├── config.py
    ├── converters
    │   ├── legacy-simplified-converter.py
    │   └── structured-meal-converter.py
    ├── data
    │   ├── init.py
    │   ├── csv exports
    │   │   ├── Daily Meals Tracker Template - 2025.csv
    │   │   ├── Daily Meals Tracker Template - Simplified Form Legacy.csv
    │   │   ├── Daily Meals Tracker Template - Structured Form Legacy.csv
    │   │   └── init.py
    │   ├── models
    │   │   ├── init.py
    │   │   ├── meal_request.py
    │   │   └── meal_types.py
    │   └── txt exports
    │       ├── init.py
    │       ├── almuerzo.txt
    │       ├── cena.txt
    │       ├── desayuno.txt
    │       ├── postre.txt
    │       └── salsa.txt
    ├── folder_structure_gen.py
    ├── main.py
    ├── requirements.txt
    ├── routers
    │   ├── init.py
    │   └── meal_recommendation.py
    └── services
    ├── init.py
    └── fileUploader.py


## Prerequisites
- Python 3.12.4
- An OpenAI API key (available from [OpenAI Platform](https://platform.openai.com/))

## How to Run
Follow these best practices to set up and run the project:

1. **Set Up a Virtual Environment**:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt

3. **Configure Environment**:
OPENAI_API_KEY="your_openai_api_key_here"

- Replace "your_openai_api_key_here" with your actual OpenAI API key.

4. **Run the Application**:
    ```bash
    python main.py

5. **Test the API**:
Open your browser to http://localhost:8000/docs to access the Swagger UI.
Test the endpoints:
- POST /recommend-meal: Input a meal type (e.g., "desayuno") and preferences (e.g., "quick prep") to get a recommendation.
- POST /chat/{thread_id}: Use the thread_id from the previous response to ask follow-up questions.

## Manual File Upload
Upload your .txt files manually to the OpenAI platform:

- Go to https://platform.openai.com/assistants.
- Create an assistant and vector store, then upload files (e.g., desayuno.txt, almuerzo.txt) to the vector store.
- Note the vector store and assistant IDs, and add them to config.json:
    ```json
    {
        "vector_store_id": "your_vector_store_id",
        "assistant_id": "your_assistant_id"
    }

## Notes on Converters
The converters folder contains scripts (legacy-simplified-converter.py and structured-meal-converter.py) tailored to my specific, horribly misformatted CSV files from Google Sheets. They convert these CSVs into .txt files suitable for the vector store. For your own CSV exports, you’ll need to implement your own converter. Example:

- If your CSV has columns Meal Type, Ingredients, Instructions:
    ```python
    import pandas as pd

    df = pd.read_csv("your_meals.csv")
    with open("output.txt", "w") as f:
        for _, row in df.iterrows():
            f.write(f"{row['Meal Type']}: {row['Ingredients']} - {row['Instructions']}\n")

- Adjust based on your data structure.

## Anecdote
I struggled a little too much with the 'file uploading' part of the solution. It was before finding the online UI, so I rather used it instead of spending too much time uploading the files by code. It is possible though! I still recommend using config.py and config.json to save references to the assistant and vector store. For some reason (not really surprising), the OpenAI SDK sometimes behaves contrary to what the official documentation says, so it’s better to have a backup plan—and the config file is a good one.

## Future Improvements
For future release versions, consider:

- Automated File Upload: Revisit fileUploader.py for a robust upload solution.
- Database Integration: Store meal data in a database (e.g., SQLite, PostgreSQL) for easier management.
- User Interface: Build a frontend to interact with the API.
- Recipe Expansion: Add more meal types or preferences (e.g., dietary restrictions).
- Performance: Cache file ID-to-name mappings for faster source citation in responses.
- Developers are welcome to fork the repo and contribute! Check out the issues and pull requests for collaboration opportunities.