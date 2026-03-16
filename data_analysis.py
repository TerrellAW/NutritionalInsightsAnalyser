import os
import pandas as pd
import seaborn as sbn
import matplotlib.pyplot as plt

# Ensure output folder exists
os.makedirs("out", exist_ok=True)

# Load data
df = pd.read_csv("res/data.csv")

# Fill missing values with mean
df.fillna(df.mean(numeric_only=True), inplace=True)

# Average macronutrients per diet
avg_macros = df.groupby("Diet_type")[["Protein(g)", "Carbs(g)", "Fat(g)"]].mean()

# Top 5 protein recipes per diet
top_prot = df.sort_values("Protein(g)", ascending=False).groupby("Diet_type").head(5)

# Ratios
df["Protein_to_Carbs"] = df["Protein(g)"] / df["Carbs(g)"]
df["Carbs_to_Fat"] = df["Carbs(g)"] / df["Fat(g)"]

# Subplots
fig, (bar, heat, scat) = plt.subplots(1, 3, figsize=(18, 5))

# 1) Bar chart: Average Protein by Diet Type
sbn.barplot(x=avg_macros.index, y=avg_macros["Protein(g)"], ax=bar)
bar.set_title("Average Protein by Diet Type")
bar.set_ylabel("Average Protein (g)")
bar.set_xlabel("Diet Type")
bar.tick_params(axis="x", rotation=45)

# 2) Heatmap: Avg macros (clean + meaningful)
sbn.heatmap(avg_macros, annot=True, fmt=".1f", ax=heat)
heat.set_title("Average Macronutrients Heatmap")

# 3) Scatter: Ratio relationships
sbn.scatterplot(data=df, x="Protein_to_Carbs", y="Carbs_to_Fat", ax=scat)
scat.set_title("Protein/Carbs vs Carbs/Fat")
scat.set_xlabel("Protein to Carbs Ratio")
scat.set_ylabel("Carbs to Fat Ratio")

plt.tight_layout()

# Save output
plt.savefig("out/plots.png", dpi=200)
print("Plots saved to out/plots.png")
