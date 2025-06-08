# 📄 Document Processor API (FastAPI)

A FastAPI application providing a RESTful API to process and analyze documents using a flexible registry of processors. Ideal for AI-based extraction and document understanding workflows.

---

## 🚀 Features

- 📁 Process documents using a dynamic processor registry
- ⚙️ Support for multiple job types (`extract`, `analyze`, etc.)
- 🧠 Optional structured data extraction using schemas
- ✅ Robust error handling and logging

---

## 📡 API Endpoints

### `POST /process`

Process a document using the specified job type.

#### 🔷 Request Body

```json
{
  "job_type": "extract",
  "file_name": "document.pdf",
  "file_content": "<base64-encoded or raw text>",
  "extraction_schema": [ 
    {
      "field": "Company Name",
      "type": "string"
    }
  ]
}
```

job_type (string): The type of job to perform (extract, analyze, etc.)

file_name (string): The name of the file to process

file_content (string): Raw or encoded content of the file

extraction_schema (optional): JSON schema defining fields to extract

🟢 Response
```json
{
  "status": "success",
  "result": {
    "Company Name": "Acme Corp"
  }
}
```

status: "success" or "error"

result: Output of the job (extracted fields, analysis results, etc.)

🛠️ Processors
Custom processors are registered in app/src/orchestrators/registry.py. Each processor maps a job_type to a specific document-handling strategy.

📦 Dependencies
FastAPI

Pydantic

OpenAI

Instructor (for structured output parsing)

▶️ Running the App
bash
Copiar
Editar
uvicorn main:app --host 0.0.0.0 --port 5000
By default, the API will be available at: http://localhost:5000

🧪 Testing
Run all tests using:

bash
Copiar
Editar
pytest