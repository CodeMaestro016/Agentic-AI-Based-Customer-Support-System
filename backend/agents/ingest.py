# do this once (or only when the PDF changes).

# ---------------------------------------------------------------
# This script ingests a PDF knowledge base into a Chroma vectorstore.
# It:
#   - Calculates a hash of the PDF to detect changes.
#   - Loads and splits the PDF into text chunks.
#   - Embeds the chunks using OpenAI embeddings.
#   - Persists the embeddings into a Chroma database for retrieval.
#   - Skips re-indexing if the PDF hasn't changed since the last run.
# ---------------------------------------------------------------

import os
import json
import hashlib
from dotenv import load_dotenv

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings      # or replace with HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

PDF_PATH = "../../data/MediConnect_Channeling_Center_KB[1].pdf"  # Path to your PDF knowledge base
PERSIST_DIR = "chroma_mediconnect"                              # Folder where vectorstore will be saved
MANIFEST = os.path.join(PERSIST_DIR, "manifest.json")           # File storing metadata (PDF hash, num chunks, etc.)

# Helper function: Compute SHA-256 hash of the PDF
def sha256_of_file(path):
    """
    Compute SHA-256 hash of a file to detect changes.
    Reads the file in 64KB blocks to handle large files efficiently.
    """
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return h.hexdigest()

def ingest(pdf_path=PDF_PATH, persist_dir=PERSIST_DIR, force_reindex=False, chunk_size=500, chunk_overlap=50):
    """
    Ingests the given PDF into a Chroma vectorstore.
    
    Args:
        pdf_path (str): Path to the PDF file.
        persist_dir (str): Directory where Chroma DB will be stored.
        force_reindex (bool): If True, forces re-indexing even if file hasn't changed.
        chunk_size (int): Max size of each text chunk (not currently used; hardcoded below).
        chunk_overlap (int): Number of overlapping characters between chunks (not currently used; hardcoded below).
    """
    os.makedirs(persist_dir, exist_ok=True)
    file_hash = sha256_of_file(pdf_path)
    if os.path.exists(MANIFEST) and not force_reindex:
        with open(MANIFEST, "r") as mf:
            data = json.load(mf)
            if data.get("sha256") == file_hash:
                print("No changes detected in PDF. Skipping ingestion.")
                return
            else:
                print("Change detected in PDF. Reindexing...")

    print("Loading PDF...")
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

      # ingest.py (only the splitter part + force reindex for this run)

    print(f"Splitting into chunks ...")
    splitter = RecursiveCharacterTextSplitter(
    # keep lists together as much as possible
        chunk_size=1200, # Max size of each chunk
        chunk_overlap=200,# Overlap between chunks for better context continuity
        separators=["\n\n", "\n", " "],   # be gentle splitting lists
        add_start_index=True # Keep track of original positions
    )
    chunks = splitter.split_documents(docs)

    print(f"Creating embeddings for {len(chunks)} chunks...")
    embeddings = OpenAIEmbeddings()

    print(f"Persisting to Chroma @ {persist_dir} ...")
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_dir
    )
    vectordb.persist()

# Write manifest file to record current PDF state
    manifest = {"sha256": file_hash, "num_chunks": len(chunks), "source": os.path.basename(pdf_path)}
    with open(MANIFEST, "w") as mf:
        json.dump(manifest, mf, indent=2)

    print("Ingestion complete. Manifest written.")

if __name__ == "__main__":
    ingest()
 