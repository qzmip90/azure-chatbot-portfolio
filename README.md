# Quest Bot 4o 🤖💬

An interactive, lightweight chatbot built with **Flask**, **Azure OpenAI**, and **Azure Blob Storage**, designed to simulate helpful assistant conversations in a stylish, web-based UI. This project demonstrates cloud deployment, prompt engineering, user feedback capture, and CI/CD readiness.

---

## 🌟 Features

- ✅ **Live chat interface** using Flask backend + HTML/CSS frontend
- 🧠 **Azure OpenAI integration** (GPT model)
- 💾 **User feedback logging** to Azure Blob Storage (thumbs up/down)
- 🧰 **Environment configuration** with `.env` file
- 🔄 **Context-aware chat** with tracked message history
- 📦 **Deployable** on Azure App Service & GitHub Pages / Azure Static Web Apps

---

## 🧱 Tech Stack

| Layer       | Tech                        |
|-------------|-----------------------------|
| Frontend    | HTML, CSS, JavaScript       |
| Backend     | Python, Flask, Flask-CORS   |
| AI Engine   | Azure OpenAI Service (GPT)  |
| Storage     | Azure Blob Storage          |
| Deployment  | Azure App Service (Backend) |
| DevOps      | GitHub Actions (CI/CD)      |

---

## 🚀 Live Demo

> Coming soon

---

## 📁 Project Structure

```bash
azure-chatbot-portfolio/
├── backend/
│   ├── app.py                 # Flask backend API
│   ├── requirements.txt       # Python dependencies
│   └── .env.example           # Example env vars
├── frontend/
│   └── index.html             # Stylish chatbot UI
├── .gitignore
├── README.md
```

---

## ⚙️ Getting Started (Local)

### 1. Clone the repo
```bash
git clone https://github.com/qzmip90/azure-chatbot-portfolio.git
cd azure-chatbot-portfolio
```

### 2. Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Fill in your Azure OpenAI + Blob Storage keys in .env
python app.py
```

### 3. Frontend
Simply open `frontend/index.html` in a browser (will call backend at `localhost:5000`).

---

## ☁️ Azure Deployment

### 1. Azure OpenAI Setup
- Create Azure OpenAI Resource
- Deploy GPT model (e.g., `gpt-4o`)
- Note endpoint & key for `.env`

### 2. Azure Blob Storage Setup
- Create Storage Account + Container
- Get account name & key

### 3. Deploy Backend to Azure App Service
- Use Azure CLI or Portal
- Set environment variables in App Service config

### 4. Optional CI/CD with GitHub Actions
- Auto-deploy on push
- See `.github/workflows/` examples

---

## 🔐 Environment Variables (`.env`)
```env
OPENAI_API_KEY=...
OPENAI_API_BASE=...
DEPLOYMENT_NAME=...
AZURE_STORAGE_ACCOUNT_NAME=...
AZURE_STORAGE_ACCOUNT_KEY=...
AZURE_STORAGE_CONTAINER_NAME=...
```