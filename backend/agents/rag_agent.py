# rag_agent.py
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew   # optional: we'll use Agent mainly for metadata/memory like your example
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

PERSIST_DIR = "chroma_mediconnect"
K = 4   # how many chunks to retrieve

# load embeddings and vectorstore
print("Loading embeddings & vectorstore...")
embeddings = OpenAIEmbeddings()
vectordb = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)
retriever = vectordb.as_retriever(search_kwargs={"k": K})

# LLM setup (same family you're using)
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.2)  # or adjust temperature

# Retrieval QA chain: this will feed retrieved docs to the LLM
qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True)

# optional: create a CrewAI agent for persona/memory like your sample
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
    # Run the retrieval+answer chain
    result = qa_chain({"query": user_query})
    answer = result["result"]
    source_docs = result.get("source_documents", [])

    # Build compact source list (source metadata and snippet)
    sources = []
    for i, d in enumerate(source_docs, start=1):
        meta = d.metadata or {}
        src = meta.get("source") or meta.get("page") or f"chunk_{i}"
        snippet = d.page_content.strip().replace("\n"," ")
        if len(snippet) > 300:
            snippet = snippet[:300] + "..."
        sources.append({"source": src, "snippet": snippet})
    return {"answer": answer, "sources": sources}

if __name__ == "__main__":
    # quick interactive mode
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
