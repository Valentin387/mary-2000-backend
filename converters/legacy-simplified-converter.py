import os
import csv
import pandas as pd
from pathlib import Path
from datetime import datetime

# Define the absolute path to the project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent
SIMPLIFIED_CSV = os.path.join(PROJECT_DIR, 'data', 'csv exports', 'Daily Meals Tracker Template - Simplified Form Legacy.csv')
OUTPUT_DIR = os.path.join(PROJECT_DIR, 'data', 'txt exports')

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Function to normalize date to DD/MM/YYYY format
def normalize_date(date_str):
    if not date_str:
        return 'Unknown'
    try:
        for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%Y/%m/%d'):
            try:
                date_obj = datetime.strptime(date_str, fmt)
                return date_obj.strftime('%d/%m/%Y')
            except ValueError:
                continue
        raise ValueError(f"Unknown date format: {date_str}")
    except ValueError as e:
        print(f"Warning: {e}. Defaulting to 'Unknown'")
        return 'Unknown'

# Function to parse the simplified CSV using csv module
def parse_simplified_entries(csv_path):
    meals = []
    current_meal = {}

    with open(csv_path, 'r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f, quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for row in reader:
            if not row or all(x.strip() == '' for x in row):
                continue

            key = row[0].strip()
            value = row[1].strip() if len(row) > 1 else ''

            if key == 'Daily Meals Tracker Template':
                if current_meal:  # Save the previous meal
                    meals.append(current_meal)
                current_meal = {}
                continue

            if key == 'Date' and value:
                value = normalize_date(value)

            if value:  # Only add non-empty values
                current_meal[key] = value

        # Append the last meal
        if current_meal:
            meals.append(current_meal)

    return meals

# Manual mapping of titles to meal types (customize as needed)
MEAL_TYPE_MAPPING = {
    'Pizza casera': 'cena',
    'Kartoffelpuffer: pancakes de papa rallada': 'desayuno',
    'pancakes': 'desayuno',
    'Huevos revueltos de Philippe Thalhofer': 'desayuno',
    'Papas de Daniel Lorand Szabo': 'cena',
    'ensalada gourmet 1': 'almuerzo',
    'Ensalada de habichuelas de la abuela': 'almuerzo',
    'salsa de mango': 'salsa',
    'arepa picara': 'cena',
    'Omelette Híbrido': 'desayuno',
    'Alitas BBQ Caseras 🍗🔥': 'almuerzo',
    'Apuros – Tortilla Rápida y Completa 🌯🔥':'cena',
    'Arroz Aliñado 🌿🍚':'almuerzo',
    'Rollo de Pollo 🍗🔥':'almuerzo',
    'desayuno y consejos varios':'desayuno',
    'Ensalada gourmet':'almuerzo'
}

# Function to format a simplified meal entry, excluding empty fields
def format_simplified_entry(row):
    meal_type = MEAL_TYPE_MAPPING.get(row.get('title', ''), 'snack')  # Default to 'snack'

    # Define fields to check
    fields = {
        'Date': str(row.get('Date', 'Unknown')),
        'title': str(row.get('title', 'None')),
        'Ingredientes principales': str(row.get('Ingredientes principales', 'None')),
        'Cooking Notes': str(row.get('Cooking Notes', 'None'))
    }

    # Filter out empty or null fields
    non_empty_fields = {k: v for k, v in fields.items() if v and v.lower() not in ('', 'none', 'nan')}

    # Build the formatted string
    lines = [f"**{meal_type} Meal on {non_empty_fields.pop('Date', 'Unknown')}**"]
    for field_name, field_value in non_empty_fields.items():
        if field_name == 'Cooking Notes':
            lines.append(f"- {field_name}: \n{field_value}")
        else:
            lines.append(f"- {field_name}: {field_value}")

    return '\n'.join(lines)

# Parse the CSV
simplified_entries = parse_simplified_entries(SIMPLIFIED_CSV)
print("Parsed simplified entries:", simplified_entries)

# Convert to DataFrame
df = pd.DataFrame(simplified_entries)
print("Converted to DataFrame:\n", df)

# Append to text files based on mapped meal types
for index, row in df.iterrows():
    meal_type = MEAL_TYPE_MAPPING.get(row.get('title', ''), 'snack')  # Default to 'snack'
    output_file = os.path.join(OUTPUT_DIR, f'{meal_type.lower()}.txt')
    with open(output_file, 'a', encoding='utf-8') as f:  # Append mode
        formatted_entry = format_simplified_entry(row)
        f.write(formatted_entry)
        f.write('\n\n')

print("Text files updated with simplified legacy entries in", OUTPUT_DIR)