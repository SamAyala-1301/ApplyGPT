import streamlit as st
from utils.parser import load_resume
from utils.matcher import match_score, semantic_match_score
from utils.llm_handler import query_llm
from utils.scraper import scrape_naukri_jobs
import tempfile
import pandas as pd
import json
import os


def load_job_list():
    if "job_list" not in st.session_state:
        return None, None
    job_list = st.session_state["job_list"]
    st.sidebar.header("📌 Select a Job to Match")
    job_titles = [f"{job['title']} at {job['company']} ({job['location']})" for job in job_list]
    selected_job_idx = st.sidebar.selectbox("Choose a job", range(len(job_list)), format_func=lambda i: job_titles[i])
    return job_list[selected_job_idx], job_list


st.sidebar.markdown("### 🔍 Search Job Role (Live Scrape)")
search_query = st.sidebar.text_input("Enter a job title (e.g., Support Engineer)")
if st.sidebar.button("Search Now"):
    with st.spinner("Searching Naukri..."):
        scraped_jobs = scrape_naukri_jobs(search_query)

    if scraped_jobs:
        st.session_state["job_list"] = scraped_jobs
        st.success(f"✅ Found {len(scraped_jobs)} jobs for '{search_query}'")
        st.rerun()
    else:
        st.warning(f"🔒 Naukri is not allowing scraping for '{search_query}'. Please try a more specific role.")

# Optional: File uploader to upload job JSON
import json
uploaded_jobs_file = st.sidebar.file_uploader("Or upload jobs JSON manually", type=["json"])
if uploaded_jobs_file and "job_list" not in st.session_state:
    job_list = json.load(uploaded_jobs_file)
    st.session_state["job_list"] = job_list
    st.sidebar.success("✅ Job data loaded.")


def display_selected_job(selected_job):
    st.subheader("📄 Job Description Preview")
    st.markdown(f"**🔹 Title:** {selected_job['title']}")
    st.markdown(f"**🏢 Company:** {selected_job['company']} | **📍 Location:** {selected_job['location']}")
    st.markdown(f"**🔗 Job Link:** [{selected_job['link']}]({selected_job['link']})")
    st.markdown("---")
    st.markdown(selected_job["jd"])


