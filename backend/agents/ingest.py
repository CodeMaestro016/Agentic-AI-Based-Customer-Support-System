# do this once (or only when the PDF changes).
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

PDF_PATH = "data/MediConnect_Channeling_Center_KB[1].pdf"
PERSIST_DIR = "chroma_mediconnect"
MANIFEST = os.path.join(PERSIST_DIR, "manifest.json")

def sha256_of_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return h.hexdigest()

def ingest(pdf_path=PDF_PATH, persist_dir=PERSIST_DIR, force_reindex=False, chunk_size=500, chunk_overlap=50):
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

    print(f"Splitting into chunks (size={chunk_size}, overlap={chunk_overlap})...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_documents(docs)

    print(f"Creating embeddings for {len(chunks)} chunks...")
    embeddings = OpenAIEmbeddings()   # requires OPENAI_API_KEY. Replace if you prefer a local model.

    print(f"Persisting to Chroma @ {persist_dir} ...")
    vectordb = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=persist_dir)
    vectordb.persist()

    manifest = {"sha256": file_hash, "num_chunks": len(chunks), "source": os.path.basename(pdf_path)}
    with open(MANIFEST, "w") as mf:
        json.dump(manifest, mf, indent=2)

    print("Ingestion complete. Manifest written.")

if __name__ == "__main__":
    ingest()
 