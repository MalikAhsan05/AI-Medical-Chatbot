# ============================================================
# TEST FAISS DATABASE
# ============================================================
#
# PURPOSE:
# We already created our FAISS database in Phase 1.
#
# Now we want to check:
#
# Question
#    ↓
# FAISS database
#    ↓
# Relevant text from our medical PDF
#
# NO Mistral/LLM is being used yet.
# ============================================================


# ------------------------------------------------------------
# 1. IMPORT REQUIRED LIBRARIES
# ------------------------------------------------------------

from pathlib import Path

# HuggingFaceEmbeddings loads the SAME embedding model
# that we used while creating our FAISS database.
from langchain_huggingface import HuggingFaceEmbeddings

# FAISS allows us to load and search our existing database.
from langchain_community.vectorstores import FAISS


# ------------------------------------------------------------
# 2. FIND OUR PROJECT FOLDER
# ------------------------------------------------------------

# This finds the folder where test_faiss.py exists.
#
# In your case:
# E:\my projects\Medical ChatBot

BASE_DIR = Path(__file__).resolve().parent


# ------------------------------------------------------------
# 3. TELL PYTHON WHERE OUR FAISS DATABASE IS
# ------------------------------------------------------------

# Our database is located at:
#
# Medical ChatBot
#     └── vectorstore
#           └── FAISS database

FAISS_PATH = BASE_DIR / "vectorstore" / "FAISS database"


# ------------------------------------------------------------
# 4. LOAD THE EMBEDDING MODEL
# ------------------------------------------------------------

print("\nLoading embedding model...")


# IMPORTANT:
# We use the SAME model that was used in create_memory.py.
#
# all-MiniLM-L6-v2 converts text/questions into numerical
# vectors so that FAISS can compare them.

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True}
)


print("Embedding model loaded successfully!")


# ------------------------------------------------------------
# 5. LOAD OUR EXISTING FAISS DATABASE
# ------------------------------------------------------------

print("\nLoading FAISS database...")


vector_store = FAISS.load_local(

    # Where our index.faiss and index.pkl files are located
    str(FAISS_PATH),

    # Same embedding model used when database was created
    embeddings,

    # Required by LangChain when loading a locally created
    # FAISS database.
    # Only use this with a database you created/trust.
    allow_dangerous_deserialization=True
)


print("FAISS database loaded successfully!")


# ------------------------------------------------------------
# 6. CREATE A TEST QUESTION
# ------------------------------------------------------------

# This is the medical question that we want FAISS to search
# for inside our medical encyclopedia.

question = "What is diabetes mellitus and how is it treated?"


print("\nQUESTION:")
print(question)


# ------------------------------------------------------------
# 7. SEARCH THE FAISS DATABASE
# ------------------------------------------------------------

# similarity_search() converts our question into an embedding
# and compares it against the embeddings stored in FAISS.
#
# k=3 means:
#
# "Give me the THREE most relevant chunks."

results = vector_store.similarity_search(
    question,
    k=3
)


# ------------------------------------------------------------
# 8. DISPLAY THE RESULTS
# ------------------------------------------------------------

print("\nSearching medical knowledge base...")


# We received 3 results.
# This loop displays them one by one.

for number, result in enumerate(results, start=1):

    print("\n" + "=" * 70)

    print(f"RESULT {number}")

    print("=" * 70)


    # page_content contains the actual text retrieved
    # from our medical PDF.

    print("\nRETRIEVED TEXT:\n")

    print(result.page_content)


    # metadata tells us where the information came from.
    #
    # For example:
    #
    # source = medical PDF.pdf
    # page   = 1234

    print("\nSOURCE INFORMATION:")

    print(result.metadata)


# ------------------------------------------------------------
# 9. FINISH
# ------------------------------------------------------------

print("\n" + "=" * 70)

print("FAISS TEST COMPLETED!")

print("=" * 70)