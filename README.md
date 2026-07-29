# Docuchat

Docuchat is an application that allows users to upload PDFs and ask questions about them.

## Features

* Upload and process PDF documents
* Extract and divide PDF text into smaller chunks
* Generate vector embeddings for document chunks
* Store embeddings in PostgreSQL using pgvector
* Search documents using vector similarity
* Ask questions about a selected document
* Generate answers using a locally running Ollama model
* Display recently uploaded documents
* Run the frontend, backend, and database using Docker Compose

## Technology Stack

### Frontend

* Next.js
* React
* TypeScript
* Tailwind CSS

### Backend

* FastAPI
* Python 3.11
* PyMuPDF
* Sentence Transformers
* Ollama Python client

### Database

* PostgreSQL
* pgvector

### Infrastructure

* Docker
* Docker Compose
* GitHub Actions

## How It Works

```text
PDF upload
    ↓
Text extraction
    ↓
Text chunking
    ↓
Embedding generation
    ↓
PostgreSQL + pgvector storage
```

When a user asks a question:

```text
User question
    ↓
Question embedding
    ↓
Vector similarity search
    ↓
Relevant document chunks
    ↓
Ollama language model
    ↓
Generated answer
```

## Prerequisites

Before running the project, install:

* Git
* Docker Desktop
* Ollama

Ollama should be installed directly on the host computer.

Verify the installation:

```bash
ollama --version
```

Download a model:

```bash
ollama pull llama3.2
```

Verify that Ollama is running:

```bash
curl http://localhost:11434/api/tags
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/docuchat.git
cd docuchat
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Create the environment file

Copy the example environment file:

```bash
cp .env.example .env
```

Update `.env` with your local database settings:

```env
DB_HOST=db
DB_NAME=app_db
DB_USER=postgres
DB_PASSWORD=change_this_password

```

Do not commit the real `.env` file to GitHub.

### 3. Start Ollama

Launch the Ollama application or run:

```bash
ollama serve
```

### 4. Build and start the application

```bash
docker compose up --build
```

The services should be available at:

* Frontend: `http://localhost:3000`
* Backend: `http://localhost:8000`
* FastAPI documentation: `http://localhost:8000/docs`
* PostgreSQL host port: `5433`

## Running in the Background

```bash
docker compose up -d --build
```

View logs:

```bash
docker compose logs -f
```

View backend logs only:

```bash
docker compose logs -f backend
```

Stop the application:

```bash
docker compose down
```

## API Endpoints

### Upload a document

```http
POST /upload
```

Uploads and processes a PDF document.

Example:

```bash
curl -X POST \
  -F "file=@example.pdf" \
  http://localhost:8000/upload
```

### List recent documents

```http
GET /documents
```

Returns recently uploaded document names.

Example:

```bash
curl http://localhost:8000/documents
```

### Ask a question

```http
POST /chat
```

Submits a question about a selected document.

The exact request format may depend on the current backend implementation.

Example:

```bash
curl -X POST \
  "http://localhost:8000/chat?query=What%20is%20the%20document%20about%3F&document_name=example.pdf"
```

## Database

The application uses PostgreSQL with the pgvector extension.

Example document chunk table:

```sql
CREATE TABLE document_chunks (
    id SERIAL PRIMARY KEY,
    document_name TEXT NOT NULL,
    page_number INTEGER,
    chunk_text TEXT NOT NULL,
    embedding VECTOR(384)
);
```

Example document-name table:

```sql
CREATE TABLE document_names (
    id SERIAL PRIMARY KEY,
    document_name TEXT NOT NULL
);
```

Connect to PostgreSQL inside Docker:

```bash
docker compose exec db psql -U postgres -d docuchat
```

List tables:

```sql
\dt
```

Describe a table:

```sql
\d document_chunks
```

Exit PostgreSQL:

```sql
\q
```

## Embedding Model

Docuchat currently uses:

```text
BAAI/bge-small-en-v1.5
```

This model produces embeddings with 384 dimensions.

The PostgreSQL vector column must therefore use:

```sql
VECTOR(384)
```

## Ollama Configuration

The FastAPI backend runs inside Docker, while Ollama runs on the host computer.

The backend should connect to Ollama using:

```text
http://host.docker.internal:11434
```

Example Python client:

```python
from ollama import Client

client = Client(
    host="http://host.docker.internal:11434"
)
```

Using `localhost:11434` from inside the backend container will attempt to connect to the backend container itself rather than the host computer.

## Development

### Rebuild only the backend

```bash
docker compose up -d --build backend
```

### Rebuild only the frontend

```bash
docker compose up -d --build frontend
```

### Open a shell inside the backend

```bash
docker compose exec backend sh
```

### Open a shell inside the frontend

```bash
docker compose exec frontend sh
```

## Continuous Integration

GitHub Actions runs automated checks when code is pushed to `main` or when a pull request targets `main`.

Current checks include:

* Installing backend dependencies
* Checking Python syntax
* Installing frontend dependencies
* Running frontend linting
* Building the Next.js frontend

Automated backend tests will be added later using pytest.

## Environment Variables

Do not commit passwords or private environment values.

The repository should contain:

```text
.env.example
```

The repository should not contain:

```text
.env
```

Make sure `.gitignore` includes:

```gitignore
.env
.env.local
*.env
```

An example `.env.example` file may contain placeholder values:

```env
DB_HOST=db
DB_NAME=app_db
DB_USER=postgres
DB_PASSWORD=replace_with_your_password

```

## Troubleshooting

### Ollama connection error

If the backend reports:

```text
Failed to connect to Ollama
```

Confirm that Ollama is running:

```bash
curl http://localhost:11434/api/tags
```

Then test access from the backend container:

```bash
docker compose exec backend \
  curl http://host.docker.internal:11434/api/tags
```

### Frontend changes are not appearing

Rebuild the frontend:

```bash
docker compose up -d --build frontend
```

If necessary, rebuild without using the Docker cache:

```bash
docker compose build --no-cache frontend
docker compose up -d frontend
```

### Database connection error

Confirm that the backend uses the Docker Compose database service name:

```env
DB_HOST=db
```

Do not use `localhost` as the database host from inside the backend container.

### View container status

```bash
docker compose ps
```

### View all logs

```bash
docker compose logs -f
```

## Roadmap

Potential future improvements include:

* Support for additional document formats
* Document deletion and management
* Conversation history
* Source citations in generated answers
* Page-level references
* Streaming LLM responses
* Multiple Ollama model options
* User authentication
* Automated backend tests
* Improved retrieval and reranking
* Production deployment support

## Contributing

Contributions are welcome.

To contribute:

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Test your changes locally.
5. Open a pull request.

Example:

```bash
git checkout -b feature/my-feature
git add .
git commit -m "Add my feature"
git push origin feature/my-feature
```

For bugs, use the bug-report issue form.

For feature suggestions, use the feature-request issue form.

## Security

Do not post passwords, API keys, `.env` contents, personal documents, or other sensitive information in issues or pull requests.

Potential security vulnerabilities should be reported privately through GitHub Security Advisories.

## License

This project is licensed under the terms described in the `LICENSE` file.

## Author

Created by Aryavikram Pingali.

GitHub: `https://github.com/BrainySoap99689`
