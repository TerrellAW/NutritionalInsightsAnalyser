import pandas as pd
import numpy as np  # Added for safe vectorized division
import time

# Load the real dataset
df = pd.read_csv('res/data.csv')

# 1. Test Original (Iterative-style)
start_slow = time.time()
for _ in range(10): 
    # Standard grouping is robust but slower due to index overhead
    avg = df.groupby('Diet_type')[['Protein(g)', 'Carbs(g)']].mean()
end_slow = time.time()

# 2. Test Optimized (Vectorized-style + NumPy Safety)
start_fast = time.time()
for _ in range(10):
    # .values gets us into the CPU's fast lane
    prot_arr = df['Protein(g)'].values
    carb_arr = df['Carbs(g)'].values
    # np.where handles 0g carbs safely without stopping the CPU
    ratio = np.where(carb_arr != 0, prot_arr / carb_arr, 0)
end_fast = time.time()

print(f"Original logic average: {(end_slow - start_slow)/10:.6f}s")
print(f"Vectorized logic (with NumPy safety) average: {(end_fast - start_fast)/10:.6f}s")