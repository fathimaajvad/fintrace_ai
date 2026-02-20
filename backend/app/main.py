from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import time

from app.detection import analyze_transactions

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    try:
        start_time = time.time()

        # Read CSV
        df = pd.read_csv(file.file)

        # Run detection logic
        result = analyze_transactions(df)

        # Add processing time
        result["summary"]["processing_time_seconds"] = round(
            time.time() - start_time, 2
        )

        return result

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
