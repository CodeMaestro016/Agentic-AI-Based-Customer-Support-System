# rag_agent.py

import os
from dotenv import load_dotenv
from crewai import Agent   # Optional: For persona and metadata
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# -------------------------------------------------------------------
# 1. Load environment variables (like your OpenAI API key)
# -------------------------------------------------------------------
load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# -------------------------------------------------------------------
# 2. Paths and retrieval settings
# -------------------------------------------------------------------
PERSIST_DIR = "chroma_mediconnect"   # where your Chroma DB is stored
K = 10                               # number of chunks to retrieve

# -------------------------------------------------------------------
# 3. Load embeddings and connect to Chroma vector database
# -------------------------------------------------------------------
print("Loading embeddings & vectorstore...")
embeddings = OpenAIEmbeddings()
vectordb = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)

# Use MMR retrieval to ensure diversity (not just last chunks)
retriever = vectordb.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": K,          # final results returned
        "fetch_k": 50,   # candidate pool
        "lambda_mult": 0.5  # balance between relevance and diversity
    }
)

# -------------------------------------------------------------------
# 4. Initialize LLM (GPT model)
# -------------------------------------------------------------------
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.2)

# -------------------------------------------------------------------
# 5. Custom prompts: force the model to return ALL doctors
# -------------------------------------------------------------------
QUESTION_PROMPT = PromptTemplate.from_template(
"""You are given context from the MediConnect knowledge base.

Question: {question}

Use ONLY the provided context. If the question is about a specialty (e.g., Neurology),
list ALL doctors for that specialty (not just one).
Format the answer as a clean bullet list with:
- Doctor name
- Specialty
- Sub-specialty (if available)
- Availability or schedule

If none are found, say: "No doctors found for this specialty."

Context:
{context}
"""
)

# 5a. General QA prompt (for services, facilities, other questions)
GENERAL_PROMPT = PromptTemplate.from_template(
"""You are given context from the MediConnect knowledge base.

Question: {question}

Use ONLY the provided context. 
Answer the question clearly and concisely.
If the question is about services, list ALL available services.
If none are found, say: "No relevant information found."

Context:
{context}
"""
)

# 5b. Doctor-specific prompt (same as before, optimized for doctors)
DOCTOR_PROMPT = PromptTemplate.from_template(
"""You are given context from the MediConnect knowledge base.

Question: {question}

Use ONLY the provided context. If the question is about a specialty (e.g., Neurology),
list ALL doctors for that specialty (not just one).
Format as a bullet list with:
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
"""Combine all the partial answers into ONE final answer.
Merge duplicates, and include everything relevant.

Partial answers:
{summaries}

Final clean answer:"""
)


# -------------------------------------------------------------------
# 6. Create RetrievalQA chain (map_reduce ensures all chunks are merged)
# -------------------------------------------------------------------
def get_qa_chain(user_query: str):
    """Return the appropriate RetrievalQA chain based on query type."""
    if "doctor" in user_query.lower() or "specialist" in user_query.lower():
        prompt = DOCTOR_PROMPT
    else:
        prompt = GENERAL_PROMPT

    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="map_reduce",
        retriever=retriever,
        return_source_documents=False,
        chain_type_kwargs={
            "question_prompt": prompt,
            "combine_prompt": COMBINE_PROMPT
        },
    )


# -------------------------------------------------------------------
# 7. Define the Agent (optional, for persona/memory)
# -------------------------------------------------------------------
query_handler_agent = Agent(
    role="MediConnect RAG Agent",
    goal="Answer user questions about MediConnect KB clearly and completely.",
    backstory="You are a helpful assistant for MediConnect, answering based on the knowledge base.",
    llm=llm,
    verbose=False,   # less noisy logs
    memory=True,
    allow_delegation=False,
    tools=[]
)

# -------------------------------------------------------------------
# 8. Helper function to query the knowledge base
# -------------------------------------------------------------------
def answer_query(user_query: str):
    qa_chain = get_qa_chain(user_query)   # choose prompt based on questionwhat are the services do you have?
    result = qa_chain({"query": user_query})
    return result["result"]



# -------------------------------------------------------------------
# 9. Interactive loop (simple CLI chatbot)
# -------------------------------------------------------------------
if __name__ == "__main__":
    print("MediConnect RAG Agent ready. Type a question (or 'quit'):")
    while True:
        q = input("\n> ").strip()
        if not q or q.lower() in ("quit", "exit"):
            break
        answer = answer_query(q)
        print("\n--- ANSWER ---\n")
        print(answer)
