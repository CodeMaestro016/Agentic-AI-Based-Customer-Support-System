import os
from pathlib import Path
from dotenv import load_dotenv
from crewai import Agent
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# 1. Load environment variables
load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# 2. Paths and retrieval settings
# Persist under backend/chroma_mediconnect regardless of CWD
PERSIST_DIR = str(Path(__file__).resolve().parents[1] / "chroma_mediconnect")
K = 15

# 3. Load embeddings and vectorstore
print("Loading embeddings & vectorstore...")
embeddings = OpenAIEmbeddings()
vectordb = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)
retriever = vectordb.as_retriever(
    search_type="similarity",
    search_kwargs={"k": K}
)

# 4. Initialize model
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.2)

# 5. Prompts
GENERAL_PROMPT = PromptTemplate.from_template(
"""You are given context from the MediConnect knowledge base.

Question: {question}

Use ONLY the provided context. 
If the question is about services, list ALL available services clearly.
If none are found, say: "No relevant information found."

Context:
{context}
"""
)

DOCTOR_PROMPT = PromptTemplate.from_template(
"""You are given context from the MediConnect knowledge base.

Question: {question}

Use ONLY the provided context. If the question is about a specialty (e.g., Neurology),
list ALL doctors for that specialty (not just one).
Format the answer as:
- Doctor name
- Specialty
- Sub-specialty (if available)
- Availability or schedule

If none found, say: "No doctors found for this specialty."

Context:
{context}
"""
)

COMBINE_PROMPT = PromptTemplate.from_template(
"""Combine all partial answers into ONE final answer.
Merge duplicates and include everything relevant.

Partial answers:
{summaries}

Final clean answer:"""
)

# 6. Chain selector
def get_qa_chain(user_query: str):
    if "doctor" in user_query.lower() or "specialist" in user_query.lower():
        prompt = DOCTOR_PROMPT
    else:
        prompt = GENERAL_PROMPT

    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={
            "prompt": prompt
        },
    )

# 7. Agent setup
query_handler_agent = Agent(
    role="MediConnect RAG Agent",
    goal="Answer user questions about MediConnect knowledge base accurately.",
    backstory="You are a helpful assistant for MediConnect, answering from the KB.",
    llm=llm,
    verbose=False,
    memory=True,
    allow_delegation=False,
    tools=[]
)

# 8. Query handler
def answer_query(user_query: str):
    qa_chain = get_qa_chain(user_query)
    result = qa_chain({"query": user_query})

    answer = result.get("result", "").strip()
    source_docs = result.get("source_documents", [])
    sources = []

    for i, d in enumerate(source_docs, start=1):
        meta = d.metadata or {}
        src = meta.get("source") or f"chunk_{i}"
        snippet = d.page_content.strip().replace("\n", " ")
        if len(snippet) > 300:
            snippet = snippet[:300] + "..."
        sources.append({"source": src, "snippet": snippet})

    # Strict policy: if no retrieved sources, do not return a model-generated answer
    if not sources:
        return {"answer": "No relevant information found.", "sources": []}

    # If sources exist but the model produced an empty answer, still indicate no info
    if not answer:
        answer = "No relevant information found."

    return {"answer": answer, "sources": sources}

# 9. CLI
if __name__ == "__main__":
    print("MediConnect RAG Agent ready. Type a question (or 'quit'):")
    while True:
        q = input("\n> ").strip()
        if not q or q.lower() in ("quit", "exit"):
            break
        out = answer_query(q)
        print("\n--- ANSWER ---\n")
        print(out["answer"])
        print("\n--- SOURCES ---")
        for s in out["sources"]:
            print(f"- {s['source']}: {s['snippet']}")
