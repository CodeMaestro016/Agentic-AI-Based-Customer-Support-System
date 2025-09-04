# rag_agent.py
import os
from dotenv import load_dotenv
from crewai import Agent   # you can still use Task/Crew if needed
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

PERSIST_DIR = "chroma_mediconnect"
K = 10   # retrieve more chunks for better coverage

print("Loading embeddings & vectorstore...")
embeddings = OpenAIEmbeddings()
vectordb = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)

# Use MMR for diverse retrieval
retriever = vectordb.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": K,
        "fetch_k": 50,
        "lambda_mult": 0.5
    }
)

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.2)

# Custom prompts to ensure listing ALL relevant doctors
QUESTION_PROMPT = PromptTemplate.from_template(
"""You are given context from the MediConnect knowledge base.

Question: {question}

Use ONLY the provided context. If the question is about a specialty (e.g., Neurology),
list ALL doctors for that specialty you can find in the context (not just one).
Output as bullet points: Doctor name, specialty, and any schedule/notes present.
If none found, say so.

Context:
{context}
"""
)

COMBINE_PROMPT = PromptTemplate.from_template(
"""You will combine multiple partial answers into ONE final, deduplicated list.
Merge duplicates, keep all doctors that match the requested specialty.

Partial answers:
{summaries}

Final answer (bullet list of ALL doctors + any schedules/notes):"""
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="map_reduce",
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={
        "question_prompt": QUESTION_PROMPT,
        "combine_prompt": COMBINE_PROMPT
    },
)

query_handler_agent = Agent(
    role="MediConnect RAG Agent",
    goal="Answer user questions about MediConnect KB using the KB contents and cite sources when possible",
    backstory="You are a friendly assistant that answers questions using the MediConnect knowledge base.",
    llm=llm,
    verbose=True,
    memory=True,
    allow_delegation=False,
    tools=[]
)


def answer_query(user_query: str):
    result = qa_chain({"query": user_query})
    answer = result["result"]
    source_docs = result.get("source_documents", [])

    sources = []
    for i, d in enumerate(source_docs, start=1):
        meta = d.metadata or {}
        src = meta.get("source") or meta.get("page") or f"chunk_{i}"
        snippet = d.page_content.strip().replace("\n", " ")
        if len(snippet) > 300:
            snippet = snippet[:300] + "..."
        sources.append({"source": src, "snippet": snippet})
    return {"answer": answer, "sources": sources}


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
