import streamlit as st
from utils import extract_text_from_pdf
from analyzer import (
    analyze_resume,
    match_resume_with_jd,
    company_analysis,
    improve_resume,
    generate_cover_letter,
    generate_interview_questions,
    generate_learning_roadmap,
    role_fit_analysis,
    clean_json
)
import json
from report_generator import generate_pdf
from utils import extract_text_from_pdf, resume_statistics
from doc_generator import create_docx
# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="ResumeLens AI",
    page_icon="📄",
    layout="wide"
)
def load_css():
    with open("styles.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

# ---------------- SIDEBAR ---------------- #
with st.sidebar:
    st.title("📄 ResumeLens AI")
    st.write("AI-Powered Resume Analyzer")

    st.divider()

    st.markdown("""
### Features
✅ Resume Summary

✅ ATS Score

✅ Skills Extraction

✅ Resume Feedback

✅ Job Description Matching
""")

    st.divider()

    st.info("Upload your resume to get started.")

# ---------------- MAIN PAGE ---------------- #

st.title("📄 ResumeLens AI")
st.subheader("AI-Powered Resume Analysis & ATS Checker")

st.write(
    "Upload your resume in PDF format and get instant AI-powered insights."
)

st.divider()

uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

if uploaded_file:

    st.success("✅ Resume uploaded successfully!")

    st.write("**Filename:**", uploaded_file.name)
    st.write("**Size:**", round(uploaded_file.size / 1024, 2), "KB")

    st.divider()

    resume_text = extract_text_from_pdf(uploaded_file)
    st.subheader("📄 Extracted Resume Text")

    st.text_area(
        "Resume Content",
        resume_text,
        height=350
    )
    st.subheader("📋 Job Description (Optional)")

    job_description = st.text_area(
        "Paste the Job Description here",
        height=200,
        placeholder="Paste the company's job description..."
    )
    st.subheader("🏢 Target Company")

    company = st.selectbox(
    "Select Company",
        [
        "General ATS",
        "Google",
        "Microsoft",
        "Amazon",
        "Adobe",
        "Oracle",
        "IBM",
        "Infosys",
        "TCS",
        "Accenture"
        ]
    )
    st.subheader("🎯 Target Role")

    role = st.selectbox(
    "Select Role",
        [
        "Software Engineer",
        "AI Engineer",
        "ML Engineer",
        "Data Analyst",
        "Backend Developer",
        "Frontend Developer",
        "Full Stack Developer",
        "Cloud Engineer"
        ]
    )
    if job_description.strip() == "":
        st.info("💡 Paste a Job Description to use Resume vs JD Match.")
    st.divider()
    if st.button("🚀 Analyze Resume"):

        with st.spinner("Analyzing Resume..."):
           result = analyze_resume(resume_text)
           result = clean_json(result)

        try:
            data = json.loads(result)
        except Exception:
            st.error("Gemini did not return valid JSON.")
            st.code(result)
            st.stop()

        data = json.loads(result)
        st.session_state["analysis_done"] = True
        st.session_state["analysis_data"] = data
        st.session_state["resume_text"] = resume_text

        st.success("Analysis Completed!")


    if st.session_state.get("analysis_done", False):

        data = st.session_state["analysis_data"]

        st.divider()
        
        if company != "General ATS":

            st.divider()
            st.subheader(f"🏢 {company} Analysis")

            company_result = company_analysis(resume_text, company)

            company_result = clean_json(company_result)

            company_data = json.loads(company_result)

            st.metric(
                f"{company} Resume Score",
                f"{company_data['company_score']}%"
            )

            st.progress(company_data["company_score"] / 100)

            st.subheader("🎯 Fit")

            st.write(company_data["fit"])

            st.subheader("❌ Missing Skills")

            for skill in company_data["missing_skills"]:
                st.markdown(f"• {skill}")

            st.subheader("💪 Strengths")

            for strength in company_data["strengths"]:
                st.markdown(f"• {strength}")

            st.subheader("💡 Recommendations")

            for tip in company_data["recommendations"]:
                st.markdown(f"• {tip}")

            st.subheader("📚 Interview Topics")

            for topic in company_data["interview_topics"]:
                st.markdown(f"• {topic}")

    # ⭐ ATS Score
        col1, col2 = st.columns([1,3])

        with col1:
            st.metric("⭐ ATS Score", f"{data['ats_score']}%")

        with col2:
            st.progress(data["ats_score"] / 100)
        stats = resume_statistics(resume_text)

        st.divider()

        st.subheader("📊 Resume Statistics")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("📝 Words", stats["words"])

        with col2:
            st.metric("💻 Skills", stats["skills"])

        with col3:
            st.metric("📂 Projects", stats["projects"])

        with col4:
            st.metric("🏆 Certifications", stats["certifications"])
        
        st.subheader("✅ Resume Checklist")

        col1, col2 = st.columns(2)

        with col1:
            st.write("📧 Email :", "✅" if stats["email"] else "❌")
            st.write("📱 Phone :", "✅" if stats["phone"] else "❌")

        with col2:
            st.write("💻 GitHub :", "✅" if stats["github"] else "❌")
            st.write("🔗 LinkedIn :", "✅" if stats["linkedin"] else "❌")
                    # 📊 ATS Breakdown

        score_breakdown = data.get("score_breakdown")

        if score_breakdown:

            st.subheader("📊 ATS Score Breakdown")

            for category, score in score_breakdown.items():

                st.write(f"**{category}**")

                st.progress(score / 100)

                st.caption(f"{score}%")

    


    # 📄 Resume Summary
        st.subheader("📄 Resume Summary")
        st.write(data["summary"])

        st.subheader("💻 Technical Skills")

        for skill in data["technical_skills"]:
            st.markdown(f"• {skill}")

    # 💪 Strengths
        st.subheader("💪 Strengths")

        for s in data["strengths"]:
            st.markdown(f"• {s}")

    # ⚠ Weaknesses
        st.subheader("⚠ Weaknesses")

        for w in data["weaknesses"]:
            st.markdown(f"• {w}")

    # 🔍 Missing Keywords
        st.subheader("🔍 Missing Keywords")

        for k in data["missing_keywords"]:
            st.markdown(f"• {k}")

    # 🛠 Suggestions
        st.subheader("🛠 Suggestions")

        for s in data["suggestions"]:
            st.markdown(f"• {s}")
        pdf = generate_pdf(data)

        st.download_button(
            label="📄 Download PDF Report",
            data=pdf,
            file_name="Resume_Analysis_Report.pdf",
            mime="application/pdf"
        )
        if st.session_state.get("analysis_done", False):

            st.divider()

            st.divider()

        if st.button("✨ Improve My Resume"):

            with st.spinner("Improving Resume..."):

                improved_resume = improve_resume(
                st.session_state["resume_text"]
            )

            st.subheader("📄 Improved Resume")

            st.markdown(improved_resume)

            st.download_button(
                "⬇️ Download Improved Resume",
                improved_resume,
                file_name="Improved_Resume.md",
                mime="text/markdown"
            )
            docx_resume = create_docx(
                "Improved Resume",
                improved_resume
            )

            st.download_button(
                "📄 Download Improved Resume (.docx)",
                data=docx_resume,
                file_name="Improved_Resume.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

            st.divider()

        if st.button("📄 Generate Cover Letter"):

            with st.spinner("Generating Cover Letter..."):

                cover_letter = generate_cover_letter(
                    st.session_state["resume_text"],
                    job_description
                )

            st.subheader("📄 AI Generated Cover Letter")

            st.write(cover_letter)

            st.download_button(
                "⬇ Download Cover Letter",
                cover_letter,
                file_name="Cover_Letter.txt",
                mime="text/plain"
            )
            docx_cover = create_docx(
                "Cover Letter",
                cover_letter
            )

            st.download_button(
                "📄 Download Cover Letter (.docx)",
                data=docx_cover,
                file_name="Cover_Letter.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
            st.divider()

        if st.button("🎤 Generate Interview Questions"):

            with st.spinner("Generating Interview Questions..."):

                questions = generate_interview_questions(
                st.session_state["resume_text"]
            )

            st.subheader("🎤 AI Interview Questions")

            st.markdown(questions)

            st.download_button(
                "⬇ Download Questions",
                questions,
                file_name="Interview_Questions.txt",
                mime="text/plain"
            )
            st.divider()

        if st.button("🗺 Generate Learning Roadmap"):

            with st.spinner("Generating Personalized Roadmap..."):

                roadmap = generate_learning_roadmap(
                st.session_state["resume_text"]
            )

            st.subheader("🗺 Personalized Learning Roadmap")

            st.markdown(roadmap)

            st.download_button(
                "⬇ Download Roadmap",
                roadmap,
                file_name="Learning_Roadmap.md",
                mime="text/markdown"
            )
            st.divider()

        if st.button("🎯 Analyze Role Fit"):

            with st.spinner("Analyzing Role Fit..."):

                result = role_fit_analysis(
                    st.session_state["resume_text"],
                    role
            )

            result = result.replace("```json", "").replace("```", "").strip()

            role_data = json.loads(result)

            st.subheader("🎯 Resume Role Fit")

            st.metric(
                "Role Match",
                f"{role_data['match_score']}%"
             )

            st.progress(role_data["match_score"]/100)

            st.subheader("✅ Matching Skills")

            for skill in role_data["matching_skills"]:
                st.markdown(f"• {skill}")

            st.subheader("❌ Missing Skills")

            for skill in role_data["missing_skills"]:
                st.markdown(f"• {skill}")

            st.subheader("💡 Recommendations")

            for tip in role_data["recommendations"]:
                st.markdown(f"• {tip}")

            st.divider()

        if st.button("📊 Resume vs JD Match"):

            if job_description.strip() == "":

                st.warning("Please paste a Job Description first.")

        else:

            with st.spinner("Matching Resume with Job Description..."):

                jd_result = match_resume_with_jd(
                    st.session_state["resume_text"],
                    job_description
                )

            jd_result = jd_result.replace("```json", "").replace("```", "").strip()

            jd_data = json.loads(jd_result)

            st.subheader("📊 Resume vs Job Description Dashboard")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                   "🎯 JD Match Score",
                    f"{jd_data['match_score']}%"
                )

            with col2:
                st.progress(jd_data["match_score"] / 100)

            st.subheader("✅ Matched Skills")

            for skill in jd_data["matched_skills"]:
                st.markdown(f"• {skill}")

            st.subheader("❌ Missing Skills")

            for skill in jd_data["missing_skills"]:
                st.markdown(f"• {skill}")

            st.subheader("💡 ATS Recommendations")

            for tip in jd_data["recommendations"]:
                st.markdown(f"• {tip}")
            st.divider()

        st.subheader("🤖 AI Resume Chatbot")

        question = st.text_input(
            "Ask anything about your resume",
            placeholder="Example: Why is my ATS score low?"
            )
        if st.button("💬 Ask AI"):

            if question.strip() == "":

                st.warning("Please enter a question.")

            else:

                with st.spinner("Thinking..."):

                    answer = resume_chatbot(
                        st.session_state["resume_text"],
                        question
                    )

                st.subheader("🤖 AI Answer")

                st.markdown(answer)