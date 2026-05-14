import fitz
import ollama


def extract_text_from_pdf(pdf_path):

    text = ""

    doc = fitz.open(pdf_path)

    for page in doc:
        text += page.get_text()

    return text


def extract_skills(text):

    prompt = f"""
    You are an expert AI recruiter.

    Extract ONLY technical skills from this resume.

    Rules:
    - Return comma-separated skills only
    - No numbering
    - No explanations
    - Include:
      - programming languages
      - frameworks
      - tools
      - databases
      - cloud platforms
      - software skills

    Resume:
{text[:2000]}

    Return only comma-separated skills.
    """

    response = ollama.chat(
        model="phi3",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


def calculate_match(resume_skills, jd_text):

    resume_skills = [s.strip() for s in resume_skills.split(",")]

    jd_text = jd_text.lower()

    matched = []
    missing = []

    for skill in resume_skills:

        skill_lower = skill.lower()

        if (
            skill_lower in jd_text
            or skill_lower.replace(" ", "") in jd_text.replace(" ", "")
            or any(word in jd_text for word in skill_lower.split())
        ):
            matched.append(skill)

        else:
            missing.append(skill)

    score = int((len(matched) / len(resume_skills)) * 100)

    return {
        "match_score": score,
        "matched_skills": matched,
        "missing_skills": missing
    }
from jobs import jobs


def recommend_jobs(resume_skills):

    resume_skills = [
        s.strip().lower()
        for s in resume_skills.split(",")
    ]

    recommendations = []

    for job in jobs:

        matched = 0

        for skill in job["skills"]:

            if skill.lower() in resume_skills:
                matched += 1

        score = int(
            (matched / len(job["skills"])) * 100
        )

        recommendations.append({
            "title": job["title"],
            "match_score": score
        })

    recommendations = sorted(
        recommendations,
        key=lambda x: x["match_score"],
        reverse=True
    )

    return recommendations