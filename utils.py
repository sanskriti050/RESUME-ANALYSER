import fitz
import re


def extract_text_from_pdf(uploaded_file):
    pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")

    text = ""

    for page in pdf:
        text += page.get_text()

    pdf.close()

    return text


def resume_statistics(resume_text):

    stats = {}

    text = resume_text
    lower = text.lower()

    # ---------------- WORDS ---------------- #

    stats["words"] = len(text.split())

    # ---------------- CHARACTERS ---------------- #

    stats["characters"] = len(text)

    # ---------------- SKILLS ---------------- #

    skill_keywords = [
        "Python","Java","C","C++","SQL","MySQL","JavaScript",
        "HTML","CSS","React","Node","Express","Flask","Django",
        "FastAPI","Git","GitHub","Docker","AWS","Azure",
        "Machine Learning","Deep Learning","TensorFlow",
        "PyTorch","Scikit-learn","Power BI","Pandas",
        "NumPy","OpenCV","MongoDB","Streamlit","Groq",
        "Gemini","LLM","NLP","Linux"
    ]

    found_skills = set()

    for skill in skill_keywords:
        if skill.lower() in lower:
            found_skills.add(skill)

    stats["skills"] = len(found_skills)

    # ---------------- PROJECTS ---------------- #

    project_titles = []

    lines = [line.strip() for line in text.splitlines()]

    in_projects = False

    section_headers = [
        "EDUCATION",
        "CERTIFICATION",
        "CERTIFICATIONS",
        "SKILLS",
        "TECHNICAL SKILLS",
        "ACHIEVEMENTS",
        "EXPERIENCE",
        "WORK EXPERIENCE",
        "INTERNSHIP",
        "LANGUAGES",
        "CONTACT"
    ]

    for line in lines:

        if not line:
            continue

        upper = line.upper()

        if "PROJECT" in upper:
            in_projects = True
            continue

        if in_projects:

            if any(header in upper for header in section_headers):
                break

            if (
                line.startswith("•")
                or line.startswith("●")
                or line.startswith("-")
                or line.startswith("*")
            ):
                continue

            if len(line) < 5:
                continue

            if "github" in line.lower():
                line = line.split("github")[0]

            if line not in project_titles:
                project_titles.append(line)

    stats["projects"] = len(project_titles)

    # ---------------- CERTIFICATIONS ---------------- #

    cert_count = 0

    for line in lines:

        l = line.lower()

        if (
            "certification" in l
            or "certificate" in l
            or "certified" in l
        ):
            cert_count += 1

    stats["certifications"] = cert_count

    # ---------------- EXPERIENCE ---------------- #

    experience = re.findall(
        r"\d+\+?\s*(?:years?|yrs?|months?)",
        lower
    )

    stats["experience"] = len(experience)

    # ---------------- EDUCATION ---------------- #

    education_keywords = [
        "b.tech",
        "btech",
        "bachelor",
        "master",
        "m.tech",
        "mtech",
        "university",
        "college",
        "school"
    ]

    stats["education"] = any(
        word in lower for word in education_keywords
    )

    # ---------------- EMAIL ---------------- #

    stats["email"] = bool(
        re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            text
        )
    )

    # ---------------- PHONE ---------------- #

    stats["phone"] = bool(
        re.search(
            r"(\+91[- ]?)?[6-9]\d{9}",
            text
        )
    )

    # ---------------- GITHUB ---------------- #

    stats["github"] = "github" in lower

    # ---------------- LINKEDIN ---------------- #

    stats["linkedin"] = "linkedin" in lower

    return stats