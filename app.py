# ============================================================
# MEDICARE AI
# Professional Medical RAG Platform
# Step 3: Authentication UI + Existing RAG Dashboard
# ============================================================

import streamlit as st
from pathlib import Path

from auth import register_user, login_user


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Medicare AI",
    page_icon="✚",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
HERO_IMAGE = BASE_DIR / "assets" / "medical-hero.jpg"


# ============================================================
# SESSION STATE
# ============================================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "user" not in st.session_state:
    st.session_state.user = None

if "auth_page" not in st.session_state:
    st.session_state.auth_page = "login"

if "question_text" not in st.session_state:
    st.session_state.question_text = ""

if "answer" not in st.session_state:
    st.session_state.answer = None

if "sources" not in st.session_state:
    st.session_state.sources = []

if "recent_searches" not in st.session_state:
    st.session_state.recent_searches = []

if "last_question" not in st.session_state:
    st.session_state.last_question = ""


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    """
<style>

/* ==========================================================
   GLOBAL
   ========================================================== */

html,
body,
[class*="css"] {
    font-family:
        "Segoe UI",
        Inter,
        system-ui,
        -apple-system,
        BlinkMacSystemFont,
        sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 82% 10%,
            rgba(34, 211, 238, 0.09),
            transparent 27%
        ),
        radial-gradient(
            circle at 12% 75%,
            rgba(37, 99, 235, 0.08),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #06101c 0%,
            #071522 45%,
            #07111e 100%
        );

    color: #e9f1f8;
}

.block-container {
    max-width: 1180px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}


/* ==========================================================
   STREAMLIT CHROME
   ========================================================== */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}


/* ==========================================================
   HEADINGS
   ========================================================== */

h1,
h2,
h3 {
    font-family:
        "Segoe UI",
        Inter,
        sans-serif !important;

    letter-spacing: -0.5px;
}

h1 {
    color: #f8fbff !important;
    font-weight: 750 !important;
}

h2,
h3 {
    color: #e8f1f8 !important;
}


/* ==========================================================
   NORMAL TEXT
   ========================================================== */

[data-testid="stMarkdownContainer"] p {
    line-height: 1.75;
}

[data-testid="stCaptionContainer"] {
    color: #73869a !important;
}


/* ==========================================================
   INPUTS
   ========================================================== */

[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {

    background:
        linear-gradient(
            145deg,
            rgba(13, 30, 48, 0.95),
            rgba(9, 23, 38, 0.95)
        ) !important;

    color: #edf5fb !important;

    border:
        1px solid rgba(148, 163, 184, 0.15) !important;

    border-radius: 13px !important;

    font-size: 14px !important;

    transition:
        border-color 0.2s ease,
        box-shadow 0.2s ease;
}


[data-testid="stTextInput"] input {
    min-height: 48px;
    padding-left: 15px;
}


[data-testid="stTextArea"] textarea {
    min-height: 180px !important;
    padding: 18px !important;
    line-height: 1.7 !important;
}


[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {

    border-color:
        rgba(34, 211, 238, 0.52) !important;

    box-shadow:
        0 0 0 3px rgba(34, 211, 238, 0.055) !important;
}


[data-testid="stTextInput"] input::placeholder,
[data-testid="stTextArea"] textarea::placeholder {
    color: #53677b !important;
}


[data-testid="stTextInput"] label,
[data-testid="stTextArea"] label {

    color: #cbd8e4 !important;

    font-weight: 600 !important;

    font-size: 13px !important;
}


/* ==========================================================
   PRIMARY BUTTON
   ========================================================== */

.stButton > button[kind="primary"] {

    min-height: 49px;

    border: none !important;

    border-radius: 12px !important;

    background:
        linear-gradient(
            100deg,
            #0891b2 0%,
            #0ea5e9 45%,
            #2563eb 100%
        ) !important;

    color: white !important;

    font-weight: 700 !important;

    font-size: 13px !important;

    letter-spacing: 0.1px;

    box-shadow:
        0 12px 30px rgba(14, 165, 233, 0.16);

    transition:
        transform 0.18s ease,
        box-shadow 0.18s ease;
}


.stButton > button[kind="primary"]:hover {

    transform: translateY(-1px);

    box-shadow:
        0 16px 38px rgba(14, 165, 233, 0.25);
}


/* ==========================================================
   SECONDARY BUTTON
   ========================================================== */

.stButton > button:not([kind="primary"]) {

    min-height: 43px;

    border-radius: 11px !important;

    background:
        rgba(13, 28, 46, 0.72) !important;

    color: #a7b7c8 !important;

    border:
        1px solid rgba(148, 163, 184, 0.12) !important;

    font-size: 12px !important;

    transition: all 0.18s ease;
}


.stButton > button:not([kind="primary"]):hover {

    color: #edf7fb !important;

    border-color:
        rgba(34, 211, 238, 0.30) !important;

    background:
        rgba(34, 211, 238, 0.06) !important;
}


/* ==========================================================
   IMAGE
   ========================================================== */

[data-testid="stImage"] img {

    border-radius: 22px;

    border:
        1px solid rgba(148, 163, 184, 0.13);

    box-shadow:
        0 28px 75px rgba(0, 0, 0, 0.32);

    object-fit: cover;
}


/* ==========================================================
   CONTAINERS
   ========================================================== */

[data-testid="stVerticalBlockBorderWrapper"] {

    border:
        1px solid rgba(148, 163, 184, 0.12) !important;

    border-radius: 20px !important;

    background:
        linear-gradient(
            145deg,
            rgba(14, 31, 49, 0.80),
            rgba(8, 20, 34, 0.78)
        );

    box-shadow:
        0 20px 55px rgba(0, 0, 0, 0.13);
}


/* ==========================================================
   SIDEBAR
   ========================================================== */

[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            #081624 0%,
            #07111e 100%
        );

    border-right:
        1px solid rgba(148, 163, 184, 0.10);
}


[data-testid="stSidebar"] h1 {
    font-size: 23px !important;
}


[data-testid="stSidebar"] h3 {

    font-size: 11px !important;

    text-transform: uppercase;

    letter-spacing: 1.1px;

    color: #6f8397 !important;
}


[data-testid="stSidebar"] .stButton > button {

    width: 100%;

    justify-content: flex-start;

    text-align: left;
}


/* ==========================================================
   ALERTS
   ========================================================== */

[data-testid="stAlert"] {

    border-radius: 13px !important;

    border:
        1px solid rgba(148, 163, 184, 0.12) !important;
}


/* ==========================================================
   EXPANDERS
   ========================================================== */

[data-testid="stExpander"] {

    background:
        rgba(10, 24, 40, 0.75);

    border:
        1px solid rgba(148, 163, 184, 0.11) !important;

    border-radius: 13px !important;

    margin-bottom: 7px;
}


/* ==========================================================
   DIVIDERS
   ========================================================== */

hr {
    border-color:
        rgba(148, 163, 184, 0.10) !important;
}


/* ==========================================================
   METRICS
   ========================================================== */

[data-testid="stMetric"] {

    background:
        rgba(12, 27, 44, 0.55);

    border:
        1px solid rgba(148, 163, 184, 0.09);

    border-radius: 14px;

    padding: 13px;
}


/* ==========================================================
   SCROLLBAR
   ========================================================== */

::-webkit-scrollbar {
    width: 7px;
}

::-webkit-scrollbar-track {
    background: #07111e;
}

::-webkit-scrollbar-thumb {

    background: #26394c;

    border-radius: 10px;
}


/* ==========================================================
   MOBILE
   ========================================================== */

@media (max-width: 768px) {

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def go_to_login():
    """
    Switch authentication page to Login.
    """

    st.session_state.auth_page = "login"


def go_to_signup():
    """
    Switch authentication page to Create Account.
    """

    st.session_state.auth_page = "signup"


def set_question(text):
    """
    Set a question from a recent search or example.
    """

    st.session_state.question_text = text


def new_chat():
    """
    Clear the current temporary conversation.
    Persistent conversation history comes in later steps.
    """

    st.session_state.question_text = ""
    st.session_state.answer = None
    st.session_state.sources = []
    st.session_state.last_question = ""


def save_recent_search(question):
    """
    Temporary session-based search history.

    Persistent per-user database history will be
    implemented in later steps.
    """

    question = question.strip()

    if not question:
        return

    if question in st.session_state.recent_searches:
        st.session_state.recent_searches.remove(question)

    st.session_state.recent_searches.insert(
        0,
        question,
    )

    st.session_state.recent_searches = (
        st.session_state.recent_searches[:8]
    )


# ============================================================
# AUTHENTICATION UI
# ============================================================

def show_authentication():

    # --------------------------------------------------------
    # Hide sidebar before login
    # --------------------------------------------------------

    st.markdown(
        """
        <style>

        [data-testid="stSidebar"] {
            display: none;
        }

        [data-testid="collapsedControl"] {
            display: none;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


    # --------------------------------------------------------
    # TOP BRAND BAR
    # --------------------------------------------------------

    brand_left, brand_right = st.columns(
        [4, 1],
        vertical_alignment="center",
    )

    with brand_left:

        st.caption(
            "✚  MEDICARE AI  /  MEDICAL INTELLIGENCE"
        )

    with brand_right:

        st.caption(
            "SECURE ACCESS"
        )


    st.write("")
    st.write("")


    # ========================================================
    # TWO-COLUMN AUTH LAYOUT
    # ========================================================

    visual_column, form_column = st.columns(
        [1.12, 0.88],
        gap="large",
        vertical_alignment="center",
    )


    # ========================================================
    # LEFT SIDE — BRAND / HERO
    # ========================================================

    with visual_column:

        st.caption(
            "AI-POWERED MEDICAL KNOWLEDGE"
        )

        st.title(
            "Medical intelligence, grounded in evidence."
        )

        st.write(
            """
            Medicare AI combines semantic retrieval and
            generative AI to help you explore medical
            information through a focused, evidence-grounded
            experience.
            """
        )

        st.write("")

        feature1, feature2, feature3 = st.columns(3)

        with feature1:
            st.metric(
                "Search",
                "Semantic",
            )

        with feature2:
            st.metric(
                "Knowledge",
                "Grounded",
            )

        with feature3:
            st.metric(
                "Access",
                "Private",
            )

        st.write("")

        if HERO_IMAGE.exists():

            st.image(
                str(HERO_IMAGE),
                use_container_width=True,
            )

        else:

            with st.container(border=True):

                st.subheader(
                    "Medicare AI"
                )

                st.write(
                    "Place your medical image at "
                    "`assets/medical-hero.jpg`."
                )


    # ========================================================
    # RIGHT SIDE — AUTH CARD
    # ========================================================

    with form_column:

        with st.container(
            border=True,
        ):

            # =================================================
            # LOGIN PAGE
            # =================================================

            if st.session_state.auth_page == "login":

                st.caption(
                    "WELCOME BACK"
                )

                st.subheader(
                    "Sign in to Medicare AI"
                )

                st.caption(
                    "Access your medical intelligence workspace."
                )

                st.write("")

                login_email = st.text_input(
                    "Email address",
                    placeholder="name@example.com",
                    key="login_email",
                )

                login_password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Enter your password",
                    key="login_password",
                )

                st.write("")

                login_clicked = st.button(
                    "Sign in to Medicare AI  →",
                    type="primary",
                    use_container_width=True,
                    key="login_button",
                )


                # ---------------------------------------------
                # LOGIN PROCESSING
                # ---------------------------------------------

                if login_clicked:

                    with st.spinner(
                        "Securely signing you in..."
                    ):

                        success, message, user = login_user(
                            login_email,
                            login_password,
                        )

                    if success:

                        st.session_state.authenticated = True
                        st.session_state.user = user

                        st.success(
                            "Authentication successful."
                        )

                        st.rerun()

                    else:

                        st.error(
                            message
                        )


                st.write("")
                st.divider()

                st.caption(
                    "NEW TO MEDICARE AI?"
                )

                st.button(
                    "Create a new account",
                    use_container_width=True,
                    on_click=go_to_signup,
                    key="go_signup",
                )

                st.write("")

                st.caption(
                    "Your password is verified securely "
                    "using cryptographic password hashing."
                )


            # =================================================
            # SIGNUP PAGE
            # =================================================

            else:

                st.caption(
                    "CREATE YOUR WORKSPACE"
                )

                st.subheader(
                    "Create a Medicare AI account"
                )

                st.caption(
                    "Set up secure access to your medical "
                    "intelligence workspace."
                )

                st.write("")

                signup_name = st.text_input(
                    "Full name",
                    placeholder="Enter your full name",
                    key="signup_name",
                )

                signup_email = st.text_input(
                    "Email address",
                    placeholder="name@example.com",
                    key="signup_email",
                )

                signup_password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Create a secure password",
                    key="signup_password",
                )

                signup_confirm_password = st.text_input(
                    "Confirm password",
                    type="password",
                    placeholder="Re-enter your password",
                    key="signup_confirm_password",
                )


                st.caption(
                    "Use at least 8 characters with an "
                    "uppercase letter, lowercase letter, "
                    "and number."
                )

                st.write("")

                signup_clicked = st.button(
                    "Create Medicare AI account  →",
                    type="primary",
                    use_container_width=True,
                    key="signup_button",
                )


                # ---------------------------------------------
                # SIGNUP PROCESSING
                # ---------------------------------------------

                if signup_clicked:

                    with st.spinner(
                        "Creating your secure account..."
                    ):

                        success, message, user = register_user(
                            signup_name,
                            signup_email,
                            signup_password,
                            signup_confirm_password,
                        )

                    if success:

                        st.success(
                            "Account created successfully. "
                            "You can now sign in."
                        )

                        st.session_state.auth_page = "login"

                    else:

                        st.error(
                            message
                        )


                st.write("")
                st.divider()

                st.caption(
                    "ALREADY HAVE AN ACCOUNT?"
                )

                st.button(
                    "Return to sign in",
                    use_container_width=True,
                    on_click=go_to_login,
                    key="go_login",
                )


    # ========================================================
    # AUTH FOOTER
    # ========================================================

    st.write("")
    st.write("")
    st.divider()

    footer1, footer2, footer3 = st.columns(3)

    with footer1:

        st.caption(
            "RETRIEVAL"
        )

        st.write(
            "**FAISS Semantic Search**"
        )

    with footer2:

        st.caption(
            "AI ENGINE"
        )

        st.write(
            "**Qwen + MiniLM**"
        )

    with footer3:

        st.caption(
            "SECURITY"
        )

        st.write(
            "**Hashed Credentials**"
        )

    st.write("")

    st.caption(
        "Medicare AI is an educational medical knowledge "
        "assistant and does not replace professional medical "
        "diagnosis, emergency care, or individualized treatment."
    )


