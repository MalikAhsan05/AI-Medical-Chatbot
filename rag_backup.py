# ============================================================
# MEDICAL RAG CHATBOT - PHASE 2
# ============================================================
#
# PURPOSE:
#
# Phase 1 created our medical memory:
#
# Medical PDF
#     ↓
# Chunks
#     ↓
# Embeddings
#     ↓
# FAISS
#
#
# Phase 2 will do:
#
# User Question
#     ↓
# FAISS Retrieval
#     ↓
# Relevant Medical Context
#     ↓
# Mistral LLM
#     ↓
# Grounded Medical Answer
#
# ============================================================


# ============================================================
# 1. IMPORT REQUIRED LIBRARIES
# ============================================================

import os

from pathlib import Path


# Loads variables stored inside our .env file.
#
# We use this for our Hugging Face token.
from dotenv import load_dotenv


# HuggingFaceEmbeddings loads the SAME embedding model
# that we used during Phase 1.
from langchain_huggingface import HuggingFaceEmbeddings


# HuggingFaceEndpoint allows LangChain to communicate
# with a model hosted through Hugging Face.
from huggingface_hub import InferenceClient


# FAISS allows us to load our existing medical
# vector database.
from langchain_community.vectorstores import FAISS


import os

from pathlib import Path

from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings

from huggingface_hub import InferenceClient

from langchain_community.vectorstores import FAISS


# ============================================================
# 2. LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# Read Hugging Face token from:
#
# .env
#
# HF_TOKEN=hf_xxxxxxxxxxxxx

HF_TOKEN = os.getenv("HF_TOKEN")


# Check whether the token exists.
#
# If it doesn't exist, stop immediately and give
# a useful error.

if not HF_TOKEN:

    raise ValueError(
        "HF_TOKEN was not found.\n"
        "Create a .env file and add:\n"
        "HF_TOKEN=your_huggingface_token"
    )


# ============================================================
# 3. PROJECT PATHS
# ============================================================

# Find our Medical ChatBot project directory.

BASE_DIR = Path(__file__).resolve().parent


# Location of the database created during Phase 1.

FAISS_PATH = BASE_DIR / "vectorstore" / "FAISS database"


# Check that our FAISS database actually exists.

if not FAISS_PATH.exists():

    raise FileNotFoundError(
        f"FAISS database was not found at:\n{FAISS_PATH}"
    )


# ============================================================
# 4. LOAD EMBEDDING MODEL
# ============================================================

print("\nLoading embedding model...")


# IMPORTANT:
#
# This MUST be the same embedding model we used
# when creating the FAISS database.
#
# Phase 1:
# all-MiniLM-L6-v2
#
# Phase 2:
# all-MiniLM-L6-v2
#
# If we use a different embedding model, retrieval
# may not work correctly.

embeddings = HuggingFaceEmbeddings(

    model_name="sentence-transformers/all-MiniLM-L6-v2",

    model_kwargs={
        "device": "cpu"
    },

    encode_kwargs={
        "normalize_embeddings": True
    }
)


print("Embedding model loaded successfully!")


# ============================================================
# 5. LOAD FAISS MEDICAL DATABASE
# ============================================================

print("Loading FAISS medical knowledge base...")


vector_store = FAISS.load_local(

    str(FAISS_PATH),

    embeddings,

    # Our FAISS index.pkl was created locally by us.
    #
    # Never enable this for an untrusted .pkl file.

    allow_dangerous_deserialization=True
)


print("FAISS database loaded successfully!")


# ============================================================
# 6. CREATE THE RETRIEVER
# ============================================================

# A retriever is basically the search component of RAG.
#
#
# User:
# "What is diabetes?"
#
#       ↓
#
# Retriever
#
#       ↓
#
# FAISS searches thousands of chunks
#
#       ↓
#
# Returns the most relevant chunks.
#
#
# k=4 means:
#
# Retrieve FOUR relevant medical chunks.

retriever = vector_store.as_retriever(

    search_kwargs={
        "k": 4
    }
)


# ============================================================
# 7. SET UP THE MISTRAL LLM
# ============================================================

print("Connecting to LLM through Hugging Face...")


# This is the model that will GENERATE the final answer.
#
# IMPORTANT:
#
# MiniLM = Embeddings / retrieval
#
# Mistral = Answer generation
#
# They perform completely different jobs.


# ============================================================
# SET UP MISTRAL USING HUGGING FACE CHAT API
# ============================================================

print("Connecting to LLM through Hugging Face...")


# Create Hugging Face inference client.
#
# provider="auto" tells Hugging Face to automatically
# select an available inference provider.

client = InferenceClient(
    provider="auto",
    api_key=HF_TOKEN
)


# The LLM we want to use.

MODEL_NAME = "Qwen/Qwen3-4B-Instruct-2507"




