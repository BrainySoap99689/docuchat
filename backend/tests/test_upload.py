import os

os.environ["DB_NAME"] = "app_db_test"

from fastapi.testclient import TestClient
from app.main import app
import psycopg2

client = TestClient(app)

def get_test_conn():
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

def test_upload():
    # Clean up database before the test
    conn = get_test_conn()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM document_chunks;")
    cursor.execute("DELETE FROM document_names;")
    conn.commit()
    cursor.close()
    conn.close()

    # Upload a PDF file
    with open("tests/sample.pdf", "rb") as f:
        response = client.post("/upload", files={"file": ("sample.pdf", f, "application/pdf")})

    assert response.status_code == 200
    assert "Processed" in response.json()["message"]

    # Check if the document name is stored in the database
    conn = get_test_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT document_name FROM document_names WHERE document_name = %s;", ("sample.pdf",))
    result = cursor.fetchone()
    cursor.execute("SELECT COUNT(*) FROM document_chunks WHERE document_name = %s;", ("sample.pdf",))
    chunk_count = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    assert result is not None
    assert result[0] == "sample.pdf"
    assert chunk_count > 0