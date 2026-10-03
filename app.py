# ============================================================
# MedRAG AI — PROFESSIONAL STREAMLIT INTERFACE
# ============================================================

import streamlit as st
import html
from datetime import datetime


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="MedRAG AI | Medical Knowledge Assistant",
    page_icon="✚",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM DESIGN SYSTEM
# ============================================================

st.markdown("""
<style>

/* ---------- Fonts ---------- */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');


/* ---------- Global ---------- */

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 50% -10%,
        rgba(37, 99, 235, 0.12),
        transparent 32%),
        #07111f;
}

.block-container {
    max-width: 1080px;
    padding-top: 2.2rem;
    padding-bottom: 5rem;
}


/* ---------- Hide Streamlit chrome ---------- */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}


/* ---------- Top navigation ---------- */

.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;

    padding-bottom: 24px;

    border-bottom: 1px solid rgba(148,163,184,0.12);

    margin-bottom: 55px;
}

.logo-area {
    display: flex;
    align-items: center;
    gap: 12px;
}

.logo-mark {
    width: 39px;
    height: 39px;

    border-radius: 11px;

    display: flex;
    align-items: center;
    justify-content: center;

    background: linear-gradient(
        135deg,
        #22d3ee,
        #2563eb
    );

    color: white;

    font-size: 20px;
    font-weight: 700;

    box-shadow:
        0 8px 25px rgba(37,99,235,0.22);
}

.logo-text {
    font-family: 'Manrope', sans-serif;

    color: #f8fafc;

    font-size: 19px;
    font-weight: 800;

    letter-spacing: -0.5px;
}

.logo-sub {
    color: #64748b;

    font-size: 10px;

    margin-top: -2px;
}

.online-pill {
    display: flex;
    align-items: center;
    gap: 7px;

    padding: 7px 12px;

    border-radius: 100px;

    background: rgba(16,185,129,0.07);

    border: 1px solid rgba(16,185,129,0.16);

    color: #6ee7b7;

    font-size: 10px;

    font-weight: 700;

    letter-spacing: 0.7px;
}

.online-dot {
    width: 6px;
    height: 6px;

    border-radius: 50%;

    background: #34d399;

    box-shadow: 0 0 9px rgba(52,211,153,0.8);
}


/* ---------- Hero ---------- */

.hero {
    text-align: center;

    max-width: 850px;

    margin: 0 auto 42px auto;
}

.hero-badge {
    display: inline-block;

    padding: 7px 13px;

    border-radius: 100px;

    background: rgba(34,211,238,0.06);

    border: 1px solid rgba(34,211,238,0.15);

    color: #67e8f9;

    font-size: 10px;

    font-weight: 700;

    letter-spacing: 1.1px;

    text-transform: uppercase;

    margin-bottom: 20px;
}

.hero-title {
    font-family: 'Manrope', sans-serif;

    font-size: clamp(40px, 5vw, 62px);

    line-height: 1.08;

    font-weight: 800;

    letter-spacing: -2.6px;

    color: #f8fafc;

    margin-bottom: 17px;
}

.hero-highlight {
    background: linear-gradient(
        90deg,
        #67e8f9,
        #60a5fa,
        #818cf8
    );

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;
}

.hero-description {
    max-width: 690px;

    margin: auto;

    color: #8da0b7;

    font-size: 15px;

    line-height: 1.75;
}


/* ---------- Main assistant panel ---------- */

.assistant-panel {
    padding: 27px 30px 8px 30px;

    background:
        linear-gradient(
            145deg,
            rgba(15,30,49,0.90),
            rgba(9,21,36,0.88)
        );

    border: 1px solid rgba(148,163,184,0.13);

    border-radius: 22px 22px 0 0;

    border-bottom: none;
}

.panel-top {
    display: flex;
    justify-content: space-between;
    align-items: center;

    margin-bottom: 5px;
}

.panel-title {
    color: #eaf1f9;

    font-family: 'Manrope', sans-serif;

    font-size: 16px;

    font-weight: 700;
}

.panel-status {
    color: #64748b;

    font-size: 10px;
}

.panel-description {
    color: #6f8298;

    font-size: 12px;

    margin-bottom: 5px;
}


/* ---------- Text area ---------- */

[data-testid="stTextArea"] {
    margin-bottom: -5px;
}

[data-testid="stTextArea"] textarea {
    min-height: 155px !important;

    background: #0b1727 !important;

    border: 1px solid rgba(148,163,184,0.15) !important;

    border-radius: 0 0 14px 14px !important;

    color: #e7eef7 !important;

    font-size: 14px !important;

    line-height: 1.65 !important;

    padding: 20px !important;

    box-shadow: none !important;
}

[data-testid="stTextArea"] textarea::placeholder {
    color: #52657a !important;
}

[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(34,211,238,0.42) !important;

    box-shadow:
        0 0 0 1px rgba(34,211,238,0.08) !important;
}


/* Hide textarea label */

[data-testid="stTextArea"] label {
    display: none;
}


/* ---------- Character helper ---------- */

.input-helper {
    color: #506176;

    font-size: 10px;

    margin-top: 4px;
}


/* ---------- Primary button ---------- */

.stButton > button[kind="primary"] {
    width: 100%;

    min-height: 48px;

    border: none;

    border-radius: 12px;

    background:
        linear-gradient(
            90deg,
            #0891b2,
            #2563eb
        );

    color: white;

    font-size: 13px;

    font-weight: 700;

    box-shadow:
        0 10px 30px rgba(37,99,235,0.17);

    transition: all 0.2s ease;
}

.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px);

    box-shadow:
        0 12px 34px rgba(37,99,235,0.25);
}


/* ---------- Secondary button ---------- */

.stButton > button:not([kind="primary"]) {
    min-height: 42px;

    border-radius: 11px;

    background: rgba(15,30,49,0.65);

    border: 1px solid rgba(148,163,184,0.12);

    color: #9aacbf;

    font-size: 11px;

    transition: 0.2s;
}

.stButton > button:not([kind="primary"]):hover {
    color: #e2e8f0;

    border-color: rgba(34,211,238,0.25);

    background: rgba(34,211,238,0.05);
}


/* ---------- Suggestions ---------- */

.suggestion-label {
    color: #53667c;

    font-size: 10px;

    font-weight: 700;

    letter-spacing: 0.9px;

    text-transform: uppercase;

    margin-top: 27px;

    margin-bottom: 10px;
}


/* ---------- Answer section ---------- */

.answer-header {
    display: flex;

    align-items: center;

    gap: 10px;

    margin-top: 42px;

    margin-bottom: 14px;
}

.answer-icon {
    width: 32px;
    height: 32px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 9px;

    background: linear-gradient(
        135deg,
        rgba(34,211,238,0.16),
        rgba(37,99,235,0.16)
    );

    border: 1px solid rgba(34,211,238,0.14);

    color: #67e8f9;

    font-weight: 700;
}

.answer-heading {
    color: #f1f5f9;

    font-family: 'Manrope', sans-serif;

    font-size: 17px;

    font-weight: 700;
}

.answer-meta {
    color: #52657a;

    font-size: 10px;

    margin-top: 2px;
}

.answer-card {
    background:
        linear-gradient(
            145deg,
            rgba(14,29,47,0.92),
            rgba(9,21,36,0.90)
        );

    border: 1px solid rgba(148,163,184,0.13);

    border-radius: 18px;

    padding: 27px 30px;

    color: #c9d5e3;

    font-size: 14px;

    line-height: 1.85;

    box-shadow:
        0 20px 55px rgba(0,0,0,0.12);
}


/* ---------- Sources ---------- */

.sources-title {
    margin-top: 22px;

    color: #71849a;

    font-size: 10px;

    font-weight: 700;

    letter-spacing: 1px;

    text-transform: uppercase;
}

.source-row {
    display: flex;

    align-items: center;

    justify-content: space-between;

    margin-top: 8px;

    padding: 11px 14px;

    border-radius: 10px;

    background: rgba(15,30,49,0.55);

    border: 1px solid rgba(148,163,184,0.09);
}

.source-left {
    color: #91a4b9;

    font-size: 11px;
}

.source-number {
    color: #67e8f9;

    font-weight: 700;

    margin-right: 9px;
}

.source-page {
    color: #61748a;

    font-size: 10px;
}


/* ---------- Architecture strip ---------- */

.tech-strip {
    margin-top: 50px;

    padding: 17px 20px;

    border-top: 1px solid rgba(148,163,184,0.10);

    border-bottom: 1px solid rgba(148,163,184,0.10);

    display: flex;

    justify-content: center;

    gap: 42px;

    flex-wrap: wrap;
}

.tech-item {
    color: #52657a;

    font-size: 10px;

    letter-spacing: 0.5px;
}

.tech-item strong {
    color: #8497ad;

    font-weight: 600;
}


/* ---------- Disclaimer ---------- */

.disclaimer {
    max-width: 720px;

    margin: 25px auto 0 auto;

    text-align: center;

    color: #4c5e72;

    font-size: 10px;

    line-height: 1.6;
}


/* ---------- Spinner ---------- */

[data-testid="stSpinner"] {
    color: #8da0b7 !important;
}


/* ---------- Responsive ---------- */

@media (max-width: 700px) {

    .hero-title {
        font-size: 39px;
        letter-spacing: -1.7px;
    }

    .topbar {
        margin-bottom: 38px;
    }

    .assistant-panel {
        padding: 22px 20px 7px 20px;
    }

    .answer-card {
        padding: 22px;
    }

    .tech-strip {
        gap: 18px;
    }
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "question_text" not in st.session_state:
    st.session_state.question_text = ""

if "answer" not in st.session_state:
    st.session_state.answer = None

if "sources" not in st.session_state:
    st.session_state.sources = []

if "last_question" not in st.session_state:
    st.session_state.last_question = ""


# ============================================================
# CALLBACK FOR SUGGESTION BUTTONS
# ============================================================

def set_question(question):
    st.session_state.question_text = question


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="topbar">
    <div class="logo-area">
        <div class="logo-mark">✚</div>
        <div>
            <div class="logo-text">MedRAG AI</div>
            <div class="logo-sub">RETRIEVAL-AUGMENTED MEDICAL INTELLIGENCE</div>
        </div>
    </div>
    <div class="online-pill">
        <span class="online-dot"></span>
        SYSTEM ONLINE
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero">
    <div class="hero-badge">
        Evidence-grounded medical knowledge
    </div>

    <div class="hero-title">
        Ask. Retrieve.
        <span class="hero-highlight">Understand.</span>
    </div>

    <div class="hero-description">
        Explore medical knowledge through intelligent retrieval.
        MedRAG searches its medical knowledge base, identifies
        relevant evidence, and generates a clear response with
        transparent source references.
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# INPUT HEADER
# ============================================================

st.markdown("""
<div class="assistant-panel">
    <div class="panel-top">
        <div class="panel-title">Medical Knowledge Assistant</div>
        <div class="panel-status">RAG ENGINE READY</div>
    </div>

    <div class="panel-description">
        Describe your question, concern, or medical topic below.
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# LARGE TEXT AREA
# ============================================================

question = st.text_area(
    "Medical question",
    key="question_text",
    placeholder=(
        "Write your medical question or thoughts here...\n\n"
        "Example: What is hypertension, what causes it, "
        "and how is it generally managed?"
    ),
    height=170
)


# ============================================================
# ACTION AREA
# ============================================================

left, right = st.columns([4.6, 1.4])

with left:
    st.markdown(
        '<div class="input-helper">'
        'Your question is processed against the indexed medical knowledge base.'
        '</div>',
        unsafe_allow_html=True
    )

with right:
    ask_button = st.button(
        "Analyze Question  →",
        type="primary",
        use_container_width=True
    )


# ============================================================
# SUGGESTED QUESTIONS
# ============================================================

st.markdown(
    '<div class="suggestion-label">Try an example</div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.button(
        "What is hypertension?",
        key="hypertension",
        on_click=set_question,
        args=("What is hypertension?",),
        use_container_width=True
    )

with c2:
    st.button(
        "Explain diabetes mellitus",
        key="diabetes",
        on_click=set_question,
        args=("Explain diabetes mellitus.",),
        use_container_width=True
    )

with c3:
    st.button(
        "What are asthma symptoms?",
        key="asthma",
        on_click=set_question,
        args=("What are the common symptoms of asthma?",),
        use_container_width=True
    )

with c4:
    st.button(
        "What causes migraine?",
        key="migraine",
        on_click=set_question,
        args=("What causes migraine headaches?",),
        use_container_width=True
    )


# ============================================================
# PROCESS QUESTION
# ============================================================

if ask_button:

    clean_question = question.strip()

    if not clean_question:

        st.warning(
            "Please enter a medical question before continuing."
        )

    else:

        try:

            with st.spinner(
                "Retrieving medical evidence and generating your response..."
            ):

                # Lazy import keeps the UI fast on initial load.
                from rag import ask_medical_question

                answer, retrieved_documents = (
                    ask_medical_question(clean_question)
                )

            source_data = []

            for index, document in enumerate(
                retrieved_documents,
                start=1
            ):

                page = document.metadata.get(
                    "page",
                    "Unknown"
                )

                source = document.metadata.get(
                    "source",
                    "Medical Knowledge Base"
                )

                source_data.append(
                    {
                        "number": index,
                        "page": page,
                        "source": source
                    }
                )

            st.session_state.answer = answer
            st.session_state.sources = source_data
            st.session_state.last_question = clean_question

        except Exception as error:

            st.error(
                "MedRAG could not generate a response. "
                "Please try again."
            )

            with st.expander("Technical details"):
                st.code(str(error))


# ============================================================
# ANSWER
# ============================================================

if st.session_state.answer:

    safe_answer = html.escape(
        str(st.session_state.answer)
    )

    # Preserve paragraphs/new lines.
    safe_answer = safe_answer.replace(
        "\n\n",
        "<br><br>"
    ).replace(
        "\n",
        "<br>"
    )

    current_time = datetime.now().strftime("%H:%M")

    st.markdown(
        f"""
<div class="answer-header">
    <div class="answer-icon">✦</div>
    <div>
        <div class="answer-heading">MedRAG Response</div>
        <div class="answer-meta">
            Generated at {current_time} · Grounded in retrieved context
        </div>
    </div>
</div>

<div class="answer-card">
    {safe_answer}
</div>
""",
        unsafe_allow_html=True
    )


    # ========================================================
    # SOURCES
    # ========================================================

    if st.session_state.sources:

        st.markdown(
            '<div class="sources-title">Retrieved evidence</div>',
            unsafe_allow_html=True
        )

        for source in st.session_state.sources:

            number = source["number"]
            page = source["page"]

            st.markdown(
                f"""
<div class="source-row">
    <div class="source-left">
        <span class="source-number">
            {number:02d}
        </span>
        Medical Knowledge Base
    </div>

    <div class="source-page">
        PDF PAGE {page}
    </div>
</div>
""",
                unsafe_allow_html=True
            )


# ============================================================
# TECHNOLOGY STRIP
# ============================================================

st.markdown("""
<div class="tech-strip">

    <div class="tech-item">
        RETRIEVAL&nbsp;&nbsp;<strong>FAISS</strong>
    </div>

    <div class="tech-item">
        EMBEDDINGS&nbsp;&nbsp;<strong>MiniLM-L6</strong>
    </div>

    <div class="tech-item">
        GENERATION&nbsp;&nbsp;<strong>Qwen3</strong>
    </div>

    <div class="tech-item">
        PIPELINE&nbsp;&nbsp;<strong>RAG</strong>
    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# MEDICAL DISCLAIMER
# ============================================================

st.markdown("""
<div class="disclaimer">
    MedRAG AI is an educational medical knowledge system and
    does not provide a medical diagnosis or replace professional
    medical care. For medical decisions, diagnosis, emergencies,
    or treatment, consult an appropriately qualified healthcare
    professional.
</div>
""", unsafe_allow_html=True)