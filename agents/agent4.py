import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader

# Load environment variables
load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
if not os.environ['OPENAI_API_KEY']:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")

# Define the LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

# Custom Function: PDF Text Extraction
def read_pdf(file_path: str) -> str:
    if not os.path.exists(file_path):
        return f"Error: File {file_path} does not exist."
    try:
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        full_text = "\n".join([doc.page_content for doc in documents])
        return full_text
    except Exception as e:
        return f"Error loading PDF: {str(e)}"

# Define the Summarizer Agent with enhanced capabilities
summarizer_agent = Agent(
    role="Medical Report Summarizer Agent",
    goal=(
        "Summarize uploaded medical reports by extracting key details like diagnosis, treatments, and recommendations. "
        "Provide an overall assessment of what the report says about the patient's health status (e.g., stable, improving, or concerning), "
        "and if the report indicates any issues, recommend consulting a doctor. Always emphasize that this is not professional medical advice."
    ),
    backstory=(
        "You are an AI expert in analyzing medical documents for customer support in healthcare systems. "
        "You focus on key sections like patient info, symptoms, test results, diagnosis, and next steps. "
        "Provide empathetic summaries, assess overall health based on the report's content, and suggest doctor consultation if needed. "
        "Keep responses concise, objective, and always include a strong disclaimer that AI summaries may have errors and professional review is essential."
    ),
    llm=llm,
    verbose=True,
    memory=True,
    allow_delegation=False,
    tools=[]  # No tools needed; text is passed directly
)

# Define the Summarization Task with stricter structure
summarize_task = Task(
    description=(
        "Summarize the following medical report text: {pdf_text}. "
        "Output MUST always follow the exact structure below:\n\n"
        "Symptoms and Tests:\n"
        "Diagnosis:\n"
        "Treatments :\n"
        "Recommendations:\n"
        "Health Status Assessment:\n"
        "Doctor Recommendation:\n"
        "Disclaimer:\n\n"
        "Rules:\n"
        "- If no Treatments are mentioned and the health is good, write 'None reported'.\n"
        "- Doctor Recommendation must always be written by the AI agent based on the health status.\n"
        "- Always end with a strong disclaimer that this summary may contain errors and patients must consult a doctor for confirmation."
    ),
    expected_output=(
        "A structured summary with the following sections exactly:\n"
        "Symptoms and Tests:\n"
        "Diagnosis:\n"
        "Treatments (if not in good health):\n"
        "Recommendations:\n"
        "Health Status Assessment:\n"
        "Doctor Recommendation:\n"
        "Disclaimer:\n"
    ),
    agent=summarizer_agent,
    tools=[]
)


# Create a Crew
crew = Crew(
    agents=[summarizer_agent],
    tasks=[summarize_task],
    verbose=True
)


if __name__ == "__main__":
    report_file_path = "D:\Hospital-AI-Support\Ca.pdf" 
    pdf_text = read_pdf(report_file_path)
    
    if "Error" in pdf_text:
        print(pdf_text) 
    else:
        try:
            result = crew.kickoff(inputs={"pdf_text": pdf_text})
            print(result)
        except Exception as e:
            print(f"Error running crew: {str(e)}")