# ============================================================
# MEDICARE AI DASHBOARD
# ============================================================

def show_dashboard():

    user = st.session_state.user


    # ========================================================
    # SIDEBAR
    # ========================================================

    with st.sidebar:

        st.title(
            "✚ Medicare AI"
        )

        st.caption(
            "Medical Intelligence Assistant"
        )

        st.write("")

        st.button(
            "＋  New conversation",
            on_click=new_chat,
            use_container_width=True,
            type="primary",
        )

        st.write("")

        st.subheader(
            "Recent Searches"
        )

        if len(
            st.session_state.recent_searches
        ) == 0:

            st.caption(
                "Your recent medical questions "
                "will appear here."
            )

        else:

            for index, recent_question in enumerate(
                st.session_state.recent_searches
            ):

                if len(recent_question) > 36:

                    display_question = (
                        recent_question[:36]
                        + "..."
                    )

                else:

                    display_question = (
                        recent_question
                    )

                st.button(
                    display_question,
                    key=f"recent_{index}",
                    on_click=set_question,
                    args=(recent_question,),
                    use_container_width=True,
                )


        st.write("")
        st.divider()


        # ----------------------------------------------------
        # ACCOUNT AREA
        # ----------------------------------------------------

        st.caption(
            "SIGNED IN AS"
        )

        st.write(
            f"**{user['name']}**"
        )

        st.caption(
            user["email"]
        )

        st.write("")


        # ----------------------------------------------------
        # LOGOUT
        # ----------------------------------------------------

        if st.button(
            "↪  Sign out",
            use_container_width=True,
            key="logout_button",
        ):

            st.session_state.authenticated = False
            st.session_state.user = None

            st.session_state.question_text = ""
            st.session_state.answer = None
            st.session_state.sources = []
            st.session_state.last_question = ""

            st.rerun()


        st.write("")
        st.divider()

        st.caption(
            "SYSTEM"
        )

        st.success(
            "● Knowledge base ready"
        )

        st.caption(
            "FAISS retrieval · MiniLM embeddings · "
            "Qwen generation"
        )


    # ========================================================
    # TOP BAR
    # ========================================================

    top_left, top_right = st.columns(
        [5, 1],
        vertical_alignment="center",
    )

    with top_left:

        st.caption(
            "MEDICARE AI  /  MEDICAL INTELLIGENCE"
        )

    with top_right:

        st.success(
            "● ONLINE"
        )


    # ========================================================
    # HERO
    # ========================================================

    st.write("")

    hero_text, hero_visual = st.columns(
        [1.05, 1],
        gap="large",
        vertical_alignment="center",
    )


    with hero_text:

        st.caption(
            "EVIDENCE-GROUNDED MEDICAL INTELLIGENCE"
        )

        st.title(
            f"Welcome, {user['name'].split()[0]}."
        )

        st.write(
            """
            Explore medical knowledge through intelligent
            retrieval. Medicare AI searches its indexed
            knowledge base, retrieves relevant evidence,
            and generates a focused response with source
            transparency.
            """
        )

        st.write("")

        metric1, metric2, metric3 = st.columns(3)

        with metric1:

            st.metric(
                "Retrieval",
                "FAISS",
            )

        with metric2:

            st.metric(
                "Context",
                "Top 4",
            )

        with metric3:

            st.metric(
                "Generator",
                "Qwen3",
            )


    with hero_visual:

        if HERO_IMAGE.exists():

            st.image(
                str(HERO_IMAGE),
                use_container_width=True,
            )


    # ========================================================
    # QUESTION SECTION
    # ========================================================

    st.write("")
    st.divider()
    st.write("")

    st.subheader(
        "What would you like to understand?"
    )

    st.caption(
        "Describe a medical topic, condition, symptom, "
        "treatment concept, or question."
    )


    question = st.text_area(
        "Your medical question",
        key="question_text",
        placeholder=(
            "Write your medical question or thoughts here...\n\n"
            "Example: What is hypertension, what causes it, "
            "and how is it generally managed?"
        ),
        height=190,
    )


    helper_column, button_column = st.columns(
        [3.8, 1.3],
        vertical_alignment="center",
    )


    with helper_column:

        st.caption(
            "Medicare AI will retrieve relevant information "
            "from the indexed medical knowledge base."
        )


    with button_column:

        analyze_button = st.button(
            "Analyze with Medicare AI  →",
            type="primary",
            use_container_width=True,
        )


    # ========================================================
    # QUICK QUESTIONS
    # ========================================================

    st.write("")

    st.caption(
        "QUICK QUESTIONS"
    )

    example1, example2, example3, example4 = (
        st.columns(4)
    )


    with example1:

        st.button(
            "What is hypertension?",
            key="example_hypertension",
            on_click=set_question,
            args=("What is hypertension?",),
            use_container_width=True,
        )


    with example2:

        st.button(
            "Explain diabetes",
            key="example_diabetes",
            on_click=set_question,
            args=("What is diabetes mellitus?",),
            use_container_width=True,
        )


    with example3:

        st.button(
            "Asthma symptoms",
            key="example_asthma",
            on_click=set_question,
            args=(
                "What are the common symptoms of asthma?",
            ),
            use_container_width=True,
        )


    with example4:

        st.button(
            "Causes of migraine",
            key="example_migraine",
            on_click=set_question,
            args=(
                "What causes migraine headaches?",
            ),
            use_container_width=True,
        )


    # ========================================================
    # PROCESS QUESTION
    # ========================================================

    if analyze_button:

        clean_question = question.strip()

        if not clean_question:

            st.warning(
                "Please write a medical question before "
                "clicking Analyze."
            )

        else:

            try:

                with st.spinner(
                    "Searching the medical knowledge base "
                    "and preparing your response..."
                ):

                    # Lazy import keeps startup fast.
                    from rag import ask_medical_question

                    answer, retrieved_documents = (
                        ask_medical_question(
                            clean_question
                        )
                    )


                # ---------------------------------------------
                # PREPARE SOURCES
                # ---------------------------------------------

                source_data = []

                for number, document in enumerate(
                    retrieved_documents,
                    start=1,
                ):

                    page = document.metadata.get(
                        "page",
                        "Unknown",
                    )

                    excerpt = (
                        document.page_content.strip()
                    )

                    if len(excerpt) > 650:

                        excerpt = (
                            excerpt[:650]
                            + "..."
                        )

                    source_data.append(
                        {
                            "number": number,
                            "page": page,
                            "excerpt": excerpt,
                        }
                    )


                # ---------------------------------------------
                # SAVE TEMPORARY SESSION RESULT
                # ---------------------------------------------

                st.session_state.answer = answer

                st.session_state.sources = (
                    source_data
                )

                st.session_state.last_question = (
                    clean_question
                )

                save_recent_search(
                    clean_question
                )


            except Exception as error:

                st.error(
                    "Medicare AI could not generate a "
                    "response. Please try again."
                )

                with st.expander(
                    "Technical details"
                ):

                    st.code(
                        str(error)
                    )


    # ========================================================
    # ANSWER
    # ========================================================

    if st.session_state.answer:

        st.write("")
        st.write("")
        st.divider()

        st.caption(
            "MEDICARE AI RESPONSE"
        )

        st.subheader(
            "Evidence-grounded answer"
        )

        st.caption(
            "Question: "
            + st.session_state.last_question
        )

        st.write("")


        with st.container(
            border=True
        ):

            st.markdown(
                "#### ✦ Medicare AI"
            )

            st.markdown(
                st.session_state.answer
            )

            st.caption(
                "Generated using retrieved context "
                "from the indexed medical knowledge base."
            )


        # ====================================================
        # SOURCES
        # ====================================================

        if st.session_state.sources:

            st.write("")

            st.subheader(
                "Retrieved evidence"
            )

            st.caption(
                "These passages were retrieved by FAISS "
                "and supplied as context to the language model."
            )

            st.write("")

            for source in st.session_state.sources:

                number = source["number"]
                page = source["page"]
                excerpt = source["excerpt"]

                title = (
                    f"Source {number:02d}"
                    f"  ·  PDF Page {page}"
                )

                with st.expander(
                    title
                ):

                    st.caption(
                        "Medical Knowledge Base"
                    )

                    st.write(
                        excerpt
                    )


    # ========================================================
    # DASHBOARD FOOTER
    # ========================================================

    st.write("")
    st.write("")
    st.divider()

    footer1, footer2, footer3 = st.columns(3)


    with footer1:

        st.caption(
            "RETRIEVAL"
        )

        st.write(
            "**FAISS Vector Search**"
        )


    with footer2:

        st.caption(
            "EMBEDDINGS"
        )

        st.write(
            "**MiniLM-L6-v2**"
        )


    with footer3:

        st.caption(
            "GENERATION"
        )

        st.write(
            "**Qwen3-4B Instruct**"
        )


    st.write("")

    st.caption(
        "Medical information notice — Medicare AI is an "
        "educational knowledge assistant. It does not provide "
        "a medical diagnosis and does not replace qualified "
        "professional medical advice, emergency care, or "
        "individualized treatment."
    )


# ============================================================
# APPLICATION ROUTER
# ============================================================

if st.session_state.authenticated:

    show_dashboard()

else:

    show_authentication()