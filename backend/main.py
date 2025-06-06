from fastapi import FastAPI, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
from ingest import process_pdf
from qa_chain import qa_pipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    process_pdf(contents, file.filename)
    return {"message": f"{file.filename} processed successfully"}

@app.get("/ask")
async def ask_question(q: str = Query(...)):
    result = qa_pipeline(q)
    return {"answer": result}
