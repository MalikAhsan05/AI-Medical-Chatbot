# ============================================================
# MEDICAL RAG CHATBOT - PHASE 1
# CREATE VECTOR DATABASE / MEMORY
# ============================================================
#
# PURPOSE:
# This file takes our medical PDF and converts it into a
# searchable FAISS vector database.
#
# Complete flow:
#
# Medical PDF
#     ↓
# Load PDF pages
#     ↓
# Split text into smaller chunks
#     ↓
# Convert chunks into embeddings
#     ↓
# Store embeddings in FAISS
#     ↓
# Save FAISS database locally
#
# ============================================================


# ============================================================
# 1. IMPORT REQUIRED LIBRARIES
# ============================================================

# PyPDFLoader reads the PDF and converts each PDF page
# into a LangChain Document object.
from langchain_community.document_loaders import PyPDFLoader


# RecursiveCharacterTextSplitter breaks large pieces of text
# into smaller chunks while trying to preserve natural text
# boundaries such as paragraphs and sentences.
from langchain_text_splitters import RecursiveCharacterTextSplitter


# HuggingFaceEmbeddings allows LangChain to use a
# Hugging Face / Sentence Transformer embedding model.
from langchain_huggingface import HuggingFaceEmbeddings


# FAISS is our vector database.
# It stores the numerical embeddings and allows fast
# similarity searches later when the user asks a question.
from langchain_community.vectorstores import FAISS


# Path helps us create file/folder paths safely.
from pathlib import Path


# ============================================================
# 2. DEFINE PROJECT PATHS
# ============================================================

# This gets the directory where create_memory.py exists.
#
# Example:
# E:\my projects\Medical ChatBot
BASE_DIR = Path(__file__).resolve().parent


# Location of our medical PDF.
#
# Based on your current project structure:
#
# Medical ChatBot/
#     data/
#         medical PDF.pdf
#
PDF_PATH = BASE_DIR / "data" / "medical PDF.pdf"


# Location where FAISS will be saved.
#
# After successful execution, the database files will
# be created inside this directory.
FAISS_PATH = BASE_DIR / "vectorstore" / "FAISS database"


# ============================================================
# 3. CHECK THAT THE PDF ACTUALLY EXISTS
# ============================================================

# Before trying to process the PDF, we check whether Python
# can find it at the expected location.
#
# This gives us a clear error instead of a confusing error
# later in the program.

if not PDF_PATH.exists():
    raise FileNotFoundError(
        f"\nMedical PDF was not found at:\n{PDF_PATH}\n"
        "Make sure 'medical PDF.pdf' exists inside the data folder."
    )


print("\n====================================================")
print(" MEDICAL RAG - VECTOR DATABASE CREATION")
print("====================================================")

print(f"\nPDF found:")
print(PDF_PATH)


# ============================================================
# 4. LOAD THE MEDICAL PDF
# ============================================================

print("\n[1/5] Loading medical PDF...")
print("This PDF is large, so this step may take some time.\n")


# PyPDFLoader opens our PDF.
loader = PyPDFLoader(str(PDF_PATH))


# load() extracts text from all pages.
#
# Each page becomes approximately one LangChain Document.
#
# A Document contains:
#
# document.page_content  -> extracted text
# document.metadata      -> information such as page number/source
#
documents = loader.load()


print(f"PDF loaded successfully.")
print(f"Total pages/documents loaded: {len(documents)}")


# ============================================================
# 5. REMOVE EMPTY PAGES
# ============================================================

# Some PDF pages may contain:
#
# - images only
# - blank pages
# - almost no extractable text
#
# These pages aren't useful for embeddings.
#
# We therefore keep only documents containing meaningful text.

documents = [
    document
    for document in documents
    if document.page_content
    and len(document.page_content.strip()) > 50
]


print(f"Usable text pages: {len(documents)}")


# ============================================================
# 6. CREATE THE TEXT SPLITTER
# ============================================================

print("\n[2/5] Splitting medical text into chunks...")


