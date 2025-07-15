# server.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from inference_worker import run_inference
from logik_11_07 import run_pipeline

app = FastAPI(title="Risk-Field-Extractor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

class TextRequest(BaseModel):
    text: str

@app.post("/extract")
def extract(req: TextRequest):
    input_text = req.text.strip()
    if not input_text:
        raise HTTPException(status_code=400, detail="Text must not be empty")

    result = run_inference(input_text)
    advice = run_pipeline(result)
    return {"advice": advice}
