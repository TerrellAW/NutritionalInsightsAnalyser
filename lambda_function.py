import io
import json
import numpy as np
import pandas as pd
import warnings 
from azure.storage.blob import BlobServiceClient

# Suppress the divide by zero warning
warnings.filterwarnings("ignore", category=RuntimeWarning, message="divide by zero encountered in divide")

# Azurite connection string
connect_str = (
    "DefaultEndpointsProtocol=http;"
    "AccountName=devstoreaccount1;"
    "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
    "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
)

def serverless_process():
    print("[SERVERLESS SIMULATION] Starting data processing from Azurite...")
    
    # 1. Connect to Azurite
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_name = "datasets"
    blob_name = "data.csv"
    
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)
    
    # 2. Download CSV from Azurite
    stream = blob_client.download_blob().readall()
    df = pd.read_csv(io.BytesIO(stream))
    print(f"Downloaded {blob_name} | Rows: {df.shape[0]}, Columns: {df.shape[1]}")
    
    # 3. Clean data (as in Task 1)
    df.fillna(df.mean(numeric_only=True), inplace=True)
    
    # 4. Perform Vectorized Calculations (Optimized for Task 5)
    # Instead of multiple steps, we perform bulk column-wise operations
    df['Protein_to_Carbs'] = df['Protein(g)'].values / df['Carbs(g)'].values
    df['Carbs_to_Fat'] = np.where(df['Fat(g)'] != 0, df['Carbs(g)'].values / df['Fat(g)'].values, 0)
    
    # Efficient grouping using numeric_only to skip unnecessary overhead
    avg_macros = df.groupby('Diet_type', as_index=False)[['Protein(g)', 'Carbs(g)', 'Fat(g)']].mean(numeric_only=True)
    
    # Fast top-n extraction
    top_prot = df.sort_values(['Diet_type', 'Protein(g)'], ascending=[True, False]).groupby('Diet_type').head(5)
    
    # 5. Prepare results for NoSQL simulation
    results = {
        "average_macros_per_diet": avg_macros.round(3).reset_index().to_dict(orient='records'),
        "top_5_protein_recipes_per_diet": top_prot[['Diet_type', 'Recipe_name', 'Protein(g)']].to_dict(orient='records'),
        "sample_recipes_with_ratios": df[['Recipe_name', 'Protein_to_Carbs', 'Carbs_to_Fat']].head(10).to_dict(orient='records'),
        "dataset_summary": {
            "total_recipes": len(df),
            "diet_types": df['Diet_type'].unique().tolist(),
            "cuisine_types": df['Cuisine_type'].unique().tolist()
        }
    }
    
    # 6. Save to JSON (simulated NoSQL)
    output_file = "simulated_nosql.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=4)
    
    print(f"[SERVERLESS SIMULATION] Processing complete.")
    print(f"Results saved to {output_file}")
    return results

# Manual trigger (simulating serverless invocation)
if __name__ == "__main__":
    print("=" * 50)
    print("Simulated Azure Function (Triggered Manually)")
    print("=" * 50)
    try:
        serverless_process()
        print("[✓] Serverless simulation finished successfully.")
    except Exception as e:
        print(f"[✗] Error: {e}")