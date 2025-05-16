# 🚀 Enterprise RAG Platform (Multimodal AI Assistant)

This is an enterprise-level Retrieval-Augmented Generation (RAG) platform built for multimodal document understanding and secure cloud deployment. The system combines structured and unstructured retrieval from PDF, CSV, and visual content, and supports AI-driven responses with context-aware source traceability.

---

## 🔧 Features

- ✅ **Multimodal RAG**: Extracts and reasons over text, tables, and figures (via BLIP captions).
- ✅ **OpenAI-Powered**: Uses GPT-4 for advanced reasoning and source-grounded generation.
- ✅ **Cloud-First Storage**: Embeddings, vector DBs, and input files are stored on **Azure Blob**.
- ✅ **Dockerized**: Easily containerized for development or production workloads.
- ✅ **CI/CD via GitHub Actions**: Automated build and deployment to Azure Web Apps or AKS.
- ✅ **Streamlit UI**: Interactive, brandable interface with figure preview on hover.

---

## 🗂️ Project Structure

├── app/ # Agents, orchestrator, vector store logic
├── ui/app.py # Streamlit UI with session-aware chat and image sources
├── static/ # Generated figure images (referenced in chat)
├── vector_db/ # FAISS index and metadata
├── blob_utils.py # Azure Blob upload/download utility
├── Dockerfile # Container configuration
├── requirements.txt # Python dependencies
├── .env # Secrets (OpenAI key, Azure connection string)
├── .github/
│ └── workflows/
│ └── docker-azure-deploy.yml # GitHub Actions pipeline

yaml
Copy

---

## 🚀 Quick Start

### 🔐 1. Setup `.env`

```bash
OPENAI_API_KEY=your-openai-key
AZURE_STORAGE_CONNECTION_STRING=your-azure-blob-conn-string
ENV=production
🧱 2. Build and Run Locally (Docker)
bash
Copy
docker build -t enterprise-rag .
docker run -p 8501:8501 --env-file .env enterprise-rag
Access at http://localhost:8501

🧪 3. Run Without Docker (Dev Mode)
bash
Copy
pip install -r requirements.txt
streamlit run ui/app.py
☁️ 4. Azure Deployment (via GitHub Actions)
Create an Azure Container Registry (ACR) and Web App for Containers.

Set these secrets in GitHub:

AZURE_ACR_USERNAME

AZURE_ACR_PASSWORD

AZURE_WEBAPP_PUBLISH_PROFILE

Push to main branch:

bash
Copy
git push origin main
GitHub will:

Build Docker image

Push to ACR

Deploy to Azure App Service

📦 Vector Indexing Pipeline
You can build vector DBs from PDFs with image captions using BLIP:

python
Copy
from chunker_multimodal import extract_text_and_images
from build_vector_db import build_multimodal_vector_db

build_multimodal_vector_db("Equinor_Report.pdf", "equinor_multimodal")
Stores:

vector_db/equinor_multimodal_index.faiss

*_chunks.pkl and *_meta.pkl

🧠 Agent Routing
agent_pdf.py: for text-only PDF documents

agent_csv.py: for structured data

agent_multimodal.py: for figures + text + captions

orchestrator.py: decides which agent to invoke

📊 Sources + Traceability
The app returns:

🔹 Page number

🔹 Chunk type (text, figure)

🔹 Snippet preview

🔹 Optional figure preview (on hover or expand)

✅ Tech Stack
Python 3.10

OpenAI GPT-4

Streamlit

FAISS

Azure Blob Storage

GitHub Actions + Azure Web App (Linux Container)

📄 License
Enterprise use only. For internal demo and POC deployments under NDA or client engagements.

🤝 Credits
Built by NexTurn | Demo client: Equinor
Contributors:
Shivakrishna
Sadhvija