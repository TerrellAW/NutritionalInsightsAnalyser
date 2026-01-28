import pandas as pd

# Load data from data file
df = pd.read_csv('res/data.csv')

# Fill missing values with mean
df.fillna(df.mean(), inplace=True)

# Calculate average macronutrient content
avg_macros = df.groupby('Diet_Type')[['Protein(g)', 'Carbs(g)', 'Fat(g)']].mean()

# Get top 5 recipes by protein-richness
top_prot = df.sort_values('Protein(g)', ascending=False).groupby('Diet_Type').head(5)

# Calculate protein-to-carb and carb-to-fat ratios
df['Protein_to_Carbs'] = df['Protein(g)'] / df['Carbs(g)']
df['Carbs_to_Fat'] = df['Carbs(g)'] / df['Fat(g)']

# Test
print(df.head(10))
