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

def test_documents():
    # Clean up database before the test
    conn = get_test_conn()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM document_names;")
    # Run the test 
    cursor.execute(
        """
        INSERT INTO document_names (document_name)
        VALUES (%s), (%s), (%s);
        """,
        ("biology.pdf", "physics.pdf", "chemistry.pdf")
    )

    conn.commit()
    cursor.close()
    conn.close()

    response = client.get("/documents")

    assert response.status_code == 200
    assert response.json() == [
        "chemistry.pdf",
        "physics.pdf",
        "biology.pdf"
    ]
    