import azure.functions as func
import pandas as pd
import io
import json
import time

app = func.FunctionApp()

@app.route(route="get_nutrition_data", auth_level=func.AuthLevel.ANONYMOUS)
def get_nutrition_data(req: func.HttpRequest) -> func.HttpResponse:
    start_time = time.time()
    
    # Using the SAS URL provided from Terrell's storage
    # NOTE: This link expires on April 1st, 2026
    sas_url = "https://projacct.blob.core.windows.net/data-blob/data.csv?sp=rw&st=2026-03-19T16:15:30Z&se=2026-04-01T00:30:30Z&sv=2024-11-04&sr=b&sig=ORBmcYWnVbaW123r3qSGAOOkVChixGIO2lAVxBjtBh4%3D"

    try:
        # 1. Read the CSV directly from the Azure Blob SAS URL
        df = pd.read_csv(sas_url)
        
        # 2. Convert to JSON format for Muhammad's dashboard
        json_data = df.to_dict(orient='records')
        
        # 3. Calculate metadata for assignment marks
        execution_time = round(time.time() - start_time, 4)
        record_count = len(df)

        # 4. Create the final response object
        response_body = {
            "data": json_data,
            "metadata": {
                "execution_time_seconds": execution_time,
                "record_count": record_count,
                "status": "success",
                "datasource": "Azure Blob Storage (projacct)"
            }
        }

        return func.HttpResponse(
            json.dumps(response_body),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            mimetype="application/json",
            status_code=500
        )