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

🌍 Coming Soon (v2.x Roadmap)
	•	🧠 GPT-powered resume suggestions
	•	🌐 Job scraping from LinkedIn/Naukri
	•	📊 User dashboard
	•	🛠 Deploy to Hugging Face / Render / Streamlit Cloud

