import streamlit as st
from rag import ask_medical_question

st.set_page_config(
    page_title="MedRAG Test",
    layout="wide"
)

st.title("🩺 MedRAG AI")

st.success("Streamlit UI is working correctly!")

st.write(
    "If you can see this message, Streamlit itself is fine "
    "and the problem is coming from the RAG import."
)