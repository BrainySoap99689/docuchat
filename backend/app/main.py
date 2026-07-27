from app.functions import build_prompt, get_conn, check_db, processPDF, build_context, vector_similarity_search, send_prompt
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import psycopg2
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer


load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/documents")
async def get_documents():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT document_name FROM document_names ORDER BY id DESC LIMIT 10;")
    documents = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return documents

    
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    # Save the uploaded file to a temporary location
    temp_file_path = f"temp_{file.filename}"
    check = check_db(temp_file_path)
    if check:
        return {"Error Message": f"{file.filename} has already been uploaded."}
    else:
        with open(temp_file_path, "wb") as f:
            f.write(await file.read())

        # Process the PDF and store embeddings
        num_chunks = processPDF(file.filename)

        # Clean up the temporary file
        os.remove(temp_file_path)

        return {"message": f"Processed {num_chunks} chunks from {file.filename}"}

@app.post("/chat")
async def chat_with_pdf(query: str, document_name: str):
    results = vector_similarity_search(query, document_name)
    context = build_context(results)
    prompt = build_prompt(context, query)
    response = send_prompt(prompt)
    return {"response": response}

    