"use client";

import { useState, useEffect } from "react";

type ChatMessage = {
  id: number;
  role: "user" | "assistant";
  content: string;
};

export default function Home() {
  const [error, setError] = useState<string | null>(null);
  const [documents, setDocuments] = useState<string[]>([]);
  const [selectedDocument, setSelectedDocument] = useState<string | null>(null);
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  async function handleSend() {
    const trimmedQuestion = question.trim();
    if (!selectedDocument || !trimmedQuestion) return;

    const userMessage: ChatMessage = {
      id: Date.now(),
      role: "user",
      content: trimmedQuestion,
    };

    setMessages((prev) => [...prev, userMessage]);
    setQuestion("");
    setError(null);
    setIsLoading(true);

    try {
      const response = await fetch(
        `http://localhost:8000/chat?query=${encodeURIComponent(trimmedQuestion)}&document_name=${encodeURIComponent(selectedDocument)}`,
        {
          method: "POST",
        }
      );

      const data = await response.json();
      const assistantMessage: ChatMessage = {
        id: Date.now() + 1,
        role: "assistant",
        content: data.response || data.answer || JSON.stringify(data),
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      console.error("Failed to send message:", err);
      setError("Failed to send message");
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    async function fetchDocuments() {
      try {
        const response = await fetch("http://localhost:8000/documents");
        const data = await response.json();
        setDocuments(data);
        if (data.length > 0) {
          setSelectedDocument(data[0]);
        }
      } catch (err) {
        console.error("Failed to fetch documents:", err);
      }
    }
    fetchDocuments();
  }, []);

  async function handleFileUpload(
    event: React.ChangeEvent<HTMLInputElement>
  ) {
    const file = event.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("http://localhost:8000/upload", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    console.log(data);

    // Check if response contains an error
    if (data["Error Message"]) {
      setError(`Error: ${file.name} has already been uploaded`);
      // Clear error after 5 seconds
      setTimeout(() => setError(null), 5000);
    } else {
      setError(null);
      // Refresh documents list
      const docsResponse = await fetch("http://localhost:8000/documents");
      const docsData = await docsResponse.json();
      setDocuments(docsData);
      if (docsData.length > 0) {
        setSelectedDocument(docsData[0]);
      }
    }
  }

  return (
    <main className="page-shell">
      <div className="page-header">
        <h1 className="page-title">DocuChat</h1>
      </div>

      <div className="page-frame">
        <div className="sidebar">
          <label htmlFor="file-input" className="upload-button">
            <img
              className="upload-icon"
              src="/plus-svgrepo-com.svg"
              alt="Upload File"
            />
            <span>New File</span>
          </label>

          <div className="documents-tabs">
            {documents.map((doc) => (
              <button
                key={doc}
                className={`document-tab ${selectedDocument === doc ? "active" : ""}`}
                onClick={() => setSelectedDocument(doc)}
              >
                {doc}
              </button>
            ))}
          </div>
        </div>

        <div className="page-content">
          {error && <div className="error-message">{error}</div>}

          <div className="chat-thread">
            {messages.length === 0 && !isLoading && (
              <div className="empty-state">
                Ask a question about the selected document and the answer will appear here.
              </div>
            )}

            {messages.map((message) => (
              <div
                key={message.id}
                className={`message-row ${message.role === "user" ? "user-row" : "assistant-row"}`}
              >
                <div className={`message-bubble ${message.role}`}>
                  {message.content}
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="message-row assistant-row">
                <div className="message-bubble assistant">Thinking…</div>
              </div>
            )}
          </div>

          <div className="input-container">
            <input
              type="text"
              className="message-input"
              placeholder="Type your message..."
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  e.preventDefault();
                  handleSend();
                }
              }}
            />
            <button className="send-button" onClick={handleSend}>
              <img
                src="/send-svgrepo-com.svg"
                alt="Send"
                className="send-icon"
              />
            </button>
          </div>
        </div>
      </div>

      <input
        type="file"
        id="file-input"
        onChange={handleFileUpload}
      />
    </main>
  );
}