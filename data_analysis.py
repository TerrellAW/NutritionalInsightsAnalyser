import pandas as pd
import seaborn as sbn
import matplotlib.pyplot as plt

# Load data from data file
df = pd.read_csv('res/data.csv')

# Fill missing values with mean
df.fillna(df.mean(numeric_only=True), inplace=True)

# Calculate average macronutrient content
avg_macros = df.groupby('Diet_type')[['Protein(g)', 'Carbs(g)', 'Fat(g)']].mean()

# Get top 5 recipes by protein-richness
top_prot = df.sort_values('Protein(g)', ascending=False).groupby('Diet_type').head(5)

# Calculate protein-to-carb and carb-to-fat ratios
df['Protein_to_Carbs'] = df['Protein(g)'] / df['Carbs(g)']
df['Carbs_to_Fat'] = df['Carbs(g)'] / df['Fat(g)']

# Define subplots
fig, (bar, heat, scat) = plt.subplots(1, 3, figsize=(15, 5))

# Average macronutrients bar chart
sbn.barplot(x=avg_macros.index, y=avg_macros['Protein(g)'], ax=bar)
plt.title('Average Protein by Diet Type')
plt.ylabel('Average Protein (g)')

# Top 5 protein recipes heatmap
numeric_data = top_prot.select_dtypes(include='number')
sbn.heatmap(numeric_data, annot=True, ax=heat)

# Scatter map for ratios
sbn.scatterplot(data=df, x='Protein_to_Carbs', y='Carbs_to_Fat', ax=scat)

# Prevent overlapping labels
plt.tight_layout()

# Show diagrams
plt.show()
