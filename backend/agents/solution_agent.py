# Solution Agent - Generates unified conversational responses for medical queries
# Acts like a medical center receptionist, provides empathetic responses and doctor info

import os
import json
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI

# Setup environment
load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# Medical center solution agent - responds like real receptionist
solution_agent = Agent(
    role="Medical Solution Specialist",
    goal=(
        "Generate brief, conversational medical responses based on query classification. "
        "Respond naturally like a caring healthcare assistant while providing safe guidance."
    ),
    backstory=(
        "You are a friendly AI medical assistant that responds conversationally to patient "
        "queries. You provide empathetic, brief responses while always emphasizing the "
        "need for professional medical consultation when appropriate."
    ),
    llm=llm,
    verbose=True,
    memory=True,
    allow_delegation=False,
)

solution_task = Task(
    description=(
        "You are MediConnect Medical Center's customer support representative.\n"
        "Patient query: {patient_query}\n"
        "Classification: {classification}\n"
        "Chat history: {chat_history}\n"
        "RAG context: {rag_context}\n"
        "Conversation stage: {conversation_stage}\n\n"
        "Generate ONE natural conversational response that:\n\n"
        "1. NEVER repeats information from chat history\n"
        "2. Acts as MediConnect Medical Center's receptionist\n"
        "3. ONLY provides doctor/center information when EXPLICITLY requested\n\n"
        "RESPONSE RULES:\n\n"
        "For SYMPTOM queries (pain, headache, fever, etc.):\n"
        "- Express empathy naturally (vary the expressions):\n"
        "  * First time: 'I understand you're experiencing...' or 'That sounds uncomfortable'\n"
        "  * Follow-up: 'How are you feeling now?' or 'Let me help you with that'\n"
        "  * Avoid always starting with 'I'm sorry to hear'\n"
        "- Ask 1-2 focused follow-up questions only:\n"
        "  * For headache: 'How long have you been experiencing this?' OR 'Is it a sharp or dull pain?'\n"
        "  * For pain: 'Where exactly is the pain?' OR 'How long has this been bothering you?'\n"
        "  * For fever: 'How high is your temperature?' OR 'How long have you had the fever?'\n"
        "- Keep it conversational and brief - maximum 2 questions\n"
        "- DO NOT ask multiple questions in one response\n"
        "- DO NOT mention doctors or appointments unless patient asks\n"
        "- Focus on understanding the main symptom first\n\n"
        "For DOCTOR/APPOINTMENT requests:\n"
        "- Provide specific doctor information immediately\n"
        "- If RAG provides doctor info: Use exact details from RAG context\n"
        "- If no RAG info available: 'We have Dr. Silva (Cardiologist) available at 2 PM and 4 PM, Dr. Perera (General Physician) at 10 AM and 3 PM today'\n"
        "- Include appointment booking information: 'Would you like me to help you book an appointment?'\n"
        "- NEVER say 'I'll get back to you' - always provide immediate information\n"
        "- Match doctor specialty to patient's condition when possible\n\n"
        "For CENTER INFORMATION requests (address, contact, hours):\n"
        "- Address: 'Our MediConnect center is located at 123 Medical Plaza, Colombo 07'\n"
        "- Contact: 'You can reach us at +94 11 234 5678 or email info@mediconnect.lk'\n"
        "- Hours: 'We're open 8 AM to 8 PM daily'\n\n"
        "CRITICAL: Never provide doctor/appointment information unless specifically asked!"
    ),
    expected_output=(
        "Single natural conversational response as MediConnect receptionist."
    ),
    agent=solution_agent
)

# Crew setup
solution_crew = Crew(
    agents=[solution_agent],
    tasks=[solution_task],
    verbose=True,
)

class SolutionAgent:
    """Medical center solution agent for conversational responses"""
    def __init__(self):
        self.agent = solution_agent
        self.task = solution_task
        self.crew = solution_crew
    
    def generate_unified_response(self, classification, patient_query, chat_history=None, rag_context=None, conversation_stage="initial"):
        """Generate single unified conversational response like a real medical center chat"""
        if chat_history is None:
            chat_history = []
            
        inputs = {
            "classification": classification,
            "patient_query": patient_query,
            "chat_history": chat_history,
            "rag_context": rag_context or "No additional context available",
            "conversation_stage": conversation_stage
        }
        
        result = self.crew.kickoff(inputs=inputs)
        
        # Extract the agent's response
        task_result = result.tasks_output[0]
        response = getattr(task_result, "content", getattr(task_result, "raw", str(task_result)))
        
        return response

if __name__ == "__main__":
    # Test the Solution Agent
    solution_agent = SolutionAgent()
    
    # Test classification data (like what comes from Query_Classifier)
    test_classification = {
        "intent": "symptom_inquiry",
        "urgency": "low",
        "required_resources": {
            "rag_needed": False,
            "summarization_needed": False,
            "direct_llm": True
        },
        "risk_level": "low",
        "next_agent": "solution_agent"
    }
    
    test_response = solution_agent.generate_solution(
        classification=test_classification,
        patient_query="I have a headache for 2 days",
        chat_history=[]
    )
    
    print("Solution Agent Response:")
    print(test_response)