print("LLM configured successfully!")

print(f"LLM configured: {MODEL_NAME}")


# ============================================================
# 8. CREATE OUR MEDICAL SYSTEM PROMPT
# ============================================================

# This prompt is VERY important.
#
# We don't want Mistral to simply answer from whatever
# it remembers from model training.
#
# We want:
#
# Question
# +
# Retrieved Medical Context
#
# and the model should base its answer on that context.





# ============================================================
# 9. FUNCTION TO FORMAT RETRIEVED DOCUMENTS
# ============================================================

# FAISS returns multiple LangChain Document objects.
#
# We need to combine their text before giving the
# information to Mistral.


def format_documents(documents):

    formatted_text = []

    for document in documents:

        formatted_text.append(document.page_content)

    return "\n\n".join(formatted_text)


# ============================================================
# 10. MAIN RAG FUNCTION
# ============================================================

# ============================================================
# MAIN RAG FUNCTION
# ============================================================

def ask_medical_question(question):

    """
    Complete RAG pipeline:

    User Question
         ↓
    FAISS Retrieval
         ↓
    Medical Context
         ↓
    Hugging Face Chat API
         ↓
    Mistral
         ↓
    Final Answer
    """


    # --------------------------------------------------------
    # STEP A - SEARCH THE FAISS DATABASE
    # --------------------------------------------------------

    print("\nSearching medical knowledge base...")


    # Search our medical FAISS database using the question.
    #
    # The retriever returns the 4 most relevant chunks.

    documents = retriever.invoke(question)


    print(
        f"Retrieved {len(documents)} relevant medical chunks."
    )


    # --------------------------------------------------------
    # STEP B - FORMAT THE RETRIEVED DOCUMENTS
    # --------------------------------------------------------

    # Combine the 4 retrieved chunks into one context.

    context = format_documents(documents)


    # --------------------------------------------------------
    # STEP C - CREATE SYSTEM INSTRUCTIONS
    # --------------------------------------------------------

    # The system message tells Mistral how it should behave.

    system_message = """
You are a medical information assistant using a retrieved
medical knowledge base.

Use the provided medical context as the basis for your answer.

IMPORTANT RULES:

1. Do not invent medical facts.
2. If the provided context does not contain enough information,
   clearly say that the available knowledge base does not contain
   enough information.
3. Do not provide a definitive diagnosis.
4. Do not prescribe personalized medication or dosages.
5. Explain medical information clearly.
6. If the information indicates a potentially serious or
   emergency condition, recommend seeking appropriate
   professional medical care.
7. Do not claim that information came from the knowledge base
   unless it appears in the provided context.
"""


    # --------------------------------------------------------
    # STEP D - CREATE USER MESSAGE
    # --------------------------------------------------------

    # Here we combine:
    #
    # Retrieved PDF information
    # +
    # User's question

    user_message = f"""
MEDICAL CONTEXT:

{context}


USER QUESTION:

{question}


Please answer the question using the medical context above.
"""


    # --------------------------------------------------------
    # STEP E - SEND EVERYTHING TO MISTRAL
    # --------------------------------------------------------

    print("Generating answer with LLM...")


    response = client.chat_completion(

        model=MODEL_NAME,

        messages=[
            {
                "role": "system",
                "content": system_message
            },

            {
                "role": "user",
                "content": user_message
            }
        ],

        max_tokens=500,

        temperature=0.2
    )


    # --------------------------------------------------------
    # STEP F - GET THE TEXT FROM MISTRAL'S RESPONSE
    # --------------------------------------------------------

    answer = response.choices[0].message.content


    # --------------------------------------------------------
    # STEP G - RETURN ANSWER AND SOURCES
    # --------------------------------------------------------

    return answer, documents


# ============================================================
# 11. TERMINAL TEST
# ============================================================

# This section only runs when we execute:
#
# python rag.py
#
# Later Streamlit's app.py will import
# ask_medical_question() instead.


if __name__ == "__main__":

    print("\n==============================================")
    print(" MEDICAL RAG SYSTEM")
    print("==============================================")


    # Ask the user to type a question.

    question = input(
        "\nEnter your medical question: "
    )


    # Run our RAG pipeline.

    answer, sources = ask_medical_question(question)


    # Display final generated answer.

    print("\n==============================================")
    print(" ANSWER")
    print("==============================================\n")

    print(answer)


    # ========================================================
    # DISPLAY SOURCES
    # ========================================================

    print("\n==============================================")
    print(" SOURCES")
    print("==============================================")


    for number, document in enumerate(sources, start=1):

        print(f"\nSource {number}")

        print(
            "Page:",
            document.metadata.get("page", "Unknown")
        )

        print(
            "File:",
            document.metadata.get("source", "Unknown")
        )


    print("\n==============================================")