def handle_resume_upload(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
        tmp.write(uploaded_file.read())
        file_ext = os.path.splitext(uploaded_file.name)[1].lower()
        resume_text = load_resume(tmp.name, file_ext)
    return resume_text


def run_resume_matching(resume_text, jd_text):
    with st.spinner("🔍 Scoring in progress..."):
        keyword_result = match_score(resume_text, jd_text)
        semantic_score = semantic_match_score(resume_text, jd_text)

    st.session_state.match_history.append({
        "Keyword Score": keyword_result["score"],
        "Semantic Score": semantic_score,
        "Matched Skills": ", ".join(keyword_result["matched_skills"]),
        "Missing Skills": ", ".join(keyword_result["missing_skills"]),
    })

    st.subheader("📊 Match Results")
    col1, col2 = st.columns(2)
    col1.metric("Keyword Score", f"{keyword_result['score']} / 10")
    col2.metric("Semantic Similarity", f"{semantic_score} / 10")

    st.success(f"✅ Matched Skills: {', '.join(keyword_result['matched_skills']) or 'None'}")
    st.warning(f"❌ Missing Skills: {', '.join(keyword_result['missing_skills']) or 'None'}")

def suggest_resume_lines(jd_text):
    st.subheader("✍️ Enhance My Resume for Selected Job")
    uploaded_file = st.session_state.get("uploaded_file", None)
    selected_job = None
    if "job_list" in st.session_state:
        selected_job = st.session_state.get("selected_job", None)

    if uploaded_file:
        if st.button("Suggest Resume Lines for This Job"):
            with st.spinner("Crafting smart resume lines for selected JD..."):
                enhancement_prompt = f"""
You are a helpful resume assistant. Given the following job description, suggest 3 impactful bullet points that I can add to my resume to match this role better.

Make them achievement-driven, specific, and skill-oriented.

Job Description:
\"\"\"
{jd_text}
\"\"\"
                """.strip()

                suggestions = query_llm(enhancement_prompt, use_local=False)
                st.markdown("### ✍️ Suggested Lines:")
                st.markdown(suggestions)
                st.code(suggestions, language="markdown")
                st.session_state.llm_log.append({
                    "Prompt": enhancement_prompt,
                    "LLM Output": suggestions,
                    "Job Title": selected_job["title"] if selected_job else None,
                    "Company": selected_job["company"] if selected_job else None
                })
    else:
        st.info("Upload a resume to get tailored suggestions.")

def run_bulk_matching(resume_text, job_list):
    results = []
    for job in job_list:
        keyword_result = match_score(resume_text, job["jd"])
        semantic_score = semantic_match_score(resume_text, job["jd"])
        total_score = round((keyword_result["score"] + semantic_score) / 2, 2)
        results.append({
            "Title": job["title"],
            "Company": job["company"],
            "Location": job["location"],
            "Keyword Score": keyword_result["score"],
            "Semantic Score": semantic_score,
            "Total Score": total_score,
            "Link": job["link"],
            "JD": job["jd"]
        })
    results_df = pd.DataFrame(results).sort_values(by="Total Score", ascending=False).reset_index(drop=True)
    return results_df

def generate_bulk_resume_lines(top_matches_df, selected_titles):
    st.subheader("✍️ LLM Resume Line Suggestions for Top Matches")
    for title in selected_titles:
        job_row = top_matches_df[top_matches_df["Title"] == title].iloc[0]
        job_title = job_row["Title"]
        company = job_row["Company"]
        jd_text = job_row["JD"]
        with st.spinner(f"Generating resume lines for {job_title} at {company}..."):
            enhancement_prompt = f"""
You are a helpful resume assistant. Given the following job description, suggest 3 impactful bullet points that I can add to my resume to match this role better.

Make them achievement-driven, specific, and skill-oriented.

Job Description:
\"\"\"
{jd_text}
\"\"\"
            """.strip()
            suggestions = query_llm(enhancement_prompt, use_local=False)
            st.markdown(f"### {job_title} at {company}")
            st.markdown(suggestions)
            st.code(suggestions, language="markdown")
            st.session_state.llm_log.append({
                "Prompt": enhancement_prompt,
                "LLM Output": suggestions,
                "Job Title": job_title,
                "Company": company
            })

if "match_history" not in st.session_state:
    st.session_state.match_history = []

if "llm_log" not in st.session_state:
    st.session_state.llm_log = []

st.set_page_config(page_title="ApplyGPT", layout="centered")
st.title("📄 ApplyGPT – Resume vs JD Matching")

# Job Selection
selected_job, job_list = load_job_list()
if selected_job and job_list:
    display_selected_job(selected_job)

match_mode = st.radio("Select Matching Mode", ["Paste JD Manually", "Bulk Match with All Jobs"])
st.session_state["match_mode"] = match_mode

# Resume Upload
uploaded_file = st.file_uploader("Upload Resume (.docx, .pdf, .txt)", type=["docx", "pdf", "txt"])
st.session_state["uploaded_file"] = uploaded_file

if match_mode == "Paste JD Manually":
    # Paste JD
    jd_text = st.text_area("Paste Job Description", height=200)

    # Match Scoring
    if uploaded_file and jd_text:
        if st.button("🔍 Match My Resume to This JD"):
            resume_text = handle_resume_upload(uploaded_file)
            run_resume_matching(resume_text, jd_text)

elif match_mode == "Bulk Match with All Jobs":
    # Bulk Matcher
    if uploaded_file and job_list:
        st.subheader("📊 Best Matching Jobs for Your Resume")
        resume_text = handle_resume_upload(uploaded_file)
        top_matches_df = run_bulk_matching(resume_text, job_list)
        st.dataframe(top_matches_df)

        selected_titles = st.multiselect(
            "Select jobs to get resume line suggestions for:",
            options=top_matches_df["Title"].tolist()
        )

        if selected_titles:
            generate_bulk_resume_lines(top_matches_df, selected_titles)

# Display Match History and Export
if st.session_state.match_history:
    st.subheader("📚 Match History (This Session)")
    st.dataframe(st.session_state.match_history)

    df = pd.DataFrame(st.session_state.match_history)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Match History as CSV",
        data=csv,
        file_name="applygpt_match_history.csv",
        mime="text/csv",
    )
else:
    st.info("📂 Upload your resume and paste JD to enable scoring.")



# Resume Lines Enhancement
enhance_mode = None
jd_source_text = None

if match_mode == "Paste JD Manually":
    jd_source_text = jd_text if "jd_text" in locals() else None
    enhance_mode = "manual"
elif selected_job:
    jd_source_text = selected_job["jd"]
    enhance_mode = "job"

if uploaded_file:
    if jd_source_text:
        st.subheader("✍️ Enhance My Resume")
        if st.button("Suggest Resume Lines"):
            with st.spinner("Crafting smart resume lines..."):
                enhancement_prompt = f"""
You are a helpful resume assistant. Given the following job description, suggest 3 impactful bullet points that I can add to my resume to match this role better.

Make them achievement-driven, specific, and skill-oriented.

Job Description:
\"\"\"
{jd_source_text}
\"\"\"
                """.strip()
                suggestions = query_llm(enhancement_prompt, use_local=False)
                st.markdown("### ✍️ Suggested Lines:")
                st.markdown(suggestions)
                st.code(suggestions, language="markdown")
                st.session_state.llm_log.append({
                    "Prompt": enhancement_prompt,
                    "LLM Output": suggestions,
                    "Job Title": selected_job["title"] if selected_job else None,
                    "Company": selected_job["company"] if selected_job else None
                })
    else:
        st.info("Paste a job description or select a job from the list to enable suggestions.")

with st.expander("🧠 Prompt + LLM Response Log"):
    if st.session_state.llm_log:
        for i, log_entry in enumerate(st.session_state.llm_log, 1):
            st.markdown(f"**Entry {i}:**")
            if log_entry.get("Job Title") and log_entry.get("Company"):
                st.markdown(f"- **Job Title:** {log_entry['Job Title']}")
                st.markdown(f"- **Company:** {log_entry['Company']}")
            st.markdown(f"- **Prompt:**\n```\n{log_entry['Prompt']}\n```")
            st.markdown(f"- **LLM Output:**\n```\n{log_entry['LLM Output']}\n```")
            st.markdown("---")
    else:
        st.write("No LLM prompt and response logs yet.")