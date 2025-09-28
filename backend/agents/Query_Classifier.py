import os
import json
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI

# Setup
load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)  # Lower temperature for consistent classification



class QueryClassifierAgent:
    """Classifies user queries and determines required resources"""
    def __init__(self):
        # Query classification agent - returns structured JSON
        self.agent = Agent(
            role="Medical Query Classification Specialist",
            goal=(
                "Classify medical queries and determine the appropriate workflow path. "
                "Analyze user intent, urgency level, and required resources to handle the query effectively."
            ),
            backstory=(
                "You are an AI specialist that analyzes medical queries to determine the best "
                "processing workflow. You classify queries by intent, urgency, and resource needs "
                "to ensure patients receive appropriate assistance."
            ),
            llm=llm,
            verbose=True,
            memory=True,
            allow_delegation=False,
        )

        # Classification task - returns structured JSON
        self.task = Task(
            description=(
                "Analyze the patient query: {patient_query}\n"
                "Chat history context: {chat_history}\n\n"
                "Classify this query and return a JSON object with the following structure:\n"
                "{\n"
                "  \"intent\": \"symptom_inquiry\" | \"appointment_request\" | \"doctor_inquiry\" | \"center_information\" | \"document_request\" | \"emergency\" | \"greeting\" | \"invalid_query\",\n"
                "  \"urgency\": \"low\" | \"medium\" | \"high\" | \"emergency\",\n"
                "  \"symptoms\": [\"list of mentioned symptoms\"],\n"
                "  \"required_resources\": {\n"
                "    \"rag_needed\": true/false,\n"
                "    \"summarization_needed\": true/false,\n"
                "    \"direct_llm\": true/false\n"
                "  },\n"
                "  \"risk_level\": \"low\" | \"medium\" | \"high\" | \"emergency\",\n"
                "  \"next_agent\": \"rag_agent\" | \"solution_agent\" | \"doc_summarizer\",\n"
                "  \"reasoning\": \"Brief explanation of classification\"\n"
                "}\n\n"
                "Classification Rules:\n"
                "- symptom_inquiry: Patient describes symptoms or health concerns\n"
                "- appointment_request: Patient wants to book/schedule appointment\n"
                "- doctor_inquiry: Patient asks about available doctors or specialists (including psychologists, psychiatrists, mental health specialists)\n"
                "- center_information: Patient asks for address, contact, hours\n"
                "- document_request: Patient uploads/mentions medical documents\n"
                "- emergency: Life-threatening symptoms (chest pain, difficulty breathing, severe bleeding)\n"
                "- greeting: Polite greetings like 'hi', 'hello', 'good morning', 'how are you'\n"
                "- invalid_query: Meaningless text, random characters, gibberish (like 'hjhsds', 'xyzabc'), or completely unrelated content\n\n"
                "RAG needed for: doctor inquiries, appointment requests, center information\n"
                "Direct LLM for: symptom inquiries, general health questions, greetings\n"
                "Summarization needed for: document uploads, PDF processing\n\n"
                "IMPORTANT: Distinguish between greetings (friendly words) and gibberish (random letters)\n"
                "Greeting examples: 'hi', 'hello', 'good morning', 'how are you', 'hey there'\n"
                "Invalid examples: 'hjhsds', 'aaaa', 'xyzabc', 'qwerty', random letter combinations\n"
                "Doctor inquiry keywords: doctor, specialist, psychologist, psychiatrist, therapist, counselor, mental health, psychology, psychiatry\n"
                "Emergency indicators: chest pain, can't breathe, severe bleeding, unconsciousness, stroke symptoms"
            ),
            expected_output=(
                "Valid JSON object with intent, urgency, symptoms, required_resources, risk_level, next_agent, and reasoning fields."
            ),
            agent=self.agent
        )

        # Crew setup
        self.crew = Crew(
            agents=[self.agent],
            tasks=[self.task],
            verbose=True,
        )
    
    def classify_query(self, patient_query, chat_history=None):
        """Classify a patient query and return structured JSON"""
        if chat_history is None:
            chat_history = []
            
        result = self.crew.kickoff(inputs={
            "patient_query": patient_query,
            "chat_history": chat_history
        })
        
        # Extract the agent's response
        task_result = result.tasks_output[0]
        response = getattr(task_result, "content", getattr(task_result, "raw", str(task_result)))
        
        # Parse JSON response
        try:
            classification = json.loads(response.strip())
            return classification
        except json.JSONDecodeError:
            # Fallback classification if JSON parsing fails
            print(f"Warning: Failed to parse classification JSON: {response}")
            return {
                "intent": "symptom_inquiry",
                "urgency": "medium",
                "symptoms": [],
                "required_resources": {
                    "rag_needed": False,
                    "summarization_needed": False,
                    "direct_llm": True
                },
                "risk_level": "medium",
                "next_agent": "solution_agent",
                "reasoning": "Fallback classification due to parsing error"
            }

if __name__ == "__main__":
    # Test the Query Classifier
    classifier = QueryClassifierAgent()
    
    print("Query Classifier Agent Test")
    print("👉 Enter medical queries to test classification")
    print("👉 Type 'exit' to quit.\n")
    
    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            print("👋 Goodbye!")
            break
        
        classification = classifier.classify_query(user_input)
        print("Classification:")
        print(json.dumps(classification, indent=2))
        print()
