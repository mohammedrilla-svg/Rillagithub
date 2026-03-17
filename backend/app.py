import sys
import os
import shutil
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Add the parent directory to sys.path to access tools
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# Load environment variables from .env
load_dotenv(os.path.join(parent_dir, '.env'))
sys.path.append(parent_dir)

from tools.generate_test_cases import generate_test_cases
from tools.extract_text import extract_text_from_file

app = FastAPI(title="Local Test Case Generator")

# Ensure .tmp directory exists for file uploads
TMP_DIR = os.path.join(parent_dir, ".tmp")
os.makedirs(TMP_DIR, exist_ok=True)

# Allow CORS for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TestCaseRequest(BaseModel):
    user_story: str

@app.post("/generate")
async def generate_endpoint(request: TestCaseRequest):
    try:
        # Layer 2: Navigation - Calling Layer 3: Tool
        result = generate_test_cases(request.user_story)
        
        if "error" in result:

            raise HTTPException(status_code=500, detail=result["error"])
            
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload")
async def upload_endpoint(file: UploadFile = File(...)):
    try:
        # Save uploaded file to .tmp/
        file_path = os.path.join(TMP_DIR, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Extract text from file
        result = extract_text_from_file(file_path)

        # Clean up temp file
        os.remove(file_path)

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        # Generate test cases from extracted text
        test_result = generate_test_cases(result["text"])

        if "error" in test_result:
            raise HTTPException(status_code=500, detail=test_result["error"])

        return test_result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "Local Test Case Generator"}
