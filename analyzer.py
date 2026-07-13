from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
def clean_json(response):
    response = response.replace("```json", "")
    response = response.replace("```", "")
    response = response.strip()
    return response



def ask_llm(prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content


# ---------- Resume Analysis ----------
def analyze_resume(resume_text):

    prompt = f"""
You are an expert ATS Resume Reviewer and Technical Recruiter.

Analyze the following resume exactly like a real Applicant Tracking System (ATS).

First evaluate the resume based on:

1. Technical Skills
2. Projects
3. Experience
4. Education
5. Certifications
6. ATS Formatting
7. Keywords
8. Resume Quality
9. Internship Readiness

After evaluating all these factors, calculate a realistic ATS Score.

Return ONLY valid JSON.

{{
    "ats_score": 82,

    "score_breakdown": {{
        "Skills": 90,
        "Projects": 80,
        "Experience": 60,
        "Education": 85,
        "ATS Keywords": 75,
        "Formatting": 95
    }},

    "summary": "Write a professional summary in 3-4 lines based only on the resume.",

    "technical_skills": [
        "Python",
        "SQL",
        "Machine Learning"
    ],

    "strengths": [
        "Strong Python knowledge",
        "Good AI/ML projects"
    ],

    "weaknesses": [
        "No internship experience",
        "Projects lack measurable impact"
    ],

    "missing_keywords": [
        "Docker",
        "AWS",
        "REST API"
    ],

    "suggestions": [
        "Add quantified project achievements.",
        "Include internship experience if available.",
        "Improve ATS keyword optimization."
    ]
}}

Resume:

{resume_text}

IMPORTANT RULES:

- Read the entire resume carefully.
- Never use fixed scores.
- ATS Score must depend on resume quality.
- Score Breakdown must also depend on resume quality.
- Never invent internships.
- Never invent certifications.
- Never invent skills.
- Never invent projects.
- Suggestions should be specific to the resume.
- Missing keywords should be relevant to the resume.
- Return ONLY valid JSON.
- Do NOT use markdown.
- Do NOT write ```json.
- Do NOT write any explanation before or after the JSON.
"""

    return ask_llm(prompt)

# ---------- Job Description Matching ----------
# ---------- Job Description Matching ----------
def match_resume_with_jd(resume_text, job_description):

    prompt = f"""
You are an expert ATS Recruiter.

Compare the candidate's resume with the given Job Description.

Carefully evaluate:

1. Technical Skills Match
2. Programming Languages
3. Frameworks
4. Tools & Technologies
5. Projects
6. Certifications
7. Experience
8. ATS Keywords
9. Overall Resume Relevance

Calculate a realistic ATS Match Score.

Return ONLY valid JSON.

{{
    "match_score": 84,

    "keyword_match": 78,

    "matched_skills":[
        "Python",
        "SQL",
        "Machine Learning"
    ],

    "missing_skills":[
        "Docker",
        "AWS",
        "REST API"
    ],

    "resume_strength":"Strong Python fundamentals with relevant AI/ML projects.",

    "resume_weakness":"Limited cloud exposure and no internship experience.",

    "recommendations":[
        "Learn Docker.",
        "Build cloud-based projects.",
        "Add REST API development experience.",
        "Improve project impact using measurable results."
    ]
}}

Resume:

{resume_text}

Job Description:

{job_description}

IMPORTANT:

- Compare every requirement in the Job Description.
- Match only relevant skills.
- Do NOT generate random scores.
- Match Score should depend on actual similarity.
- Keyword Match should be calculated realistically.
- Never invent skills.
- Never invent experience.
- Never invent certifications.
- Return ONLY valid JSON.
- Do NOT use markdown.
- Do NOT write ```json.
- Do NOT write explanations.
"""

    return ask_llm(prompt)
# ---------- Company Analysis ----------
def company_analysis(resume_text, company):

    prompt = f"""
You are a Senior Technical Recruiter working at {company}.

Analyze the candidate's resume specifically for recruitment at {company}.

Evaluate based on:

1. Programming Skills
2. Projects
3. Core CS Subjects
4. AI/ML Knowledge
5. Certifications
6. Internship Readiness
7. ATS Keywords
8. Resume Presentation
9. Communication of Skills

Return ONLY valid JSON.

{{
    "company_name":"{company}",

    "company_score":82,

    "fit":"Good Fit",

    "reason":"Explain in 2-3 lines why the candidate is suitable for {company}.",

    "strengths":[
        "Strong Python knowledge",
        "Good AI projects"
    ],

    "missing_skills":[
        "Docker",
        "AWS",
        "System Design"
    ],

    "recommendations":[
        "Improve backend development skills.",
        "Build cloud-based projects.",
        "Practice DSA regularly."
    ],

    "interview_topics":[
        "DSA",
        "DBMS",
        "Operating System",
        "OOP",
        "SQL",
        "Machine Learning"
    ]
}}

Resume:

{resume_text}

IMPORTANT

- Score must depend on resume.
- Never invent experience.
- Never invent internships.
- Never invent certifications.
- Return ONLY JSON.
"""

    return ask_llm(prompt)

# ---------- Improve Resume ----------
def improve_resume(resume_text):

    prompt = f"""
You are an expert Resume Writer.

Rewrite this resume professionally.

Rules

- Keep every section.
- Keep every project.
- Keep every certification.
- Keep all skills.
- Never invent internships.
- Never invent achievements.
- Never invent certifications.
- Improve grammar.
- Improve ATS formatting.
- Improve project descriptions.
- Use professional resume language.
- Make bullet points impactful.
- Keep the information truthful.

Return ONLY the improved resume in Markdown.

Resume:

{resume_text}
"""

    return ask_llm(prompt)

# ---------- Cover Letter ----------
def generate_cover_letter(resume_text, job_description):

    prompt = f"""
You are an HR Recruiter.

Write a professional ATS-friendly Cover Letter.

Instructions

- Use resume information.
- Use Job Description if available.
- Mention candidate's real projects.
- Mention certifications if relevant.
- Do not invent experience.
- Keep professional tone.
- Around 300 words.
- Return only Cover Letter.

Resume

{resume_text}

Job Description

{job_description}
"""

    return ask_llm(prompt)
# ---------- Interview Questions ----------
def generate_interview_questions(resume_text):

    prompt = f"""
You are a Senior Software Engineer.

Generate interview questions based on the resume.

Return in Markdown.

# HR Questions

5 Questions

# Technical Questions

10 Questions

# Resume Based Questions

5 Questions

# Project Based Questions

5 Questions

# Coding Questions

5 Questions

Resume

{resume_text}
"""

    return ask_llm(prompt)
# ---------- Learning Roadmap ----------
def generate_learning_roadmap(resume_text):

    prompt = f"""
You are a Career Mentor.

Generate a personalized 4 Month Learning Roadmap.

Each Month should contain

Topics

Why Learn

Resources

Mini Project

Expected Outcome

Return in Markdown.

Resume

{resume_text}
"""

    return ask_llm(prompt)

# ---------- Role Fit ----------
def role_fit_analysis(resume_text, role):

    prompt = f"""
You are an ATS Expert.

Evaluate how suitable this resume is for

{role}

Return ONLY JSON.

{{
"role":"{role}",

"match_score":82,

"why_this_score":"Explain in 2 lines.",

"matching_skills":[
"Python",
"SQL"
],

"missing_skills":[
"Docker",
"AWS"
],

"learning_priority":[
"Docker",
"Kubernetes",
"Cloud"
],

"recommendations":[
"Build backend projects",
"Practice DSA"
]
}}

Resume

{resume_text}

IMPORTANT

Do not invent skills.

Calculate realistic score.

Return ONLY JSON.
"""

    return ask_llm(prompt)
def resume_chatbot(resume_text, user_question):

    prompt = f"""
You are an experienced ATS Expert, Career Coach, and Technical Recruiter.

Answer the user's question ONLY using the information available in the resume.

If the user asks for suggestions, provide practical career advice.

Resume:

{resume_text}

User Question:

{user_question}

Give a professional and detailed answer.
"""

    return ask_llm(prompt)