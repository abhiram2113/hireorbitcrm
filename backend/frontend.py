# ======================================================
# HIRE ORBIT - COMPLETE FRONTEND.PY
# ======================================================

import streamlit as st
import sqlite3
import requests
import json
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PyPDF2 import PdfReader

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="Hire Orbit",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================
# DATABASE
# ======================================================

conn = sqlite3.connect(
    "users.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""

CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT

)

""")

conn.commit()

# ======================================================
# APPLIED JOBS FILE
# ======================================================

APPLIED_JOBS_FILE = "applied_jobs.json"

if not os.path.exists(APPLIED_JOBS_FILE):

    with open(APPLIED_JOBS_FILE, "w") as f:
        json.dump([], f)

# ======================================================
# LOAD APPLIED JOBS
# ======================================================

def load_applied_jobs():

    with open(APPLIED_JOBS_FILE, "r") as f:
        return json.load(f)

# ======================================================
# SAVE APPLIED JOBS
# ======================================================

def save_applied_jobs(jobs):

    with open(APPLIED_JOBS_FILE, "w") as f:
        json.dump(jobs, f, indent=4)

# ======================================================
# CREATE USER
# ======================================================

def create_user(username, password):

    username = username.strip().lower()

    cursor.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    )

    existing = cursor.fetchone()

    if existing:
        return False

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, password)
    )

    conn.commit()

    return True

# ======================================================
# LOGIN USER
# ======================================================

def login_user(username, password):

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username.lower(), password)
    )

    return cursor.fetchone()

# ======================================================
# EXTRACT PDF TEXT
# ======================================================

def extract_resume_text(uploaded_file):

    text = ""

    try:

        pdf = PdfReader(uploaded_file)

        for page in pdf.pages:
            text += page.extract_text()

    except:
        pass

    return text

# ======================================================
# ATS SCORE
# ======================================================

def calculate_ats_score(resume_text, job_description):

    try:

        documents = [resume_text, job_description]

        cv = CountVectorizer().fit_transform(documents)

        similarity = cosine_similarity(cv)

        score = round(similarity[0][1] * 100, 2)

        return score

    except:

        return 0

# ======================================================
# SESSION STATE
# ======================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# ======================================================
# PREMIUM UI
# ======================================================

st.markdown("""

<style>

.stApp {
    background: linear-gradient(
        135deg,
        #020617,
        #0f172a,
        #111827
    );
}

[data-testid="stHeader"] {
    background: transparent;
}

header {
    background: transparent;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #312e81,
        #1e1b4b,
        #0f172a
    );
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

