import streamlit as st
from utils.parser import load_resume
from utils.matcher import match_score, semantic_match_score
import tempfile
import pandas as pd

if "match_history" not in st.session_state:
    st.session_state.match_history = []

st.set_page_config(page_title="ApplyGPT", layout="centered")
st.title("📄 ApplyGPT – Resume vs JD Matching")

# Upload Resume
uploaded_file = st.file_uploader("Upload Resume (.docx)", type=["docx"])

# Paste JD
jd_text = st.text_area("Paste Job Description", height=200)

# Only show button if both inputs are provided
if uploaded_file and jd_text:
    if st.button("Check Match 🔍"):
        # Save resume temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp.write(uploaded_file.read())
            resume_text = load_resume(tmp.name)

        with st.spinner("🔍 Scoring in progress..."):
            # Run match scoring
            keyword_result = match_score(resume_text, jd_text)
            semantic_score = semantic_match_score(resume_text, jd_text)

        # Append result to match history
        st.session_state.match_history.append({
            "Keyword Score": keyword_result["score"],
            "Semantic Score": semantic_score,
            "Matched Skills": ", ".join(keyword_result["matched_skills"]),
            "Missing Skills": ", ".join(keyword_result["missing_skills"]),
        })

        # Display Results
        st.subheader("📊 Match Results")
        col1, col2 = st.columns(2)
        col1.metric("Keyword Score", f"{keyword_result['score']} / 10")
        col2.metric("Semantic Score", f"{semantic_score} / 10")

        st.success(f"✅ Matched Skills: {', '.join(keyword_result['matched_skills']) or 'None'}")
        st.warning(f"❌ Missing Skills: {', '.join(keyword_result['missing_skills']) or 'None'}")

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