# Why do we need chunks?
#
# Our encyclopedia contains thousands of pages.
# We don't want to create one embedding for an entire page/book.
#
# Instead:
#
# Page
# ├── Chunk 1
# ├── Chunk 2
# ├── Chunk 3
# └── Chunk 4
#
#
# chunk_size=1000
#
# Each chunk can contain roughly up to 1000 characters.
#
#
# chunk_overlap=200
#
# 200 characters from one chunk can overlap with the next.
#
# Example:
#
# Chunk 1:
# --------------------------------
# Diabetes mellitus is...
# Treatment includes...
# --------------------------------
#
#                  ↓ overlap
#
# Chunk 2:
# --------------------------------
# Treatment includes...
# Patients should...
# --------------------------------
#
# This reduces the chance that important context is lost
# exactly where one chunk ends and another begins.

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", ". ", " ", ""]
)


# split_documents() splits all PDF page Documents
# into smaller Documents.
#
# IMPORTANT:
# LangChain also keeps metadata such as the PDF source/page
# associated with the chunks.
chunks = text_splitter.split_documents(documents)


print("Text splitting completed.")
print(f"Total chunks created: {len(chunks)}")


# ============================================================
# 7. DISPLAY ONE EXAMPLE CHUNK
# ============================================================

# This is only for us to verify that the PDF has been
# extracted and chunked properly.

if chunks:

    print("\n---------------- SAMPLE CHUNK ----------------")

    print(chunks[0].page_content[:1000])

    print("\nMetadata:")
    print(chunks[0].metadata)

    print("----------------------------------------------")


# ============================================================
# 8. LOAD THE EMBEDDING MODEL
# ============================================================

print("\n[3/5] Loading embedding model...")


# We are using:
#
# sentence-transformers/all-MiniLM-L6-v2
#
# This model converts text into numerical vectors.
#
# Example:
#
# "Treatment of diabetes"
#
#              ↓
#
# [0.021, -0.143, 0.582, ...]
#
#
# FAISS doesn't understand English sentences directly.
# It searches these mathematical vector representations.
#
# The model will automatically download from Hugging Face
# the first time you run this script.

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={
        "device": "cpu"
    },
    encode_kwargs={
        "normalize_embeddings": True
    }
)


print("Embedding model loaded successfully.")


# ============================================================
# 9. CREATE THE FAISS VECTOR DATABASE
# ============================================================

print("\n[4/5] Creating embeddings and FAISS database...")

print(
    "The program is now converting the medical chunks into "
    "vectors."
)

print(
    "Because your medical PDF is very large, this can take "
    "a significant amount of time on CPU."
)


# FAISS.from_documents() performs TWO important operations:
#
# 1. Sends every chunk to our embedding model
#
#       Medical chunk
#            ↓
#       Embedding model
#            ↓
#       Numerical vector
#
#
# 2. Stores those vectors together with their associated
#    text and metadata inside FAISS.
#
#
# Final result:
#
# Chunk 1 → Vector 1
# Chunk 2 → Vector 2
# Chunk 3 → Vector 3
# ...
#
# Later, the user's question will also be converted into
# a vector and FAISS will find the most similar vectors.

vector_store = FAISS.from_documents(
    documents=chunks,
    embedding=embedding_model
)


print("FAISS database created successfully.")


# ============================================================
# 10. CREATE THE OUTPUT DIRECTORY
# ============================================================

# parents=True
# creates parent directories when necessary.
#
# exist_ok=True
# means Python will not throw an error if the folder
# already exists.

FAISS_PATH.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# 11. SAVE THE FAISS DATABASE
# ============================================================

print("\n[5/5] Saving FAISS database...")


# This stores our vector database on the computer.
#
# The important benefit is:
#
# We DO NOT have to process the 4500-page PDF every time
# we start the chatbot.
#
# We create the embeddings once and save them.
#
# Later rag.py will simply load this saved database.

vector_store.save_local(str(FAISS_PATH))


# ============================================================
# 12. FINISHED
# ============================================================

print("\n====================================================")
print(" SUCCESS!")
print("====================================================")

print(f"""
Medical PDF processed successfully.

Pages loaded       : {len(documents)}
Chunks created     : {len(chunks)}
Embedding model    : all-MiniLM-L6-v2

FAISS database saved at:
{FAISS_PATH}
""")

print("Phase 1 completed: Medical knowledge base is ready.")
print("====================================================\n")