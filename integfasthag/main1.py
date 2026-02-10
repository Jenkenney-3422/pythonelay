import os
import torch
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
from typing import List

# --- CONFIGURATION ---
MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"
SAVE_PATH = "./my_local_model2"

# --- AUTO-SAVE LOGIC ---
if not os.path.exists(SAVE_PATH):
    print("🚀 First time setup: Downloading and saving model...")
    # Load to CPU first to save VRAM during download
    temp_pipe = pipeline("sentiment-analysis", model=MODEL_NAME)
    temp_pipe.save_pretrained(SAVE_PATH)
    print(f"✅ Model saved to {SAVE_PATH}")

# --- INITIALIZE API ---
app = FastAPI(title="FastAPI + Hugging Face Batch API")

# --- LOAD MODEL (ONCE) ---
# We use device=0 for your GPU. 
# We add batch_size=4 to optimize your 2.2GB VRAM without crashing it.
print("🧠 Loading model into GPU...")
classifier = pipeline(
    "sentiment-analysis", 
    model=SAVE_PATH, 
    tokenizer=SAVE_PATH, 
    device=0,
    batch_size=3 
)

# --- DATA MODELS ---
class SingleInput(BaseModel):
    text: str

class BatchInput(BaseModel):
    texts: List[str] # Allows a list of strings

# --- ENDPOINTS ---
@app.get("/")
def health_check():
    return {"status": "Ready", "hardware": "GPU Active", "vram_limit": "2.2GB"}

@app.post("/predict")
async def predict_single(data: SingleInput):
    prediction = classifier(data.text)[0]
    return {"text": data.text, "result": prediction}

@app.post("/predict_batch")
async def predict_batch(data: BatchInput):
    # The pipeline handles the list automatically!
    predictions = classifier(data.texts)
    
    # Zip them together for a clean response
    results = [
        {"text": t, "result": p} 
        for t, p in zip(data.texts, predictions)
    ]
    return {"batch_results": results}