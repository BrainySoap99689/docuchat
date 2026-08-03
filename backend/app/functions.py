from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import psycopg2
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from ollama import Client

load_dotenv()

ollama_client = Client(host="http://host.docker.internal:11434")

model = None

def get_embedding_model():
    global model

    if model is None:
        model = SentenceTransformer("BAAI/bge-small-en-v1.5")

    return model


splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

# Lazy DB connection: create on first use so imports don't fail when DB is down
conn = None

def get_conn():
    host = os.getenv("DB_HOST")
    database = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    return psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password,
    )

def check_db(pdf_path):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT EXISTS ( 
            SELECT 1 FROM document_names WHERE document_name = %s
            
        )""",
        (pdf_path,)
    )
    ans = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return ans

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)

    pages = []

    for page_num in range(len(doc)):
        page = doc[page_num]

        pages.append({
            "page": page_num + 1,
            "text": page.get_text()
        })

    return pages

def chunkPages(pages):
    chunks = []

    for page in pages:
        page_chunks = splitter.create_documents([page["text"]])
        for chunk in page_chunks:
            chunks.append({
                "page": page["page"],
                "chunk": chunk.page_content
            })

    return chunks

def createEmbeddings(chunk):
    embedding = get_embedding_model().encode(chunk)
    return embedding.tolist()

def storeEmbeddings(chunks, document_name):
    conn = get_conn()
    for chunk in chunks:
        cursor = conn.cursor()
        embedding = createEmbeddings(chunk['chunk'])

        cursor.execute(
            """
            INSERT INTO document_chunks
            (
                document_name,
                page_number,
                chunk_text,
                embedding
            )
            VALUES (%s, %s, %s, %s)
            """,
            (
                document_name,
                chunk["page"],
                chunk["chunk"],
                embedding
            )
        )
        conn.commit()
    cursor.close()
    conn.close()
def trackDocuments(pdf_path):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO document_names
        (
            document_name
        )
        VALUES (%s)
        """,
        (pdf_path,)
    )
    conn.commit()
    cursor.close()
    conn.close()

def processPDF(pdf_path):
    pages = extract_text(pdf_path)
    chunks = chunkPages(pages)
    storeEmbeddings(chunks, pdf_path)
    trackDocuments(pdf_path)

    return len(chunks)

def vector_similarity_search(question, document_name):
    conn = get_conn()
    cursor = conn.cursor()
    question_embedding = model.encode([question])[0].tolist()
    query = """
        SELECT
        chunk_text,
        page_number,
        embedding <=> %s::vector AS distance
    FROM document_chunks
    WHERE document_name = %s
    ORDER BY embedding <=> %s::vector
    LIMIT 5;
    """
    cursor.execute(query, (question_embedding, document_name, question_embedding))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def build_context(results):
    context_parts = []
    for chunk_text, page_number, distance in results:
        context_parts.append(f"Page {page_number}: {chunk_text}")
    context = "\n\n".join(context_parts)
    return context

def build_prompt(context, question):
    prompt = f"""
        You are answering questions about a document.

        Use only the context provided below.
        If the answer is not contained in the context, say:
        "I could not find that information in the document."

        Include page numbers when possible.

        Context:
        {context}

        Question:
        {question}
    """
    return prompt

def send_prompt(prompt):
    response = ollama_client.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.message.content

    