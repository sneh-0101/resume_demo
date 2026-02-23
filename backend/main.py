from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/match")
async def match_resume(file: UploadFile = File(...)):
    """Simple placeholder endpoint that returns a short text snippet and a dummy match.

    Replace this with actual parsing, NLP processing and matching logic from the existing
    project's `utils` modules when ready.
    """
    content = await file.read()
    text = None
    try:
        text = content.decode(errors="ignore")
    except Exception:
        text = str(content)

    return {
        "filename": file.filename,
        "snippet": (text or "")[:1000],
        "matches": [{"job_title": "Software Engineer", "score": 0.78}],
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
