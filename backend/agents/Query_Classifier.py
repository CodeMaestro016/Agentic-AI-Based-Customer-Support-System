import os
import json
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI

# 1. Setup
load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# Chat history (kept in memory, can also save to file)
chat_history = []



# 2. Query Classifier Agent + Crew
query_classifier_agent = Agent(
    role="Query Classifier Agent",
    goal=(
        "Handle patient queries about symptoms responsibly by first asking clarifying questions "
        "if the symptom is vague (e.g., pain, fever, fatigue, cough). "
        "Examples of clarifying details: duration, severity, specific location, triggers, other symptoms. "
        "Once enough info is gathered, provide a brief summary of the symptom, safe next steps, "
        "and emphasize consulting a doctor."
    ),
    backstory=(
        "You are an empathetic AI assistant helping patients understand symptoms. "
        "Your first step is to gather important missing details before suggesting safe general advice. "
        "You never give a diagnosis. Instead, you guide the user to professional care while showing support."
    ),
    llm=llm,
    verbose=True,
    memory=True,
    allow_delegation=False,
)

query_task = Task(
    description=(
        "Conversation so far: {chat_history}\n\n"
        "The latest patient query is: {patient_query}. "
        "If the symptom is broad or unclear (like 'back pain', 'fever', 'tiredness'), "
        "ask 1–2 clarifying questions such as: duration, severity, exact location, or other symptoms. "
        "If enough detail is provided, then summarize the situation briefly, suggest safe actions (like rest, hydration, OTC relief), "
        "and always include a disclaimer that this is not medical advice and a doctor should be consulted."
    ),
    expected_output=(
        "Either (a) one or two clarifying questions, OR (b) a concise response including symptom details, "
        "safe recommended actions, and a disclaimer."
    ),
    agent=query_classifier_agent
)

query_crew = Crew(
    agents=[query_classifier_agent],
    tasks=[query_task],
    verbose=True,
)



# 3. Medical Summarizer Agent + Crew
medical_summarizer_agent = Agent(
    role="Medical Document Summarizer Agent",
    goal=(
        "Summarize medical research papers, instructions, or clinical documents into clear, "
        "accessible summaries while emphasizing that this is not a substitute for professional medical advice."
    ),
    backstory=(
        "You are an AI specialized in medical document summarization. "
        "You help users quickly grasp key points, risks, and next steps from long documents. "
        "You avoid making clinical decisions and always include a disclaimer."
    ),
    llm=llm,
    verbose=True,
    memory=True,
    allow_delegation=False,
)

summarizer_task = Task(
    description=(
        "Conversation so far: {chat_history}\n\n"
        "The document content is: {document_text}. "
        "Summarize it into key points that are clear and easy to understand. "
        "Highlight important warnings, safe practices, and always include a disclaimer."
    ),
    expected_output=(
        "A concise summary of the document with key points, important risks, and a disclaimer."
    ),
    agent=medical_summarizer_agent
)

summarizer_crew = Crew(
    agents=[medical_summarizer_agent],
    tasks=[summarizer_task],
    verbose=True,
)



# 4. Interactive Terminal Loop
print("Welcome to the Medical Assistant Crew (AI).")
print("👉 Ask a health-related question normally.")
print("👉 To summarize a document, prefix with 'doc:'")
print("👉 Type 'exit' to quit.\n")

while True:
    user_input = input("User: ")
    if user_input.lower() == "exit":
        print("👋 Goodbye! Stay safe.")
        # Save chat history to file for persistence
        with open("chat_history.json", "w", encoding="utf-8") as f:
            json.dump(chat_history, f, indent=2)
        break

    if user_input.startswith("doc:"):
        doc_text = user_input.replace("doc:", "").strip()
        result = summarizer_crew.kickoff(inputs={
            "document_text": doc_text,
            "chat_history": chat_history
        })
    else:
        result = query_crew.kickoff(inputs={
            "patient_query": user_input,
            "chat_history": chat_history
        })

    # Extract the agent’s response
    task_result = result.tasks_output[0]
    response = getattr(task_result, "content", getattr(task_result, "raw", str(task_result)))

    # Update chat history
    chat_history.append({"role": "user", "content": user_input})
    chat_history.append({"role": "agent", "content": response})

    print("Agent:", response)
