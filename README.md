# ⚡ ApplyGPT – Intelligent Resume Matcher (v2.0)

ApplyGPT is your personal AI copilot for job applications. Match resumes to job descriptions using keyword + semantic similarity, generate bullet points using LLMs, and even scrape job listings in real time!

---

## 🌟 Core Features (v1.0)

- 📤 Upload `.docx` resume
- 📋 Paste any job description (JD)
- 🔍 Dual scoring:
  - ✅ **Keyword Score** – based on hard skill matches
  - 🧠 **Semantic Score** – powered by `SentenceTransformer`
- 📊 Real-time score display (0–10 scale)
- 📚 Match history (session-based)
- 📥 Export match history as CSV
- ⚡ Fast, reactive UI with model caching

---

## 🧠 How Matching Works

1. Resume and JD are parsed into plain text
2. Tech skills are extracted using predefined list
3. Semantic similarity is calculated with `all-MiniLM-L6-v2`
4. Both scores displayed with detailed feedback

---

## 🗂️ Project Structure

```
applygpt/
├── app.py
├── README.md
├── requirements.txt
├── utils/
│   ├── parser.py
│   ├── matcher.py
│   └── llm_handler.py
├── data/
│   └── jobs_sample.json
├── assets/                # (screenshots/logos)
│   └── preview.png
├── .streamlit/            # (theme/secrets config)
│   └── config.toml
```

---

## 🛠 Installation Guide

```bash
# 1. Clone the repo
git clone https://github.com/SamAyala-1301/ApplyGPT.git
cd applygpt

# 2. Setup virtual environment
python3 -m venv applygpt-venv
source applygpt-venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

---

## 📘 Version Info

**This is v1.0** — Initial MVP with resume/JD scoring and match history export.

---

# 🚀 ApplyGPT v2.0 — LLMs, Job Scraping & Resume Generation

ApplyGPT v2 brings massive upgrades, making it a smarter, more production-ready tool.

---

## 🔄 What’s New in v2.0

### 🧠 2.1 — LLM-Powered Resume Suggestions
- ✍️ Generate bullet points tailored to any JD
- 🧠 Uses **LLaMA 3 (local)** and **Mistral (via HF API)**
- 📦 Bulk resume generation for all scraped roles

### 📂 2.2 — Multi-format Resume Support
- Accepts `.docx`, `.pdf`, `.txt`
- Uses `docx2txt`, `PyMuPDF`, and `python-docx` parsers

### 🧮 2.3 — Dual Match Modes
- 📋 Manual JD input
- 🗂 Bulk match against scraped job list
- 🔄 Toggle between both in-app

### 🛠️ 2.4 — Smart Suggestions UX
- 🎯 Filter top-matched roles
- 🧵 Multi-select and log LLM suggestions
- 📜 Full prompt + response log included

### 🌐 2.5 — Real-Time Job Scraping
- 🔎 Fetch jobs live from **Naukri.com**
- 🧾 Sidebar-based job search
- ☁️ JSON upload fallback for scraping issues

### 🤖 2.6 — HuggingFace API Integration
- Uses `mistralai/Mistral-7B-Instruct-v0.2`
- 🔐 Token managed via `.env` or Streamlit secrets
- 💡 Runs on cloud without local GPU

---

## 📦 Ready for Deployment

ApplyGPT v2 can be deployed on:
- ✅ **Streamlit Cloud**
- ✅ **Hugging Face Spaces**
- 🛠️ Render (WIP)

All models, dependencies, and keys are cloud-compatible.

---

## 🧭 Roadmap (v3.0 Preview)

- 🧰 SaaS backend with user accounts
- 📊 Dashboards + resume logs
- 📤 Scheduled resume submissions
- 💬 GPT chat over resume feedback

---

## 📬 Contact

Built by **Sai Sampath Ayalasomayajula**  
🔗 [LinkedIn](https://www.linkedin.com/in/sampath-ayala/) • ✉️ arg5506@gmail.com

---

## 🪪 License

MIT License

---

## 🏷️ Tags

`#resume-matching` `#LLM` `#streamlit` `#AI` `#career-tools` `#job-search`