.main-title {
    font-size: 72px;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(
        90deg,
        #60a5fa,
        #818cf8,
        #c084fc
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.sub-title {
    text-align: center;
    color: white;
    font-size: 22px;
    margin-bottom: 40px;
}

.glass-card {
    background: rgba(255,255,255,0.08);
    border-radius: 24px;
    padding: 30px;
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 20px;
}

.metric-box {
    background: rgba(255,255,255,0.08);
    border-radius: 24px;
    padding: 30px;
    text-align: center;
}

.stButton > button {
    width: 100%;
    background: linear-gradient(
        90deg,
        #6366f1,
        #8b5cf6
    );
    color: white !important;
    border: none;
    border-radius: 14px;
    padding: 14px;
    font-weight: 700;
}

.stTextInput input {
    background: white !important;
    color: black !important;
}

.stTextArea textarea {
    background: white !important;
    color: black !important;
}

.stFileUploader {
    background: white !important;
    border-radius: 14px;
    padding: 10px;
}

.stFileUploader * {
    color: black !important;
}

.stSelectbox div[data-baseweb="select"] {
    background: rgba(255,255,255,0.08);
    border-radius: 12px;
    color: white !important;
}

label {
    color: white !important;
    font-weight: 700;
}

h1,h2,h3,h4,h5,h6,p,span {
    color: white !important;
}

</style>

""", unsafe_allow_html=True)

# ======================================================
# LOGIN PAGE
# ======================================================

if not st.session_state.logged_in:

    st.markdown("""

    <div class="main-title">
    Hire Orbit
    </div>

    <div class="sub-title">
    AI Recruitment CRM & ATS Platform
    </div>

    """, unsafe_allow_html=True)

    login_tab, signup_tab = st.tabs([
        "🔐 Login",
        "✨ Sign Up"
    ])

    # LOGIN

    with login_tab:

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            user = login_user(username, password)

            if user:

                st.session_state.logged_in = True
                st.session_state.username = username

                st.rerun()

            else:

                st.error("Invalid credentials")

    # SIGNUP

    with signup_tab:

        new_user = st.text_input("Create Username")

        new_pass = st.text_input(
            "Create Password",
            type="password"
        )

        if st.button("Create Account"):

            success = create_user(
                new_user,
                new_pass
            )

            if success:

                st.success("Account Created")

            else:

                st.warning("Username already exists")

    st.stop()

# ======================================================
# SIDEBAR
# ======================================================

with st.sidebar:

    st.markdown(f"""

    # 🚀 Hire Orbit

    ### Welcome

    👤 {st.session_state.username}

    ---

    ✅ ATS Resume Analyzer

    ✅ Fresh US Jobs

    ✅ Applied Jobs Tracking

    ✅ Recruiter CRM Dashboard

    """)

    if st.button("Logout"):

        st.session_state.logged_in = False

        st.rerun()

# ======================================================
# HEADER
# ======================================================

st.markdown("""

<div class="main-title">

Hire Orbit

</div>

<div class="sub-title">

AI-Powered Recruitment CRM & Modern ATS Platform

</div>

""", unsafe_allow_html=True)

# ======================================================
# METRICS
# ======================================================

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.markdown("""

    <div class="metric-box">
    <h2>🚀 40+</h2>
    <p>Job Domains</p>
    </div>

    """, unsafe_allow_html=True)

with c2:

    st.markdown("""

    <div class="metric-box">
    <h2>🇺🇸 50</h2>
    <p>US States</p>
    </div>

    """, unsafe_allow_html=True)

with c3:

    st.markdown("""

    <div class="metric-box">
    <h2>⚡ AI</h2>
    <p>ATS Matching</p>
    </div>

    """, unsafe_allow_html=True)

with c4:

    st.markdown("""

    <div class="metric-box">
    <h2>📈 CRM</h2>
    <p>Recruiter Workflow</p>
    </div>

    """, unsafe_allow_html=True)

# ======================================================
# TABS
# ======================================================

tab1, tab2, tab3 = st.tabs([
    "📄 ATS Analyzer",
    "💼 Job Applications",
    "📌 Applied Jobs"
])

# ======================================================
# ATS ANALYZER
# ======================================================

with tab1:

    st.markdown("""

    <div class="glass-card">

    <h2>📄 ATS Resume Analyzer</h2>

    </div>

    """, unsafe_allow_html=True)

    uploaded_resume = st.file_uploader(
        "Upload Resume PDF",
        type=["pdf"]
    )

    job_description = st.text_area(
        "Paste Job Description"
    )

    if st.button("Analyze ATS Score"):

        if uploaded_resume and job_description:

            resume_text = extract_resume_text(
                uploaded_resume
            )

            score = calculate_ats_score(
                resume_text,
                job_description
            )

            st.success(
                f"ATS Match Score: {score}%"
            )

            if score >= 80:

                st.success("Excellent Resume Match")

            elif score >= 60:

                st.warning("Good Match")

            else:

                st.error("Low Match Score")

        else:

            st.warning(
                "Upload resume and paste job description"
            )

# ======================================================
# JOB APPLICATIONS
# ======================================================

with tab2:

    st.markdown("""

    <div class="glass-card">

    <h2>💼 Fresh US Job Applications</h2>

    </div>

    """, unsafe_allow_html=True)

    domains = [

        "python",
        "java",
        "react",
        "nodejs",
        "software-engineer",
        "frontend",
        "backend",
        "fullstack",
        "data-science",
        "machine-learning",
        "ai-engineer",
        "devops",
        "cloud",
        "cybersecurity",
        "aws",
        "azure",
        "flutter",
        "android",
        "ios",
        "ui-ux",
        "product-manager",
        "business-analyst",
        "salesforce",
        "sap",
        "oracle",
        "sql",
        "mongodb",
        "php",
        "laravel",
        "django",
        "flask",
        "golang",
        "rust",
        "c++",
        "dotnet",
        "typescript",
        "angular",
        "vue",
        "blockchain",
        "powerbi",
        "tableau",
        "etl",
        "data-engineer",
        "prompt-engineer",
        "supply-chain",
        "procurement-analyst",
        "logistics",
        "inventory-management",
        "warehouse-manager"

    ]

    us_states = [

        "Alabama","Alaska","Arizona","Arkansas",
        "California","Colorado","Connecticut",
        "Delaware","Florida","Georgia","Hawaii",
        "Idaho","Illinois","Indiana","Iowa",
        "Kansas","Kentucky","Louisiana","Maine",
        "Maryland","Massachusetts","Michigan",
        "Minnesota","Mississippi","Missouri",
        "Montana","Nebraska","Nevada",
        "New Hampshire","New Jersey","New Mexico",
        "New York","North Carolina","North Dakota",
        "Ohio","Oklahoma","Oregon","Pennsylvania",
        "Rhode Island","South Carolina",
        "South Dakota","Tennessee","Texas",
        "Utah","Vermont","Virginia","Washington",
        "West Virginia","Wisconsin","Wyoming"

    ]

    col1, col2 = st.columns(2)

    with col1:

        domain = st.selectbox(
            "Choose Domain",
            domains
        )

    with col2:

        state = st.selectbox(
            "Select US State",
            us_states
        )

    if st.button("🚀 Load Fresh Jobs"):

        applied_jobs = load_applied_jobs()

        try:

            url = f"https://remotive.com/api/remote-jobs?search={domain}"

            response = requests.get(url)

            data = response.json()

            jobs = data.get("jobs", [])

            if jobs:

                st.success(f"{len(jobs)} jobs found")

                for i, job in enumerate(jobs[:50]):

                    title = job.get("title", "")
                    company = job.get("company_name", "")
                    category = job.get("category", "")
                    job_url = job.get("url", "")

                    # ======================================================
                    # SKIP APPLIED JOBS
                    # ======================================================

                    already_applied = False

                    for applied in applied_jobs:

                        if applied["url"] == job_url:
                            already_applied = True

                    if already_applied:
                        continue

                    st.markdown(f"""

                    <div class="glass-card">

                    <h3>💼 {title}</h3>

                    <p><b>🏢 Company:</b> {company}</p>

                    <p><b>📍 Location:</b> {state}, USA</p>

                    <p><b>🧠 Domain:</b> {category}</p>

                    <a href="{job_url}" target="_blank">

                    🔗 Apply Now

                    </a>

                    </div>

                    """, unsafe_allow_html=True)

                    status = st.selectbox(

                        "Application Status",

                        ["Not Applied", "Applied"],

                        key=f"{title}_{i}"

                    )

                    if status == "Applied":

                        applied_jobs.append({

                            "title": title,
                            "company": company,
                            "location": state,
                            "domain": category,
                            "url": job_url

                        })

                        save_applied_jobs(applied_jobs)

                        st.success(
                            "Moved to Applied Jobs"
                        )

                        st.rerun()

            else:

                st.warning("No jobs found")

        except Exception as e:

            st.error(f"Error: {e}")

# ======================================================
# APPLIED JOBS TAB
# ======================================================

with tab3:

    st.markdown("""

    <div class="glass-card">

    <h2>📌 Applied Jobs Tracker</h2>

    </div>

    """, unsafe_allow_html=True)

    applied_jobs = load_applied_jobs()

    if applied_jobs:

        for i, job in enumerate(applied_jobs):

            st.markdown(f"""

            <div class="glass-card">

            <h3>💼 {job['title']}</h3>

            <p><b>🏢 Company:</b> {job['company']}</p>

            <p><b>📍 Location:</b> {job['location']}</p>

            <p><b>🧠 Domain:</b> {job['domain']}</p>

            <a href="{job['url']}" target="_blank">

            🔗 Job Link

            </a>

            </div>

            """, unsafe_allow_html=True)

    else:

        st.info("No applied jobs yet.")