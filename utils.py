import fitz

def extract_text_from_pdf(uploaded_file):
    pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")

    text = ""

    for page in pdf:
        text += page.get_text()

    pdf.close()

    return text

import re

def resume_statistics(resume_text):

    stats = {}

    # Total Words
    stats["words"] = len(resume_text.split())

    # Total Characters
    stats["characters"] = len(resume_text)

    # Projects
    stats["projects"] = resume_text.lower().count("project")

    # Certifications
    stats["certifications"] = (
        resume_text.lower().count("certification")
        + resume_text.lower().count("certified")
    )

    # Skills (Approx.)
    skill_keywords = [
        "Python","Java","SQL","C","C++","JavaScript","HTML","CSS",
        "React","Flask","Django","FastAPI","Git","GitHub",
        "Docker","AWS","Azure","Power BI","Machine Learning",
        "Deep Learning","TensorFlow","PyTorch","Scikit-learn"
    ]

    count = 0

    for skill in skill_keywords:
        if skill.lower() in resume_text.lower():
            count += 1

    stats["skills"] = count

    # Email
    stats["email"] = bool(
        re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", resume_text)
    )

    # Phone
    stats["phone"] = bool(
        re.search(r"(\+91[- ]?)?[6-9]\d{9}", resume_text)
    )

    # GitHub
    stats["github"] = "github" in resume_text.lower()

    # LinkedIn
    stats["linkedin"] = "linkedin" in resume_text.lower()

    return stats