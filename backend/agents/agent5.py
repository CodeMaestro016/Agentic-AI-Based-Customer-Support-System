import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
import spacy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
import re

# Load environment variables
load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
if not os.environ['OPENAI_API_KEY']:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")

# Load Spacy medical model
try:
    nlp = spacy.load("en_deid_ner")  # Medical NER model
except Exception as e:
    print(f"Error loading Spacy model: {str(e)}. Falling back to en_core_web_sm.")
    nlp = spacy.load("en_core_web_sm")

# Define the LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

# Custom Function: PDF Text Extraction with NLP Preprocessing
def process_pdf(file_path: str) -> dict:
    if not os.path.exists(file_path):
        return {"error": f"File {file_path} does not exist."}
    
    try:
        # Extract text from PDF
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        full_text = "\n".join([doc.page_content for doc in documents])
        
        # NLP Preprocessing with Spacy
        doc = nlp(full_text)
        
        # Extract entities (e.g., patient details, diagnosis, treatments)
        entities = {
            "patient_details": [],
            "symptoms": [],
            "diagnosis": [],
            "treatments": [],
            "recommendations": []
        }
        for ent in doc.ents:
            if ent.label_ in ["PERSON", "AGE", "GENDER"]:  # Adjust based on model labels
                entities["patient_details"].append(ent.text)
            elif ent.label_ in ["SYMPTOM", "CONDITION"]:
                entities["symptoms"].append(ent.text)
            elif ent.label_ in ["DIAGNOSIS", "DISEASE"]:
                entities["diagnosis"].append(ent.text)
            elif ent.label_ in ["TREATMENT", "MEDICATION"]:
                entities["treatments"].append(ent.text)
            elif ent.label_ in ["RECOMMENDATION"]:
                entities["recommendations"].append(ent.text)
        
        # Extractive Summarization with TextRank
        parser = PlaintextParser.from_string(full_text, Tokenizer("english"))
        summarizer = TextRankSummarizer()
        summary_sentences = summarizer(parser.document, 3)  # Top 3 sentences
        extractive_summary = " ".join([str(sentence) for sentence in summary_sentences])
        
        # Health Status Heuristics
        health_status = "good"
        doctor_recommendation = ""
        concerning_terms = ["critical", "urgent", "abnormal", "severe", "emergency"]
        if any(term in full_text.lower() for term in concerning_terms):
            health_status = "concerning"
            doctor_recommendation = "The report indicates potential issues. Please consult a doctor immediately for professional evaluation."
        elif "normal" in full_text.lower() or "stable" in full_text.lower():
            health_status = "good"
            doctor_recommendation = "The report suggests stable health, but consult a doctor for confirmation."
        else:
            health_status = "unclear"
            doctor_recommendation = "The report's health status is unclear. Consult a doctor for a detailed assessment."
        
        return {
            "full_text": full_text,
            "entities": entities,
            "extractive_summary": extractive_summary,
            "health_status": health_status,
            "doctor_recommendation": doctor_recommendation
        }
    except Exception as e:
        return {"error": f"Error processing PDF: {str(e)}"}

# Define the Summarizer Agent
summarizer_agent = Agent(
    role="Medical Report Summarizer Agent",
    goal=(
        "Summarize medical reports by extracting key details (patient info, symptoms, diagnosis, treatments, recommendations). "
        "Assess the patient's health status (e.g., good, concerning) and recommend consulting a doctor if issues are detected. "
        "Always emphasize that this is not professional medical advice."
    ),
    backstory=(
        "You are an AI expert in analyzing medical documents for customer support in healthcare systems. "
        "You extract key information, assess overall health based on report content, and provide empathetic, concise summaries. "
        "Always include a disclaimer that AI summaries may have errors and professional medical review is essential."
    ),
    llm=llm,
    verbose=True,
    memory=True,
    allow_delegation=False,
    tools=[]
)

# Define the Summarization Task
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

# Example Usage
if __name__ == "__main__":
    report_file_path = "D:\\MedicalSummarizer\\medi.pdf"
    processed_data = process_pdf(report_file_path)
    
    if "error" in processed_data:
        print(processed_data["error"])
    else:
        try:
            result = crew.kickoff(inputs={
                "pdf_text": processed_data["full_text"],
                "entities": str(processed_data["entities"]),  # Convert to string for LLM
                "extractive_summary": processed_data["extractive_summary"],
                "health_status": processed_data["health_status"],
                "doctor_recommendation": processed_data["doctor_recommendation"]
            })
            print(result)
        except Exception as e:
            print(f"Error running crew: {str(e)}")