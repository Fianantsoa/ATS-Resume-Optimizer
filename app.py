"""Streamlit UI for ATS Resume Optimizer."""

from __future__ import annotations

import streamlit as st

from services.ats_service import ATSService
from utils.file_handler import FileHandlingError, read_bytes


st.set_page_config(page_title="ATS Resume Optimizer", layout="wide")

st.title("ATS Resume Optimizer")
st.caption("Upload your resume and compare it with a job description in seconds.")


@st.cache_data(show_spinner=False)
def analyze_resume(file_bytes: bytes, filename: str, job_description: str) -> dict:
    service = ATSService()
    return service.analyze_file(file_bytes, filename, job_description).to_dict()


with st.container():
    left, right = st.columns(2)
    with left:
        uploaded_file = st.file_uploader(
            "Upload your resume (PDF or TXT)", type=["pdf", "txt"]
        )
    with right:
        job_description = st.text_area(
            "Paste the job description",
            height=220,
            placeholder="Paste the job requirements and responsibilities here...",
        )

optimize_clicked = st.button("Optimize Resume")

if optimize_clicked:
    if not uploaded_file or not job_description.strip():
        st.warning("Please upload a resume and provide a job description.")
    else:
        with st.spinner("Analyzing resume..."):
            try:
                file_bytes = read_bytes(uploaded_file)
                results = analyze_resume(
                    file_bytes, uploaded_file.name, job_description
                )
                st.session_state["results"] = results
            except FileHandlingError as exc:
                st.error(str(exc))
            except Exception:  # noqa: BLE001
                st.error(
                    "An error occurred while processing your resume. "
                    "Please ensure the file is valid and try again."
                )

results = st.session_state.get("results")
if results:
    st.divider()
    score_column, keywords_column = st.columns([1, 2])
    with score_column:
        st.metric("ATS Score", f"{results['score']} / 100")
    with keywords_column:
        st.subheader("Missing Keywords")
        if results["missing_keywords"]:
            st.markdown("\n".join(f"- {kw}" for kw in results["missing_keywords"]))
        else:
            st.write("Great job! No critical keywords are missing.")

    st.subheader("Improvement Suggestions")
    st.markdown("\n".join(f"- {item}" for item in results["suggestions"]))

    st.subheader("Optimized CV")
    st.text_area(
        "", value=results["optimized_cv"], height=320, label_visibility="collapsed"
    )
