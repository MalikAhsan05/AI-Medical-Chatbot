# ============================================================
# MEDICARE AI
# Premium Medical RAG Chat Interface
# ============================================================

import streamlit as st
from pathlib import Path


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Medicare AI",
    page_icon="✚",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PROFESSIONAL UI CSS
# ============================================================

st.markdown("""
<style>

/* ==========================================================
   GLOBAL
   ========================================================== */

html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI",
                 Inter, Helvetica, Arial, sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 50% -10%,
            rgba(14,165,233,0.08),
            transparent 28%
        ),
        #07111f;

    color: #eaf2fa;
}

.block-container {
    max-width: 980px;
    padding-top: 1.3rem;
    padding-bottom: 4rem;
}


/* Remove Streamlit branding */

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
   SIDEBAR
   ========================================================== */

[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #081625 0%,
            #07111f 100%
        );

    border-right:
        1px solid rgba(148,163,184,0.09);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.4rem;
}


/* Sidebar title */

[data-testid="stSidebar"] h1 {
    font-size: 21px !important;
    font-weight: 750 !important;
    letter-spacing: -0.6px !important;
    color: #f8fafc !important;
    margin-bottom: 0 !important;
}

[data-testid="stSidebar"] p {
    color: #62788e;
    font-size: 11px;
}


/* ==========================================================
   SIDEBAR NEW CHAT
   ========================================================== */

[data-testid="stSidebar"] .stButton > button[kind="primary"] {

    width: 100%;

    min-height: 47px;

    border: 0 !important;

    border-radius: 12px !important;

    background:
        linear-gradient(
            100deg,
            #0891b2,
            #2563eb
        ) !important;

    color: white !important;

    font-size: 13px !important;
    font-weight: 650 !important;

    box-shadow:
        0 8px 24px rgba(37,99,235,0.18);

    transition:
        transform 0.18s ease,
        box-shadow 0.18s ease;
}

[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {

    transform: translateY(-1px);

    box-shadow:
        0 12px 30px rgba(37,99,235,0.28);
}


/* ==========================================================
   RECENT CHAT BUTTONS
   ========================================================== */

[data-testid="stSidebar"] .stButton > button:not([kind="primary"]) {

    width: 100%;

    justify-content: flex-start;

    min-height: 40px;

    border-radius: 9px !important;

    border:
        1px solid transparent !important;

    background:
        transparent !important;

    color:
        #8296aa !important;

    font-size:
        11px !important;

    font-weight:
        450 !important;

    text-align:
        left;

    transition:
        all 0.15s ease;
}

[data-testid="stSidebar"] .stButton > button:not([kind="primary"]):hover {

    background:
        rgba(34,211,238,0.045) !important;

    border-color:
        rgba(34,211,238,0.08) !important;

    color:
        #dce8f3 !important;
}


/* ==========================================================
   HEADINGS
   ========================================================== */

h1, h2, h3 {
    letter-spacing: -0.7px;
    color: #f4f8fc !important;
}


/* ==========================================================
   CAPTION
   ========================================================== */

[data-testid="stCaptionContainer"] {
    color: #61788e !important;
}


/* ==========================================================
   INPUT AREA
   ========================================================== */

[data-testid="stTextArea"] textarea {

    min-height: 150px !important;

    padding: 20px !important;

    border-radius: 17px !important;

    border:
        1px solid rgba(148,163,184,0.14) !important;

    background:
        linear-gradient(
            145deg,
            #0d1c2e,
            #0a1727
        ) !important;

    color:
        #eef6fc !important;

    font-size:
        14px !important;

    line-height:
        1.65 !important;

    resize:
        none;

    box-shadow:
        0 16px 45px rgba(0,0,0,0.12) !important;

    transition:
        border 0.18s ease,
        box-shadow 0.18s ease;
}


[data-testid="stTextArea"] textarea::placeholder {
    color: #52687d !important;
}


[data-testid="stTextArea"] textarea:focus {

    border-color:
        rgba(34,211,238,0.38) !important;

    box-shadow:
        0 0 0 2px rgba(34,211,238,0.04),
        0 18px 50px rgba(0,0,0,0.15) !important;
}


[data-testid="stTextArea"] label {
    display: none;
}


/* ==========================================================
   PRIMARY MAIN BUTTON
   ========================================================== */

.main .stButton > button[kind="primary"] {

    min-height: 48px;

    border: none !important;

    border-radius: 12px !important;

    background:
        linear-gradient(
            100deg,
            #0891b2,
            #2563eb
        ) !important;

    color:
        white !important;

    font-size:
        12px !important;

    font-weight:
        650 !important;

    box-shadow:
        0 10px 28px rgba(37,99,235,0.18);

    transition:
        all 0.18s ease;
}


.main .stButton > button[kind="primary"]:hover {

    transform:
        translateY(-1px);

    box-shadow:
        0 14px 35px rgba(37,99,235,0.27);
}


/* ==========================================================
   SUGGESTION BUTTONS
   ========================================================== */

.main .stButton > button:not([kind="primary"]) {

    min-height:
        41px;

    border-radius:
        11px !important;

    border:
        1px solid rgba(148,163,184,0.10) !important;

    background:
        rgba(11,26,43,0.72) !important;

    color:
        #7f94a9 !important;

    font-size:
        10px !important;

    font-weight:
        500 !important;

    transition:
        all 0.17s ease;
}


.main .stButton > button:not([kind="primary"]):hover {

    background:
        rgba(34,211,238,0.045) !important;

    border-color:
        rgba(34,211,238,0.19) !important;

    color:
        #d7e4ef !important;
}


/* ==========================================================
   ANSWER CONTAINER
   ========================================================== */

[data-testid="stVerticalBlockBorderWrapper"] {

    background:
        linear-gradient(
            145deg,
            rgba(13,29,47,0.94),
            rgba(8,20,34,0.92)
        ) !important;

    border:
        1px solid rgba(148,163,184,0.11) !important;

    border-radius:
        18px !important;

    box-shadow:
        0 18px 55px rgba(0,0,0,0.14);
}


/* ==========================================================
   MARKDOWN
   ========================================================== */

[data-testid="stMarkdownContainer"] p {

    line-height:
        1.75;
}

[data-testid="stMarkdownContainer"] li {

    line-height:
        1.7;
}

[data-testid="stMarkdownContainer"] strong {

    color:
        #eaf3fa;
}


/* ==========================================================
   EXPANDERS / SOURCES
   ========================================================== */

[data-testid="stExpander"] {

    border:
        1px solid rgba(148,163,184,0.10) !important;

    border-radius:
        12px !important;

    background:
        rgba(10,24,40,0.68);

    margin-bottom:
        7px;
}

[data-testid="stExpander"] summary {

    color:
        #9aadc0 !important;

    font-size:
        11px !important;
}


/* ==========================================================
   ALERTS
   ========================================================== */

[data-testid="stAlert"] {

    border-radius:
        13px !important;

    border:
        1px solid rgba(148,163,184,0.11) !important;
}


/* ==========================================================
   DIVIDER
   ========================================================== */

hr {

    border-color:
        rgba(148,163,184,0.08) !important;
}


/* ==========================================================
   SPINNER
   ========================================================== */

[data-testid="stSpinner"] {

    color:
        #7e94a9 !important;
}


/* ==========================================================
   SCROLLBAR
   ========================================================== */

::-webkit-scrollbar {
    width: 6px;
}

::-webkit-scrollbar-track {
    background: #07111f;
}

::-webkit-scrollbar-thumb {

    background:
        #263b50;

    border-radius:
        20px;
}


/* ==========================================================
   MOBILE
   ========================================================== */

@media(max-width:768px) {

    .block-container {

        padding-left:
            1rem;

        padding-right:
            1rem;
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

if "recent_chats" not in st.session_state:
    st.session_state.recent_chats = []


# ============================================================
# FUNCTIONS
# ============================================================

def new_chat():

    st.session_state.question_text = ""
    st.session_state.answer = None
    st.session_state.sources = []
    st.session_state.last_question = ""


def load_recent_chat(question):

    st.session_state.question_text = question
    st.session_state.answer = None
    st.session_state.sources = []
    st.session_state.last_question = ""


def set_example(question):

    st.session_state.question_text = question


def save_recent_chat(question):

    question = question.strip()

    if not question:
        return

    if question in st.session_state.recent_chats:
        st.session_state.recent_chats.remove(
            question
        )

    st.session_state.recent_chats.insert(
        0,
        question
    )

    st.session_state.recent_chats = (
        st.session_state.recent_chats[:8]
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    # --------------------------------------------------------
    # BRAND
    # --------------------------------------------------------

    brand_left, brand_right = st.columns(
        [1, 4],
        vertical_alignment="center"
    )

    with brand_left:

        st.markdown(
            "## ✚"
        )

    with brand_right:

        st.title(
            "Medicare AI"
        )

        st.caption(
            "MEDICAL INTELLIGENCE"
        )


    st.write("")


    # --------------------------------------------------------
    # NEW CHAT
    # --------------------------------------------------------

    st.button(
        "＋  New Chat",
        type="primary",
        use_container_width=True,
        on_click=new_chat,
    )


    st.write("")


    # --------------------------------------------------------
    # RECENT CHATS
    # --------------------------------------------------------

    st.caption(
        "RECENT CHATS"
    )


    if not st.session_state.recent_chats:

        st.caption(
            "No conversations yet."
        )

    else:

        for index, chat in enumerate(
            st.session_state.recent_chats
        ):

            if len(chat) > 31:

                display_chat = (
                    chat[:31] + "..."
                )

            else:

                display_chat = chat


            st.button(
                "◷  " + display_chat,
                key=f"recent_{index}",
                use_container_width=True,
                on_click=load_recent_chat,
                args=(chat,),
            )


# ============================================================
# MAIN HEADER
# ============================================================

header_left, header_right = st.columns(
    [5, 1],
    vertical_alignment="center"
)


with header_left:

    st.caption(
        "MEDICARE AI  /  MEDICAL KNOWLEDGE ASSISTANT"
    )


with header_right:

    st.caption(
        "●  SYSTEM ONLINE"
    )


st.divider()


# ============================================================
# WELCOME AREA
# ============================================================

if not st.session_state.answer:

    st.write("")
    st.write("")

    center_left, center, center_right = st.columns(
        [0.8, 5, 0.8]
    )


    with center:

        st.caption(
            "✦  EVIDENCE-GROUNDED MEDICAL INTELLIGENCE"
        )

        st.title(
            "How can Medicare AI help you?"
        )

        st.write(
            """
            Ask a medical question in natural language.
            Medicare AI retrieves relevant information from its
            medical knowledge base and generates a clear,
            evidence-grounded response.
            """
        )


    st.write("")
    st.write("")


# ============================================================
# QUESTION COMPOSER
# ============================================================

st.subheader(
    "Medical Knowledge Assistant"
)

st.caption(
    "Ask about medical conditions, symptoms, treatments, "
    "medications, prevention, or general health knowledge."
)


question = st.text_area(
    "Question",
    key="question_text",
    height=150,
    placeholder=(
        "Ask Medicare AI a medical question...\n\n"
        "Example: What is hypertension, what causes it, "
        "and how is it generally managed?"
    ),
)


# ============================================================
# SUBMIT ROW
# ============================================================

information_column, submit_column = st.columns(
    [4, 1.35],
    vertical_alignment="center"
)


with information_column:

    st.caption(
        "✦ Responses are generated using retrieved "
        "medical knowledge."
    )


with submit_column:

    ask_button = st.button(
        "Ask Medicare AI  →",
        type="primary",
        use_container_width=True,
    )


# ============================================================
# SUGGESTED QUESTIONS
# ============================================================

if not st.session_state.answer:

    st.write("")

    st.caption(
        "SUGGESTED QUESTIONS"
    )


    example1, example2, example3, example4 = (
        st.columns(4)
    )


    with example1:

        st.button(
            "Hypertension",
            use_container_width=True,
            key="hypertension",
            on_click=set_example,
            args=(
                "What is hypertension and how is it managed?",
            ),
        )


    with example2:

        st.button(
            "Diabetes",
            use_container_width=True,
            key="diabetes",
            on_click=set_example,
            args=(
                "What is diabetes mellitus and what causes it?",
            ),
        )


    with example3:

        st.button(
            "Asthma",
            use_container_width=True,
            key="asthma",
            on_click=set_example,
            args=(
                "What are the common symptoms and causes of asthma?",
            ),
        )


    with example4:

        st.button(
            "Migraine",
            use_container_width=True,
            key="migraine",
            on_click=set_example,
            args=(
                "What causes migraine headaches?",
            ),
        )


# ============================================================
# PROCESS QUESTION
# ============================================================

if ask_button:

    clean_question = question.strip()


    if not clean_question:

        st.warning(
            "Please enter a medical question."
        )


    else:

        try:

            with st.spinner(
                "Searching medical knowledge and "
                "preparing your answer..."
            ):

                # --------------------------------------------
                # EXISTING RAG BACKEND
                # --------------------------------------------

                from rag import ask_medical_question


                answer, retrieved_documents = (
                    ask_medical_question(
                        clean_question
                    )
                )


            # ================================================
            # PREPARE RETRIEVED SOURCES
            # ================================================

            source_data = []


            for number, document in enumerate(
                retrieved_documents,
                start=1,
            ):

                page = document.metadata.get(
                    "page",
                    "Unknown"
                )


                source_file = document.metadata.get(
                    "source",
                    "Medical Knowledge Base"
                )


                excerpt = (
                    document.page_content.strip()
                )


                if len(excerpt) > 700:

                    excerpt = (
                        excerpt[:700]
                        + "..."
                    )


                source_data.append(
                    {
                        "number": number,
                        "page": page,
                        "source": source_file,
                        "excerpt": excerpt,
                    }
                )


            # ================================================
            # SAVE RESULT
            # ================================================

            st.session_state.answer = answer

            st.session_state.sources = (
                source_data
            )

            st.session_state.last_question = (
                clean_question
            )


            # ================================================
            # SAVE RECENT CHAT
            # ================================================

            save_recent_chat(
                clean_question
            )


            # ================================================
            # REFRESH UI
            # ================================================

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
# ANSWER
# ============================================================

if st.session_state.answer:

    st.write("")
    st.write("")

    st.divider()

    st.write("")


    # ========================================================
    # USER QUESTION
    # ========================================================

    st.caption(
        "YOUR QUESTION"
    )


    with st.container(
        border=True
    ):

        st.write(
            st.session_state.last_question
        )


    st.write("")


    # ========================================================
    # MEDICARE AI RESPONSE HEADER
    # ========================================================

    response_icon, response_title = st.columns(
        [0.45, 8],
        vertical_alignment="center"
    )


    with response_icon:

        st.markdown(
            "### ✚"
        )


    with response_title:

        st.subheader(
            "Medicare AI"
        )

        st.caption(
            "EVIDENCE-GROUNDED RESPONSE"
        )


    # ========================================================
    # ANSWER CARD
    # ========================================================

    with st.container(
        border=True
    ):

        st.markdown(
            st.session_state.answer
        )


        st.divider()


        st.caption(
            "Response generated using information retrieved "
            "from the medical knowledge base."
        )


    # ========================================================
    # RETRIEVED EVIDENCE
    # ========================================================

    if st.session_state.sources:

        st.write("")
        st.write("")

        st.subheader(
            "Retrieved Evidence"
        )


        st.caption(
            "Sources retrieved from the medical knowledge "
            "base for this response."
        )


        st.write("")


        for source in st.session_state.sources:

            number = source["number"]

            page = source["page"]

            source_file = source["source"]

            excerpt = source["excerpt"]


            with st.expander(
                f"Source {number:02d}  ·  Page {page}"
            ):

                try:

                    file_name = Path(
                        str(source_file)
                    ).name

                except Exception:

                    file_name = (
                        "Medical Knowledge Base"
                    )


                st.caption(
                    file_name
                )


                st.write(
                    excerpt
                )


# ============================================================
# FOOTER
# ============================================================

st.write("")
st.write("")
st.write("")

st.divider()


footer_left, footer_center, footer_right = (
    st.columns(
        [1, 2.5, 1]
    )
)


with footer_center:

    st.caption(
        "Medicare AI provides educational medical information "
        "and does not replace professional diagnosis, "
        "emergency care, or individualized medical treatment."
    )