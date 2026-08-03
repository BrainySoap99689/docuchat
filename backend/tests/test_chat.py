import os

os.environ["DB_NAME"] = "app_db_test"

from fastapi.testclient import TestClient
from app.main import app
import psycopg2

client = TestClient(app)

def test_chat(monkeypatch):
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
    conn = get_test_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM document_chunks;")
    cursor.execute("DELETE FROM document_names;")
    conn.commit()
    cursor.close()
    conn.close()
    # First upload the known PDF
    with open("tests/sample.pdf", "rb") as f:
        upload_response = client.post("/upload",files={"file": ("sample.pdf", f, "application/pdf")})

    assert upload_response.status_code == 200

    def fake_send_prompt(prompt):
        # Verify that vector search + context building actually
        # retrieved the correct information from sample.pdf
        assert "Sarah Thompson" in prompt

        # Pretend this came from Ollama
        return "The CEO of Blueberry Systems is Sarah Thompson."

    monkeypatch.setattr("app.main.send_prompt",fake_send_prompt)

    response = client.post("/chat",params={"query": "Who is the CEO of Blueberry Systems?","document_name": "sample.pdf"})

    assert response.status_code == 200

    answer = response.json()["response"]

    assert "Sarah Thompson" in answer