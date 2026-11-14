# AI Business Intelligence & Research Assistant

An AI-powered business intelligence platform for sales-data analysis, document Q&A, forecasting, external research, PDF reporting, and email notifications.

<!-- Add a screenshot or GIF here, for example: -->
<!-- ![App screenshot](docs/screenshot.png) -->

## Live Application

- **React frontend (Vercel):** 
https://ai-business-intelligence-assistant-ebon.vercel.app/
- **JavaScript backend, Node.js / Express (Render):** 
https://ai-business-intelligence-backend-5pi3.onrender.com
- **Python AI backend, FastAPI / Uvicorn (Render):** 
https://ai-business-intelligence-python.onrender.com

> The backends run on Render's free tier, so the first request after a period of inactivity can take 30 to 60 seconds while the service wakes up.

## Architecture

```
React Frontend (Vercel)
        |
        v
JavaScript Backend (Node.js / Express, Render)
        |
        +-- aiRoutes
        +-- uploadRoutes
        |
        v
Python AI Backend (FastAPI + Uvicorn, Render)
        |
        v
LangGraph ReAct Agent
        |
        +-- Data Analysis Tool
        +-- Business Insights Tool
        +-- Prediction Tool
        +-- RAG Tool (ChromaDB)
        +-- Web Search / News Search
        +-- Email Notification Tool (Resend)
```

### Responsibilities

- **React frontend:** User interface for uploads, questions, and streamed responses.
- **JavaScript backend:** Node.js / Express API layer, including `aiRoutes` and `uploadRoutes`.
- **Python AI backend:** FastAPI application served with Uvicorn. Runs the LangGraph agent, RAG, data analysis, business insights, forecasting, PDF report generation, research, and email tools.

### How the agent chooses tools

| Request | Tool |
| --- | --- |
| Individual calculations on an Excel/CSV file | Data Analysis Tool |
| Complete historical business assessment | Business Insights Tool |
| Future forecasting | Prediction Tool |
| Historical + forecast request | Business Insights Tool + Prediction Tool |
| Questions about an uploaded PDF | RAG Tool |
| External company or market research | Web Search |
| Latest news | News Search |
| Important findings by email | Email Notification Tool |
| Downloadable historical PDF report | Business Insights Tool (PDF enabled) |

## Features

- Excel/CSV sales analysis: revenue, profit, margins, averages, and performance breakdowns.
- Historical business insights, trends, risks, and recommendations.
- Separate model-based forecasting tool.
- PDF document Q&A using RAG, embeddings, and ChromaDB.
- LangGraph ReAct agent with automatic tool selection.
- External web and recent-news research.
- Downloadable historical business PDF reports.
- Email notifications through Resend.

## Technology Stack

- **Frontend:** React.js, Vite
- **JavaScript backend:** Node.js, Express.js
- **Python AI backend:** Python, FastAPI, Uvicorn
- **AI orchestration:** LangChain, LangGraph, ReAct agents
- **RAG / vector storage:** ChromaDB, embeddings
- **Data and forecasting:** Pandas, Statsmodels
- **Reports / visualization:** ReportLab, Matplotlib
- **Research:** Tavily
- **Email:** Resend API (Gmail SMTP fallback for local development)
- **Deployment:** Vercel and Render

## Forecasting Method

Forecasts use Holt-Winters exponential smoothing from Statsmodels, with a damped additive trend when there is enough history. The lower and upper ranges are approximate estimates based on historical model errors. They are **not** formal statistical confidence intervals. Forecasts are model-based estimates, not guarantees.

## Repository Structure

The following structure reflects the folders and files visible in the project workspace. Some directories may contain additional files that are not shown here.

```
AI-Business-Intelligence-Assistant/
├── backend/                         # Node.js / Express backend
│   ├── middleware/
│   ├── routes/
│   ├── package.json
│   ├── package-lock.json
│   └── server.js
│
├── chroma_db/                       # ChromaDB data directory
├── docs/                            # Project documentation
│
├── frontend/                        # React + Vite frontend
│   ├── src/
│   │   ├── components/
│   │   ├── styles/
│   │   ├── App.css
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   ├── .gitignore
│   ├── eslint.config.js
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── python_ai/                       # Python AI backend
│   ├── agents/
│   ├── app/
│   ├── document_processors/
│   ├── embeddings/
│   ├── loaders/
│   ├── retrievers/
│   ├── services/
│   ├── tools/
│   ├── utils/
│   ├── vector_store/
│   ├── api.py
│   ├── main.py
│   └── requirements.txt
│
├── .gitignore
└── README.md
```

`node_modules/`, `.venv/`, and `__pycache__/` are local or generated directories and are intentionally excluded from this overview. Make sure these are ignored by your `.gitignore` files and are not committed to GitHub.

## Run Locally

### 1. Python AI backend

Open a terminal in the project root:

```bash
cd python_ai
python -m venv .venv
```

Activate the environment.

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
source .venv/bin/activate
```

Install the Python dependencies and start the API:

```bash
pip install -r requirements.txt
python -m uvicorn api:app --reload
```

API documentation: http://127.0.0.1:8000/docs

### 2. JavaScript backend

Open a separate terminal:

```bash
cd backend
npm install
node server.js
```

Use the start script defined in `backend/package.json` if your project uses a different command.

### 3. React frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Configure the frontend to call the JavaScript backend, and the JavaScript backend to call the Python AI service. Use the appropriate local service URLs in your environment configuration.

## Environment Variables

Create a local `.env` file in `python_ai/` and add the keys required by the Python AI service:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
RESEND_API_KEY=your_resend_api_key
NOTIFICATION_EMAIL=recipient_email_address

# Optional: sender address for Resend.
# Defaults to onboarding@resend.dev. Change only after verifying your own domain.
EMAIL_FROM=onboarding@resend.dev

# Optional, local development only: Gmail SMTP fallback.
# Used when RESEND_API_KEY is empty. Use a Gmail app password.
EMAIL_ADDRESS=your_gmail_address
EMAIL_APP_PASSWORD=your_gmail_app_password
```

Add any additional environment variables required by the frontend and Node.js backend in their respective local environment files. Set production values in the Render and Vercel environment settings.

**Never commit `.env` files, API keys, or passwords.**

### Email notes

- On Render's free tier, outbound SMTP ports are blocked, so email is sent through the Resend HTTP API.
- Without a verified domain, Resend delivers only to the email address that owns the Resend account. To send to other recipients, verify a domain in Resend and set `EMAIL_FROM` to an address on that domain.

## Deployment

- **React frontend:** Vercel.
- **Node.js / Express backend:** Render.
- **Python FastAPI / Uvicorn AI backend:** Render.

Configure each service with its required environment variables and service URLs, then test file upload, analysis, forecasting, document Q&A, PDF reports, and email delivery.

## Limitations

- The business analysis runs Python (pandas) code generated by an LLM using `exec`. This is suitable for development and demos. Run that code in an isolated sandbox before exposing the app to untrusted public users.
- PDF reports currently contain historical analysis only. Forecasts are not included in the PDF.
- Render's free tier uses temporary storage, so uploaded files and vector data may be lost when the service restarts or redeploys.
- Results depend on uploaded data quality and on the configured model and search providers.

## License

No license has been specified yet. Add a `LICENSE` file (for example, MIT) before distributing this repository as open source.
