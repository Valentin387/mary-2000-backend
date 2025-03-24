import pandas as pd

# Load the CSV file
legacy_recipes_csv = 'legacy_recipes.csv'
df = pd.read_csv(legacy_recipes_csv)

# Function to format a legacy recipe into a readable text block
def format_legacy_recipe(row):
    return f"""**Legacy Recipe**
- Ingredients: {row['Ingredients']}
- Cooking Process: {row['Cooking Process']}
"""

# Create a text file for legacy recipes
with open('legacy_recipes.txt', 'w', encoding='utf-8') as f:
    for index, row in df.iterrows():
        f.write(format_legacy_recipe(row))
        f.write('\\n\\n')  # Add spacing between entries

print("Text file created for legacy recipes.")
