# ---------------------------------------------------------------
# PDF → Chroma VectorStore Ingestion
# ---------------------------------------------------------------
# - Detects PDF changes using SHA-256
# - Loads and splits into semantic chunks
# - Creates embeddings using OpenAI
# - Saves to persistent Chroma DB
# - Skips re-indexing if no changes detected
# - On updates: deletes previous embeddings for the same PDF source
# ---------------------------------------

import os
import json
import hashlib
from pathlib import Path
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

# --- Config ---
load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

PDF_PATH = "data/MediConnect_Channeling_Center_KB[1].pdf"
# Always persist under backend/chroma_mediconnect regardless of CWD
PERSIST_DIR = str(Path(__file__).resolve().parents[1] / "chroma_mediconnect")
MANIFEST = os.path.join(PERSIST_DIR, "manifest.json")

# --- Helper: Hash function ---
def sha256_of_file(path):
    """Compute SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return h.hexdigest()

# --- Main ingestion function ---
def ingest(pdf_path=PDF_PATH, persist_dir=PERSIST_DIR, force_reindex=False):
    """Load PDF, split, embed, and store in Chroma; delete old embeddings for same source when updating.

    Returns a dict with manifest-like info: {sha256, num_chunks, source}.
    """
    os.makedirs(persist_dir, exist_ok=True)
    file_hash = sha256_of_file(pdf_path)
    source_name = os.path.basename(pdf_path)

    # Check manifest to skip re-indexing if unchanged
    if os.path.exists(MANIFEST) and not force_reindex:
        with open(MANIFEST, "r") as mf:
            data = json.load(mf)
            if data.get("sha256") == file_hash:
                print("✅ No changes detected in PDF. Skipping ingestion.")
                return {"sha256": file_hash, "num_chunks": data.get("num_chunks", 0), "source": data.get("source", source_name), "skipped": True}
            else:
                print("🔄 Change detected in PDF. Re-indexing...")

    # Load the PDF
    print("📄 Loading PDF...")
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    # Split into chunks
    print("✂️ Splitting into chunks ...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=200,
        separators=["\n\n", "\n", " "],
        add_start_index=True
    )
    chunks = splitter.split_documents(docs)
    print(f"🧩 Created {len(chunks)} chunks")

    # Normalize metadata: ensure 'source' is the basename for delete queries
    for c in chunks:
        c.metadata = c.metadata or {}
        c.metadata["source"] = source_name

    # Create embeddings
    print("🧠 Creating embeddings...")
    embeddings = OpenAIEmbeddings()

    # Open persistent DB and delete any existing items for this source
    vectordb = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    try:
        deleted = vectordb.delete(where={"source": source_name})
        if deleted:
            print(f"🗑️ Deleted previous embeddings for {source_name}")
    except Exception as _:
        # Some versions return None; proceed regardless
        pass

    # Add new documents
    print(f"💾 Saving embeddings to {persist_dir} ...")
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_dir
    )
    vectordb.persist()

    # Write manifest
    manifest = {
        "sha256": file_hash,
        "num_chunks": len(chunks),
        "source": source_name
    }
    with open(MANIFEST, "w") as mf:
        json.dump(manifest, mf, indent=2)

    print("✅ Ingestion complete. Manifest updated.")
    return manifest

# --- CLI runner ---
if __name__ == "__main__":
    print("📘 Starting MediConnect PDF ingestion...")
    ingest(force_reindex=False)
