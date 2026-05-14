import streamlit as st
import sqlite3
import requests

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
# CREATE USER
# ======================================================

def create_user(username, password):

    username = username.strip().lower()

    if username == "" or password == "":

        return "empty"

    cursor.execute(

        "SELECT * FROM users WHERE username=?",

        (username,)

    )

    existing_user = cursor.fetchone()

    if existing_user:

        return "exists"

    cursor.execute(

        "INSERT INTO users (username, password) VALUES (?, ?)",

        (

            username,

            password

        )

    )

    conn.commit()

    return "success"

# ======================================================
# LOGIN USER
# ======================================================

def login_user(username, password):

    username = username.strip().lower()

    cursor.execute(

        "SELECT * FROM users WHERE username=? AND password=?",

        (

            username,

            password

        )

    )

    return cursor.fetchone()

# ======================================================
# SESSION
# ======================================================

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False

if "username" not in st.session_state:

    st.session_state.username = ""

# ======================================================
# PREMIUM CSS
# ======================================================

st.markdown("""

<style>

/* ======================================================
BACKGROUND
====================================================== */

.stApp {

    background: linear-gradient(
        135deg,
        #020617,
        #0f172a,
        #111827
    );

}

/* ======================================================
REMOVE STREAMLIT
====================================================== */

[data-testid="stHeader"] {

    background: transparent;

}

header {

    background: transparent;

}

footer {

    visibility: hidden;

}

#MainMenu {

    visibility: hidden;

}

/* ======================================================
SIDEBAR
====================================================== */

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

/* ======================================================
TITLE
====================================================== */

.main-title {

    font-size: 78px;

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

/* ======================================================
SUBTITLE
====================================================== */

.sub-title {

    text-align: center;

    color: white;

    font-size: 24px;

    margin-bottom: 40px;

}

/* ======================================================
GLASS CARD
====================================================== */

.glass-card {

    background: rgba(255,255,255,0.08);

    border-radius: 24px;

    padding: 30px;

    border: 1px solid rgba(255,255,255,0.08);

    margin-bottom: 20px;

}

/* ======================================================
METRIC CARD
====================================================== */

.metric-box {

    background: rgba(255,255,255,0.08);

    border-radius: 20px;

    padding: 30px;

    text-align: center;

    border: 1px solid rgba(255,255,255,0.08);

}

/* ======================================================
BUTTONS
====================================================== */

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

/* ======================================================
TEXT INPUTS
====================================================== */

.stTextInput input {

    background: white !important;

    color: black !important;

    border-radius: 14px !important;

}

/* ======================================================
TEXT AREA
====================================================== */

.stTextArea textarea {

    background: white !important;

    color: black !important;

    border-radius: 14px !important;

}

/* ======================================================
FILE UPLOADER
====================================================== */

.stFileUploader {

    background: white !important;

    border-radius: 14px !important;

    padding: 10px;

}

.stFileUploader * {

    color: black !important;

}

/* ======================================================
SELECTBOX
====================================================== */

.stSelectbox div[data-baseweb="select"] {

    background: rgba(255,255,255,0.08);

    border-radius: 14px;

    color: white !important;

}

/* ======================================================
LABELS
====================================================== */

label {

    color: white !important;

    font-weight: 700;

}

/* ======================================================
GENERAL TEXT
====================================================== */

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

    tab1, tab2 = st.tabs([

        "🔐 Login",

        "✨ Sign Up"

    ])

    # LOGIN

    with tab1:

        username = st.text_input(

            "Username"

        )

        password = st.text_input(

            "Password",

            type="password"

        )

        if st.button("Login"):

            user = login_user(

                username,

                password

            )

            if user:

                st.session_state.logged_in = True

                st.session_state.username = username

                st.rerun()

            else:

                st.error(

                    "Invalid Username or Password"

                )

    # SIGNUP

    with tab2:

        new_user = st.text_input(

            "Create Username"

        )

        new_pass = st.text_input(

            "Create Password",

            type="password"

        )

        if st.button("Create Account"):

            result = create_user(

                new_user,

                new_pass

            )

            if result == "success":

                st.success(

                    "Account Created Successfully"

                )

            elif result == "exists":

                st.warning(

                    "Username Already Exists"

                )

            else:

                st.error(

                    "Please Fill All Fields"

                )

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

    ✅ ATS Resume Screening

    ✅ Fresh US Jobs

    ✅ Applied Jobs Tracker

    ✅ Recruiter Dashboard

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

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.markdown("""

    <div class="metric-box">

    <h2>🚀 40+</h2>

    <p>Job Domains</p>

    </div>

    """, unsafe_allow_html=True)

with col2:

    st.markdown("""

    <div class="metric-box">

    <h2>🇺🇸 50</h2>

    <p>US States</p>

    </div>

    """, unsafe_allow_html=True)

with col3:

    st.markdown("""

    <div class="metric-box">

    <h2>⚡ AI</h2>

    <p>ATS Matching</p>

    </div>

    """, unsafe_allow_html=True)

with col4:

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
# ATS TAB
# ======================================================

with tab1:

    st.markdown("""

    <div class="glass-card">

    <h2>📄 ATS Resume Analyzer</h2>

    </div>

    """, unsafe_allow_html=True)

    st.file_uploader(

        "Upload Resume",

        type=["pdf"]

    )

    st.text_area(

        "Paste Job Description"

    )

    if st.button("Analyze Resume"):

        st.success("ATS Analysis Completed")

# ======================================================
# JOB APPLICATIONS TAB
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
        "docker",
        "kubernetes",
        "flutter",
        "android",
        "ios",
        "ui-ux",
        "product-manager",
        "business-analyst",
        "qa",
        "testing",
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
        "web3",
        "crypto",
        "powerbi",
        "tableau",
        "etl",
        "data-engineer",
        "prompt-engineer"

    ]

    us_states = [

        "Alabama","Alaska","Arizona","Arkansas","California",
        "Colorado","Connecticut","Delaware","Florida","Georgia",
        "Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas",
        "Kentucky","Louisiana","Maine","Maryland","Massachusetts",
        "Michigan","Minnesota","Mississippi","Missouri","Montana",
        "Nebraska","Nevada","New Hampshire","New Jersey","New Mexico",
        "New York","North Carolina","North Dakota","Ohio","Oklahoma",
        "Oregon","Pennsylvania","Rhode Island","South Carolina",
        "South Dakota","Tennessee","Texas","Utah","Vermont",
        "Virginia","Washington","West Virginia","Wisconsin","Wyoming"

    ]

    col1, col2 = st.columns(2)

    with col1:

        domain = st.selectbox(

            "Choose Job Domain",

            domains

        )

    with col2:

        state = st.selectbox(

            "Select US State",

            us_states

        )

    if st.button("🚀 Load Fresh Jobs"):

        with st.spinner("Loading jobs..."):

            try:

                url = f"https://remotive.com/api/remote-jobs?search={domain}"

                response = requests.get(url)

                data = response.json()

                jobs = data.get("jobs", [])

                if jobs:

                    st.success(

                        f"{len(jobs)} jobs found"

                    )

                    for job in jobs[:50]:

                        title = job.get(

                            "title",

                            "No Title"

                        )

                        company = job.get(

                            "company_name",

                            "Unknown"

                        )

                        category = job.get(

                            "category",

                            "N/A"

                        )

                        job_url = job.get(

                            "url",

                            "#"

                        )

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

                else:

                    st.warning(

                        "No jobs found"

                    )

            except Exception as e:

                st.error(

                    f"Error loading jobs: {e}"

                )

# ======================================================
# APPLIED JOBS TAB
# ======================================================

with tab3:

    st.markdown("""

    <div class="glass-card">

    <h2>📌 Applied Jobs Tracker</h2>

    </div>

    """, unsafe_allow_html=True)

    st.info(

        "No applied jobs yet."

    )