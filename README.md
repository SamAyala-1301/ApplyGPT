# ApplyGPT v1.0

ApplyGPT is an intelligent resume–job description matcher built using Python and Streamlit. It combines keyword-based skill matching with semantic similarity (via Sentence Transformers) to evaluate how well a resume aligns with a given job description.

---

## 🚀 Features

- 📤 Upload `.docx` resume
- 📋 Paste any job description (JD)
- 🔍 Dual scoring:
  - **Keyword Score**: Matches explicit tech skills
  - **Semantic Score**: Captures meaning/context using `all-MiniLM-L6-v2`
- 📊 Combined results with skill breakdown
- 📚 Match history (stored per session)
- 📥 Download match history as CSV
- ⚡ Fast UI with model caching

---

## 🧠 How It Works

1. Resume and JD are parsed into plain text
2. Keyword matcher extracts predefined tech skills
3. Semantic scorer encodes both texts via `SentenceTransformer`
4. Results are scored from 0–10 and shown in real-time

---

## 📂 Project Structure
applygpt/
├── app.py
├── README.md
├── requirements.txt
├── utils/
│   ├── parser.py
│   └── matcher.py
├── assets/                # (optional for screenshots or logos)
│   └── preview.png
├── .streamlit/            # (only if customizing theme)
│   └── config.toml

---

## 🛠 Installation

```bash
# Clone the repo
git clone https://github.com/SamAyala-1301/ApplyGPT.git
cd applygpt

# Create and activate virtual environment
python3 -m venv applygpt-venv
source applygpt-venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py

📄 License

MIT License

⸻

🔖 Version

This is v1.0 — public MVP version with full UI, scoring engine, and CSV export.

⸻

📬 Contact

Built by Sai Sampath Ayalasomayajula

⸻


---

# 🚀 ApplyGPT v2.0 — Feature Expansion & Intelligence Upgrade

ApplyGPT v2 brings major upgrades across resume matching, LLM integration, and job intelligence features — evolving it into a smarter, more production-ready tool.

---

## 🔄 What's New in v2.0

### 🧠 2.1 — LLM-Based Resume Enhancement
- Integrated **LLaMA-3** (locally) and **Mistral via HuggingFace API**
- Automatically suggests bullet points tailored to a job description
- Bulk suggestion for multiple jobs now supported

### 📂 2.2 — Multi-format Resume Upload
- Support for `.docx`, `.pdf`, and `.txt` files
- Backend parsing handled by `docx2txt`, `PyMuPDF`, and `python-docx`

### 🔍 2.3 — Enhanced Matching Modes
- Choose between:
  - 📋 Manual JD input
  - 🗃️ Bulk match against all scraped jobs
- Clean UI toggle implemented

### ✍️ 2.4 — Resume Suggestions + Matching UX
- 2.4.1: View top matches from scraped roles
- 2.4.2: Multi-select roles to generate LLM resume lines
- 2.4.3: Output shown inline with job metadata
- 2.4.4: Full **prompt + LLM response** log added to session

### 🌐 2.5 — Job Scraping Integration
- Live Naukri job scraping via `requests + BeautifulSoup`
- Sidebar input to fetch job postings for any title
- Fallback to `.json` upload when scraping fails
- No sample data used unless explicitly uploaded

### 🤖 2.6 — HuggingFace API LLM Integration
- Uses `mistralai/Mistral-7B-Instruct-v0.2` from HuggingFace
- API key handled via environment or Streamlit secrets
- Seamless switch from local model to API deployment mode

---

## 📦 Deployment Ready

You can now deploy ApplyGPT v2 to:
- ✅ Streamlit Cloud
- ✅ Hugging Face Spaces
- ✅ Render (coming soon)

All secrets, dependencies, and models are cloud-compatible.

---

## 🏁 Next Up (v3.0 Preview)

- 🧰 SaaS-Ready Backend
- 📈 User accounts + dashboards
- 📤 Resume submission log + job alerts
- 💬 GPT chat over resumes + JDs

