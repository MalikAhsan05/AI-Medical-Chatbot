# ============================================================
# MEDICARE AI
# Professional Medical RAG Assistant
# ============================================================

import streamlit as st
from pathlib import Path
import html


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
# GLOBAL CSS
# ============================================================

st.markdown(
    """
    <style>

    /* -------------------------------------------------------
       FONTS
    ------------------------------------------------------- */

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');


    /* -------------------------------------------------------
       GLOBAL
    ------------------------------------------------------- */

    html,
    body,
    [class*="css"] {
        font-family: "Inter", sans-serif;
    }

    .stApp {
        background:
            radial-gradient(
                circle at 50% -20%,
                rgba(14, 165, 233, 0.08),
                transparent 32%
            ),
            #07111f;

        color: #e8eef7;
    }

    .block-container {
        max-width: 1050px;
        padding-top: 1.4rem;
        padding-bottom: 4rem;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }


    /* -------------------------------------------------------
       SIDEBAR
    ------------------------------------------------------- */

    [data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #081525 0%,
                #07111f 100%
            );

        border-right:
            1px solid rgba(148, 163, 184, 0.10);
    }

    [data-testid="stSidebar"] > div:first-child {
        padding: 1.3rem 1rem 1.5rem 1rem;
    }


    /* -------------------------------------------------------
       SIDEBAR BRAND
    ------------------------------------------------------- */

    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 5px 3px 20px 3px;
    }

    .sidebar-logo {
        width: 42px;
        height: 42px;
        border-radius: 12px;

        display: flex;
        align-items: center;
        justify-content: center;

        background:
            linear-gradient(
                135deg,
                #22d3ee,
                #2563eb
            );

        box-shadow:
            0 8px 24px rgba(37, 99, 235, 0.25);

        color: white;
        font-size: 24px;
        font-weight: 700;
    }

    .sidebar-brand-name {
        font-family: "Manrope", sans-serif;
        font-size: 18px;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: #f8fafc;
        line-height: 1.1;
    }

    .sidebar-brand-sub {
        margin-top: 4px;
        font-size: 9px;
        letter-spacing: 0.8px;
        color: #60758c;
        text-transform: uppercase;
    }


    /* -------------------------------------------------------
       SIDEBAR SECTION TITLE
    ------------------------------------------------------- */

    .sidebar-section {
        margin-top: 25px;
        margin-bottom: 10px;

        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1.2px;
        text-transform: uppercase;

        color: #52677e;
    }


    /* -------------------------------------------------------
       BUTTONS
    ------------------------------------------------------- */

    .stButton > button {
        font-family: "Inter", sans-serif;
        transition: all 0.18s ease;
    }

    .stButton > button[kind="primary"] {
        min-height: 47px;

        border: none !important;
        border-radius: 12px !important;

        background:
            linear-gradient(
                100deg,
                #0891b2,
                #2563eb
            ) !important;

        color: #ffffff !important;

        font-size: 13px !important;
        font-weight: 700 !important;

        box-shadow:
            0 10px 26px rgba(37, 99, 235, 0.20);
    }

    .stButton > button[kind="primary"]:hover {
        transform: translateY(-1px);

        box-shadow:
            0 14px 32px rgba(37, 99, 235, 0.28);
    }


    /* SIDEBAR BUTTONS */

    [data-testid="stSidebar"] .stButton > button {
        width: 100%;
        justify-content: flex-start;
        text-align: left;
    }

    [data-testid="stSidebar"] .stButton > button:not([kind="primary"]) {

        min-height: 41px;

        border-radius: 10px !important;

        background:
            transparent !important;

        border:
            1px solid transparent !important;

        color:
            #8194a9 !important;

        font-size:
            11px !important;

        font-weight:
            500 !important;

        padding-left:
            11px !important;
    }

    [data-testid="stSidebar"] .stButton > button:not([kind="primary"]):hover {

        background:
            rgba(34, 211, 238, 0.055) !important;

        border-color:
            rgba(34, 211, 238, 0.10) !important;

        color:
            #dce8f3 !important;
    }


    /* -------------------------------------------------------
       TOP NAVIGATION
    ------------------------------------------------------- */

    .top-navigation {

        display: flex;
        align-items: center;
        justify-content: space-between;

        padding:
            4px 0 19px 0;

        border-bottom:
            1px solid rgba(148, 163, 184, 0.09);
    }

    .top-brand {

        display: flex;
        align-items: center;
        gap: 12px;
    }

    .top-logo {

        width: 38px;
        height: 38px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 11px;

        background:
            linear-gradient(
                135deg,
                #22d3ee,
                #2563eb
            );

        color: white;

        font-size: 21px;
        font-weight: 700;

        box-shadow:
            0 8px 24px rgba(37, 99, 235, 0.20);
    }

    .top-title {

        font-family:
            "Manrope",
            sans-serif;

        font-size:
            17px;

        font-weight:
            800;

        letter-spacing:
            -0.4px;

        color:
            #f8fafc;
    }

    .top-subtitle {

        margin-top:
            2px;

        color:
            #536b83;

        font-size:
            9px;

        letter-spacing:
            0.8px;

        text-transform:
            uppercase;
    }

    .online-pill {

        display:
            inline-flex;

        align-items:
            center;

        gap:
            7px;

        padding:
            8px 13px;

        border-radius:
            100px;

        background:
            rgba(16, 185, 129, 0.07);

        border:
            1px solid rgba(16, 185, 129, 0.18);

        color:
            #6ee7b7;

        font-size:
            9px;

        font-weight:
            700;

        letter-spacing:
            0.8px;
    }

    .online-dot {

        width:
            6px;

        height:
            6px;

        border-radius:
            50%;

        background:
            #34d399;

        box-shadow:
            0 0 8px rgba(52, 211, 153, 0.65);
    }


    /* -------------------------------------------------------
       WELCOME AREA
    ------------------------------------------------------- */

    .welcome-section {

        text-align:
            center;

        max-width:
            730px;

        margin:
            68px auto 40px auto;
    }

    .medical-badge {

        display:
            inline-flex;

        align-items:
            center;

        gap:
            7px;

        padding:
            7px 12px;

        border-radius:
            100px;

        border:
            1px solid rgba(34, 211, 238, 0.17);

        background:
            rgba(34, 211, 238, 0.055);

        color:
            #67e8f9;

        font-size:
            9px;

        font-weight:
            700;

        letter-spacing:
            1.1px;

        text-transform:
            uppercase;

        margin-bottom:
            21px;
    }

    .welcome-title {

        font-family:
            "Manrope",
            sans-serif;

        font-size:
            clamp(34px, 4vw, 49px);

        line-height:
            1.13;

        letter-spacing:
            -1.9px;

        font-weight:
            800;

        color:
            #f8fafc;

        margin-bottom:
            17px;
    }

    .welcome-gradient {

        background:
            linear-gradient(
                90deg,
                #67e8f9,
                #60a5fa
            );

        -webkit-background-clip:
            text;

        -webkit-text-fill-color:
            transparent;

        background-clip:
            text;
    }

    .welcome-description {

        max-width:
            610px;

        margin:
            0 auto;

        color:
            #71869c;

        font-size:
            13px;

        line-height:
            1.75;
    }


    /* -------------------------------------------------------
       CHAT PANEL
    ------------------------------------------------------- */

    .chat-panel-header {

        display:
            flex;

        align-items:
            center;

        justify-content:
            space-between;

        margin-bottom:
            14px;
    }

    .chat-panel-title {

        font-family:
            "Manrope",
            sans-serif;

        font-size:
            14px;

        font-weight:
            700;

        color:
            #e7eef7;
    }

    .chat-panel-status {

        color:
            #4f6880;

        font-size:
            8px;

        font-weight:
            700;

        letter-spacing:
            0.9px;

        text-transform:
            uppercase;
    }


    /* -------------------------------------------------------
       TEXT AREA / CHAT COMPOSER
    ------------------------------------------------------- */

    [data-testid="stTextArea"] textarea {

        min-height:
            145px !important;

        background:
            linear-gradient(
                145deg,
                #0c1b2d,
                #091726
            ) !important;

        color:
            #edf4fb !important;

        border:
            1px solid rgba(148, 163, 184, 0.13) !important;

        border-radius:
            17px !important;

        padding:
            20px !important;

        font-size:
            13px !important;

        line-height:
            1.65 !important;

        resize:
            none;

        box-shadow:
            0 16px 45px rgba(0, 0, 0, 0.13);
    }

    [data-testid="stTextArea"] textarea::placeholder {

        color:
            #4d6278 !important;
    }

    [data-testid="stTextArea"] textarea:focus {

        border-color:
            rgba(34, 211, 238, 0.38) !important;

        box-shadow:
            0 0 0 2px rgba(34, 211, 238, 0.045),
            0 16px 45px rgba(0, 0, 0, 0.13) !important;
    }

    [data-testid="stTextArea"] label {

        display:
            none !important;
    }


    /* -------------------------------------------------------
       MAIN SECONDARY BUTTONS
    ------------------------------------------------------- */

    .main .stButton > button:not([kind="primary"]) {

        min-height:
            39px;

        border-radius:
            10px !important;

        background:
            rgba(12, 27, 45, 0.72) !important;

        border:
            1px solid rgba(148, 163, 184, 0.10) !important;

        color:
            #7890a7 !important;

        font-size:
            10px !important;

        font-weight:
            500 !important;
    }

    .main .stButton > button:not([kind="primary"]):hover {

        border-color:
            rgba(34, 211, 238, 0.20) !important;

        color:
            #c9d9e8 !important;

        background:
            rgba(34, 211, 238, 0.045) !important;
    }


    /* -------------------------------------------------------
       QUICK QUESTION LABEL
    ------------------------------------------------------- */

    .quick-label {

        margin-top:
            26px;

        margin-bottom:
            10px;

        color:
            #52687e;

        font-size:
            9px;

        font-weight:
            700;

        letter-spacing:
            1.1px;

        text-transform:
            uppercase;
    }


    /* -------------------------------------------------------
       USER QUESTION DISPLAY
    ------------------------------------------------------- */

    .question-container {

        margin-top:
            48px;

        margin-bottom:
            16px;
    }

    .question-label {

        color:
            #50667d;

        font-size:
            9px;

        font-weight:
            700;

        letter-spacing:
            1px;

        text-transform:
            uppercase;

        margin-bottom:
            9px;
    }

    .user-question-card {

        margin-left:
            auto;

        max-width:
            78%;

        padding:
            14px 17px;

        border-radius:
            16px 16px 4px 16px;

        background:
            linear-gradient(
                135deg,
                rgba(8, 145, 178, 0.16),
                rgba(37, 99, 235, 0.13)
            );

        border:
            1px solid rgba(34, 211, 238, 0.13);

        color:
            #dbe9f5;

        font-size:
            13px;

        line-height:
            1.65;
    }


    /* -------------------------------------------------------
       ANSWER SECTION
    ------------------------------------------------------- */

    .answer-header {

        display:
            flex;

        align-items:
            center;

        gap:
            10px;

        margin-bottom:
            13px;
    }

    .answer-icon {

        width:
            31px;

        height:
            31px;

        border-radius:
            9px;

        display:
            flex;

        align-items:
            center;

        justify-content:
            center;

        background:
            linear-gradient(
                135deg,
                #0891b2,
                #2563eb
            );

        color:
            white;

        font-weight:
            700;

        font-size:
            15px;
    }

    .answer-name {

        font-family:
            "Manrope",
            sans-serif;

        color:
            #e9f1f9;

        font-size:
            13px;

        font-weight:
            700;
    }

    .answer-sub {

        color:
            #4e657b;

        font-size:
            8px;

        letter-spacing:
            0.8px;

        margin-top:
            2px;

        text-transform:
            uppercase;
    }


    /* -------------------------------------------------------
       ANSWER CONTAINER
    ------------------------------------------------------- */

    [data-testid="stVerticalBlockBorderWrapper"] {

        border:
            1px solid rgba(148, 163, 184, 0.11) !important;

        border-radius:
            18px !important;

        background:
            linear-gradient(
                145deg,
                rgba(13, 29, 47, 0.90),
                rgba(8, 20, 34, 0.90)
            ) !important;

        box-shadow:
            0 18px 55px rgba(0, 0, 0, 0.14);
    }


    /* -------------------------------------------------------
       MARKDOWN
    ------------------------------------------------------- */

    [data-testid="stMarkdownContainer"] p {

        line-height:
            1.75;
    }

    [data-testid="stMarkdownContainer"] {

        color:
            #c4d1dd;
    }

    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3,
    [data-testid="stMarkdownContainer"] h4 {

        font-family:
            "Manrope",
            sans-serif;

        color:
            #edf4fb;
    }


    /* -------------------------------------------------------
       SOURCES
    ------------------------------------------------------- */

    .sources-heading {

        margin-top:
            32px;

        margin-bottom:
            5px;

        font-family:
            "Manrope",
            sans-serif;

        font-size:
            15px;

        font-weight:
            700;

        color:
            #e5edf6;
    }

    .sources-description {

        color:
            #536a81;

        font-size:
            10px;

        margin-bottom:
            13px;
    }

    [data-testid="stExpander"] {

        background:
            rgba(10, 24, 40, 0.70);

        border:
            1px solid rgba(148, 163, 184, 0.10) !important;

        border-radius:
            12px !important;

        margin-bottom:
            7px;
    }

    [data-testid="stExpander"] summary {

        color:
            #91a5b9 !important;

        font-size:
            11px !important;
    }


    /* -------------------------------------------------------
       ALERTS
    ------------------------------------------------------- */

    [data-testid="stAlert"] {

        border-radius:
            12px !important;

        border:
            1px solid rgba(148, 163, 184, 0.11) !important;
    }


    /* -------------------------------------------------------
       FOOTER NOTICE
    ------------------------------------------------------- */

    .medical-notice {

        margin-top:
            55px;

        padding-top:
            20px;

        border-top:
            1px solid rgba(148, 163, 184, 0.08);

        text-align:
            center;

        color:
            #465d73;

        font-size:
            9px;

        line-height:
            1.6;
    }


    /* -------------------------------------------------------
       SCROLLBAR
    ------------------------------------------------------- */

    ::-webkit-scrollbar {

        width:
            6px;
    }

    ::-webkit-scrollbar-track {

        background:
            #07111f;
    }

    ::-webkit-scrollbar-thumb {

        background:
            #24384c;

        border-radius:
            20px;
    }


    /* -------------------------------------------------------
       MOBILE
    ------------------------------------------------------- */

    @media (max-width: 768px) {

        .block-container {

            padding-left:
                1rem;

            padding-right:
                1rem;
        }

        .welcome-section {

            margin-top:
                42px;
        }

        .welcome-title {

            font-size:
                34px;

            letter-spacing:
                -1.2px;
        }

        .welcome-description {

            font-size:
                12px;
        }

        .online-pill {

            display:
                none;
        }

        .user-question-card {

            max-width:
                94%;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

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
# FUNCTIONS
# ============================================================

def set_question(text):
    """Place a selected question in the composer."""

    st.session_state.question_text = text


def new_chat():
    """Start a fresh conversation."""

    st.session_state.question_text = ""
    st.session_state.answer = None
    st.session_state.sources = []
    st.session_state.last_question = ""


def save_recent_search(question):
    """Save a question in recent chat history."""

    question = question.strip()

    if not question:
        return

    if question in st.session_state.recent_searches:
        st.session_state.recent_searches.remove(question)

    st.session_state.recent_searches.insert(
        0,
        question
    )

    st.session_state.recent_searches = (
        st.session_state.recent_searches[:8]
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    # BRAND
    st.markdown(
        """
        <div class="sidebar-brand">

            <div class="sidebar-logo">
                ✚
            </div>

            <div>

                <div class="sidebar-brand-name">
                    Medicare AI
                </div>

                <div class="sidebar-brand-sub">
                    Medical Intelligence
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    # NEW CHAT
    st.button(
        "＋   New Chat",
        type="primary",
        use_container_width=True,
        on_click=new_chat,
    )


    # RECENT CHATS TITLE
    st.markdown(
        """
        <div class="sidebar-section">
            Recent Chats
        </div>
        """,
        unsafe_allow_html=True,
    )


    # RECENT CHAT LIST
    if len(st.session_state.recent_searches) == 0:

        st.markdown(
            """
            <div style="
                color:#465d73;
                font-size:11px;
                line-height:1.6;
                padding:6px 5px;
            ">
                No recent conversations yet.
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:

        for index, recent_question in enumerate(
            st.session_state.recent_searches
        ):

            if len(recent_question) > 32:

                display_question = (
                    recent_question[:32] + "..."
                )

            else:

                display_question = recent_question

            st.button(
                "◷   " + display_question,
                key=f"recent_chat_{index}",
                use_container_width=True,
                on_click=set_question,
                args=(recent_question,),
            )


# ============================================================
# TOP NAVIGATION
# ============================================================

st.markdown(
    """
    <div class="top-navigation">

        <div class="top-brand">

            <div class="top-logo">
                ✚
            </div>

            <div>

                <div class="top-title">
                    Medicare AI
                </div>

                <div class="top-subtitle">
                    Evidence-Grounded Medical Intelligence
                </div>

            </div>

        </div>


        <div class="online-pill">

            <span class="online-dot"></span>

            AI SYSTEM ONLINE

        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# WELCOME / HERO
# Only display before an answer has been generated
# ============================================================

if not st.session_state.answer:

    st.markdown(
        """
        <div class="welcome-section">

            <div class="medical-badge">
                ✦ AI-Powered Medical Knowledge
            </div>

            <div class="welcome-title">
                Medical knowledge.<br>
                <span class="welcome-gradient">
                    Clearer answers.
                </span>
            </div>

            <div class="welcome-description">

                Ask a medical question and Medicare AI will search
                its medical knowledge base, retrieve relevant evidence,
                and generate a clear, evidence-grounded response.

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# CHAT / QUESTION PANEL
# ============================================================

st.markdown(
    """
    <div class="chat-panel-header">

        <div class="chat-panel-title">
            Ask Medicare AI
        </div>

        <div class="chat-panel-status">
            Evidence Retrieval Ready
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


question = st.text_area(
    "Medical question",
    key="question_text",
    placeholder=(
        "Ask anything about symptoms, conditions, "
        "treatments, medications, or general medical knowledge..."
    ),
    height=145,
)


# ============================================================
# SUBMIT BUTTON AREA
# ============================================================

helper_col, submit_col = st.columns(
    [4.2, 1.35],
    vertical_alignment="center",
)


with helper_col:

    st.markdown(
        """
        <div style="
            color:#50677d;
            font-size:9px;
            line-height:1.5;
        ">
            Answers are generated using retrieved medical evidence.
        </div>
        """,
        unsafe_allow_html=True,
    )


with submit_col:

    analyze_button = st.button(
        "Ask Medicare AI  →",
        type="primary",
        use_container_width=True,
    )


# ============================================================
# QUICK QUESTIONS
# ============================================================

if not st.session_state.answer:

    st.markdown(
        """
        <div class="quick-label">
            Suggested Questions
        </div>
        """,
        unsafe_allow_html=True,
    )


    q1, q2, q3, q4 = st.columns(4)


    with q1:

        st.button(
            "Hypertension",
            key="quick_1",
            use_container_width=True,
            on_click=set_question,
            args=(
                "What is hypertension and how is it managed?",
            ),
        )


    with q2:

        st.button(
            "Diabetes",
            key="quick_2",
            use_container_width=True,
            on_click=set_question,
            args=(
                "What is diabetes mellitus and what causes it?",
            ),
        )


    with q3:

        st.button(
            "Asthma",
            key="quick_3",
            use_container_width=True,
            on_click=set_question,
            args=(
                "What are the symptoms and causes of asthma?",
            ),
        )


    with q4:

        st.button(
            "Migraine",
            key="quick_4",
            use_container_width=True,
            on_click=set_question,
            args=(
                "What causes migraine headaches?",
            ),
        )


# ============================================================
# PROCESS QUESTION
# ============================================================

if analyze_button:

    clean_question = question.strip()

    if not clean_question:

        st.warning(
            "Please enter a medical question before submitting."
        )

    else:

        try:

            with st.spinner(
                "Retrieving medical evidence and "
                "generating your response..."
            ):

                # Import your existing RAG backend.
                from rag import ask_medical_question

                answer, retrieved_documents = (
                    ask_medical_question(
                        clean_question
                    )
                )


            # ------------------------------------------------
            # PREPARE SOURCES
            # ------------------------------------------------

            source_data = []

            for number, document in enumerate(
                retrieved_documents,
                start=1,
            ):

                page = document.metadata.get(
                    "page",
                    "Unknown",
                )

                source_file = document.metadata.get(
                    "source",
                    "Medical Knowledge Base",
                )

                excerpt = (
                    document.page_content.strip()
                )

                if len(excerpt) > 650:

                    excerpt = (
                        excerpt[:650] + "..."
                    )

                source_data.append(
                    {
                        "number": number,
                        "page": page,
                        "source": source_file,
                        "excerpt": excerpt,
                    }
                )


            # ------------------------------------------------
            # SAVE RESPONSE
            # ------------------------------------------------

            st.session_state.answer = answer

            st.session_state.sources = (
                source_data
            )

            st.session_state.last_question = (
                clean_question
            )


            # ------------------------------------------------
            # SAVE RECENT CHAT
            # ------------------------------------------------

            save_recent_search(
                clean_question
            )


            # Rerun so the interface immediately switches
            # from welcome mode to answer mode.
            st.rerun()


        except Exception as error:

            st.error(
                "Medicare AI could not generate a response. "
                "Please try again."
            )

            with st.expander(
                "Technical details"
            ):

                st.code(
                    str(error)
                )


# ============================================================
# ANSWER SECTION
# ============================================================

if st.session_state.answer:

    # --------------------------------------------------------
    # USER QUESTION
    # --------------------------------------------------------

    safe_question = html.escape(
        st.session_state.last_question
    )

    st.markdown(
        f"""
        <div class="question-container">

            <div class="question-label">
                Your Question
            </div>

            <div class="user-question-card">
                {safe_question}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    # --------------------------------------------------------
    # AI IDENTITY
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="answer-header">

            <div class="answer-icon">
                ✚
            </div>

            <div>

                <div class="answer-name">
                    Medicare AI
                </div>

                <div class="answer-sub">
                    Evidence-Grounded Response
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    # --------------------------------------------------------
    # ANSWER CARD
    # --------------------------------------------------------

    with st.container(
        border=True
    ):

        st.markdown(
            st.session_state.answer
        )

        st.markdown(
            """
            <div style="
                margin-top:18px;
                padding-top:13px;
                border-top:
                    1px solid rgba(148,163,184,0.08);
                color:#496177;
                font-size:9px;
            ">
                Response generated from retrieved medical
                knowledge-base evidence.
            </div>
            """,
            unsafe_allow_html=True,
        )


    # ========================================================
    # SOURCES
    # ========================================================

    if st.session_state.sources:

        st.markdown(
            """
            <div class="sources-heading">
                Retrieved Evidence
            </div>

            <div class="sources-description">
                Medical passages retrieved from the knowledge
                base and supplied to the AI for this response.
            </div>
            """,
            unsafe_allow_html=True,
        )


        for source in st.session_state.sources:

            number = source["number"]

            page = source["page"]

            source_file = source["source"]

            excerpt = source["excerpt"]


            title = (
                f"Source {number:02d}"
                f"   ·   Page {page}"
            )


            with st.expander(
                title
            ):

                st.caption(
                    Path(
                        str(source_file)
                    ).name
                )

                st.write(
                    excerpt
                )


# ============================================================
# MEDICAL DISCLAIMER
# ============================================================

st.markdown(
    """
    <div class="medical-notice">

        Medicare AI provides educational medical information
        based on retrieved knowledge sources. It does not provide
        a medical diagnosis and should not replace consultation
        with a qualified healthcare professional.

    </div>
    """,
    unsafe_allow_html=True,
)