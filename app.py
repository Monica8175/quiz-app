from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pdf_reader import extract_text_from_pdf
from quiz_generator import generate_quiz
from database import init_db, save_quiz, save_score, get_history
import io

app = FastAPI()

# Initialize DB on startup
init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return FileResponse("index.html")

@app.post("/upload")
async def upload_pdf(pdf: UploadFile = File(...)):
    content = await pdf.read()
    text = extract_text_from_pdf(io.BytesIO(content))
    quiz = generate_quiz(text)

    # Save quiz to DB
    quiz_id = save_quiz(pdf.filename, quiz)

    return {"quiz": quiz, "quiz_id": quiz_id}

@app.post("/submit")
async def submit_score(data: dict):
    save_score(data["quiz_id"], data["score"])
    return {"message": "Score saved!"}

@app.get("/history")
async def history():
    return get_history()
