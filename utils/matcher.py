import streamlit as st
from sentence_transformers import SentenceTransformer, util

MODEL_NAME = "all-MiniLM-L6-v2"

@st.cache_resource(show_spinner=False)
def load_model() -> SentenceTransformer:
    return SentenceTransformer(MODEL_NAME)

model = load_model()

# Define your skill keyword list
SKILL_KEYWORDS = [
    # Programming Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "go", "ruby", "kotlin", "scala",

    # Web & Frontend
    "html", "css", "react", "angular", "vue", "next.js", "tailwind", "bootstrap",

    # Backend & Frameworks
    "node.js", "express", "django", "flask", "spring", "fastapi", "graphql", "rest api", "grpc",

    # Databases
    "mysql", "postgresql", "mongodb", "redis", "sqlite", "cassandra", "dynamodb",

    # DevOps & Cloud
    "docker", "kubernetes", "aws", "azure", "gcp", "terraform", "jenkins", "github actions", "ci/cd",

    # Testing
    "pytest", "junit", "selenium", "cypress", "testng", "unittest",

    # Data & ML
    "pandas", "numpy", "matplotlib", "scikit-learn", "xgboost", "tensorflow", "pytorch", "mlflow",

    # Tools & VCS
    "git", "jira", "confluence", "notion", "linux", "bash", "shell", "vscode", "intellij",

    # Soft Skills (Optional)
    "problem solving", "communication", "collaboration", "agile", "scrum"
]

def extract_skills(text: str) -> set[str]:
    text = text.lower()
    return {skill for skill in SKILL_KEYWORDS if skill in text}

def match_score(resume_text: str, jd_text: str) -> dict[str, any]:
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    matched = resume_skills.intersection(jd_skills)
    missing = jd_skills.difference(resume_skills)

    score = round((len(matched) / len(jd_skills)) * 10, 2) if jd_skills else 0

    return {
        "score": score,
        "matched_skills": list(matched),
        "missing_skills": list(missing),
        "total_required": len(jd_skills)
    }

def semantic_match_score(resume_text: str, jd_text: str) -> float:
    resume_clean = resume_text.strip().lower()
    jd_clean = jd_text.strip().lower()

    resume_emb = model.encode(resume_clean, convert_to_tensor=True)
    jd_emb = model.encode(jd_clean, convert_to_tensor=True)

    score = util.cos_sim(resume_emb, jd_emb).item()
    return round(score * 10, 2)

def combined_score(keyword_score: float, semantic_score: float, weight: float = 0.6) -> float:
    return round((weight * semantic_score) + ((1 - weight) * keyword_score), 2)