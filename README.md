# mary-2000-backend
Backend for my AI integrated project

## Context
My grandma is the best cook of the family, I can proudly say that any success brought by any of us is due to the energy and nutrients gotten from her insanely crazy good cuisine, she has over 70 years of experience being a housewife, she will not last forever, therefore, in order to save the performance and future academic and economic success of the family, I need to learn to cook like her... I know how to use the different stuff in a kitchen so that is not the problem, the problem is that all she does comes from her spontaneous generation of unique recipes. For a month and a half I documented her meals in a structure format saved inside a google sheet. I also had to include some legacy recipes where the template is basically: ingredients and cooking process.

## Remember to

.env
OPENAI_API_KEY


create a top level folder named 'data', inside of it, create sub folders:

'csv exports',
'txt exports'

The csv files you used for the first trial were named:
INPUT_FILES = [
    os.path.join(PROJECT_DIR, 'data', 'csv exports', 'Daily Meals Tracker Template - 2025.csv'),
    os.path.join(PROJECT_DIR, 'data', 'csv exports', 'Daily Meals Tracker Template - Structured Form Legacy.csv')
]

and

### Define the absolute path to the project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent
SIMPLIFIED_CSV = os.path.join(PROJECT_DIR, 'data', 'csv exports', 'Daily Meals Tracker Template - Simplified Form Legacy.csv')


Project Structure:
├── Dockerfile
├── LICENSE
├── Procfile
├── README.md
├── converters
│   ├── legacy-simplified-converter.py
│   └── structured-meal-converter.py
├── data
│   ├── __init__.py
│   ├── csv exports
│   │   ├── Daily Meals Tracker Template - 2025.csv
│   │   ├── Daily Meals Tracker Template - Simplified Form Legacy.csv
│   │   ├── Daily Meals Tracker Template - Structured Form Legacy.csv
│   │   └── __init__.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── meal_request.py
│   │   └── meal_types.py
│   └── txt exports
│       ├── almuerzo.txt
│       ├── cena.txt
│       ├── desayuno.txt
│       ├── postre.txt
│       ├── salsa.txt
│       └── snack.txt
├── folder_strucutre_gen.py
├── main.py
├── requirements.txt
├── routers
│   ├── __init__.py
│   └── meal_recommendation.py
└── services
    ├── __init__.py
    └── fileUploader.py


