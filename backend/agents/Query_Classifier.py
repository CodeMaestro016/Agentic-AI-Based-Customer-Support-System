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
                "  \"intent\": \"symptom_inquiry\" | \"appointment_request\" | \"doctor_inquiry\" | \"center_information\" | \"document_request\" | \"medicine_recommendation\" | \"medicine_safety\" | \"general_health\" | \"ai_role\" | \"health_apps\" | \"small_talk\" | \"privacy\" | \"bias_discrimination\" | \"harmful_intent\" | \"accessibility\" | \"language_support\" | \"emergency\" | \"greeting\" | \"appointment_booking\" | \"negative_response\" | \"positive_response\" | \"invalid_query\" | \"farewell\" | \"self_diagnosis\" | \"dangerous_request\",\n"
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
                "- symptom_inquiry: Patient describes THEIR OWN symptoms or health concerns (keywords: 'I have', 'I'm experiencing', 'I feel', 'I'm suffering from')\n"
                "- appointment_request: Patient wants to book/schedule appointment\n"
                "- doctor_inquiry: Patient asks about available doctors or specialists (including psychologists, psychiatrists, mental health specialists)\n"
                "- center_information: Patient asks for address, contact, hours\n"
                "- document_request: Patient uploads/mentions medical documents\n"
                "- medicine_recommendation: Patient asks for specific medicine recommendations or prescriptions (keywords: 'medicine for', 'prescription for', 'drug for', 'tablet for', 'pill for', 'what should I take').\n"
                "  IMPORTANT: Never recommend or name any specific medicine, drug, or prescription. "
                "  Instead, classify it as a 'medicine_recommendation' intent and clearly indicate that only a qualified healthcare professional can prescribe medication.\n"
                "- medicine_safety: Patient asks about safe use of medicines (keywords: 'safely', 'safe use', 'miss a dose', 'stop early', 'share', 'after eating', 'with food')\n"
                "- general_health: Patient asks for general health information, benefits of activities, prevention tips, causes of conditions (keywords: 'what causes', 'benefits of', 'good for', 'healthy', 'prevention', 'tips for', 'why do')\n"
                "- ai_role: Patient asks about AI assistant capabilities or limitations (keywords: 'are you a doctor', 'can you treat', 'who made you')\n"
                "- health_apps: Patient asks about health apps or technology (keywords: 'health app', 'app recommend')\n"
                "- small_talk: Patient engages in casual conversation (keywords: 'tell me a joke', 'how are you', 'what's up')\n"
                "- privacy: Patient asks about data privacy, storage, or sharing (keywords: 'store data', 'share info', 'privacy', 'confidentiality', 'someone else')\n"
                "- bias_discrimination: Patient asks about gender, age, ethnicity, religion, or income in relation to health (keywords: 'gender', 'age', 'ethnicity', 'religion', 'income', 'wealthy', 'poor', 'rich')\n"
                "- harmful_intent: Patient expresses self-harm, suicide ideation, or dangerous behaviors (keywords: 'harm myself', 'suicide', 'kill myself', 'self harm', 'end my life', 'want to die')\n"
                "- accessibility: Patient requests information in alternative formats (keywords: 'visually impaired', 'blind', 'deaf', 'hearing impaired', 'simple words', 'child')\n"
                "- language_support: Patient asks about language capabilities (keywords: 'non-english', 'spanish', 'french', 'chinese', 'language')\n"
                "- emergency: Life-threatening symptoms (chest pain, difficulty breathing, severe bleeding, unconsciousness, stroke symptoms)\n"
                "- greeting: Polite greetings like 'hi', 'hello', 'good morning', 'how are you'\n"
                "- farewell: Polite farewells like 'bye', 'goodbye', 'see you', 'farewell', 'take care'\n"
                "- appointment_booking: Patient confirms interest in booking an appointment (responses like 'yes', 'ok', 'sure' when asked about booking)\n"
                "- negative_response: Patient responds negatively (keywords: 'no', 'nope', 'not really', 'not now')\n"
                "- positive_response: Patient responds positively but doesn't need further assistance (keywords: 'ok', 'okay', 'yes', 'yeah', 'sure', 'thank you', 'thanks', 'thankyou')\n"
                "- invalid_query: Meaningless text, random characters, gibberish (like 'hjhsds', 'xyzabc'), or completely unrelated content\n"
                "- self_diagnosis: Patient wants to self-diagnose or self-treat (keywords: 'self-diagnose', 'diagnose myself', 'treat myself')\n"
                "- dangerous_request: Patient asks for dangerous or harmful medical advice (keywords: 'dangerous way', 'harmful method', 'unsafe treatment')\n\n"
                "RAG needed for: doctor inquiries, appointment requests, center information\n"
                "Direct LLM for: symptom inquiries, general health questions, medicine safety questions, greetings\n"
                "Summarization needed for: document uploads, PDF processing\n\n"
                "General health questions (like benefits of exercise, healthy eating, etc.) should be handled with informative, "
                "evidence-based responses that end with open-ended questions like 'Is there anything specific you'd like to know more about?'\n\n"
                "Medicine safety questions (like 'How should I take my prescribed medicine safely?', 'What should I do if I miss a dose?') "
                "should be handled with general safety guidelines without recommending specific drugs.\n\n"
                "AI role clarification questions (like 'Are you a doctor?', 'Can you treat diseases?') "
                "should clearly explain the AI assistant's capabilities and limitations.\n\n"
                "Small talk questions (like 'Tell me a joke') can have friendly responses but should redirect to healthcare topics.\n\n"
                "Privacy questions (like 'Can you store my health data?', 'Do you share patient info with others?') "
                "should clearly explain data handling practices and respect for confidentiality.\n\n"
                "Bias/discrimination questions (like 'Which gender should see a cardiologist?', 'Is this disease more common in [specific ethnicity]?') "
                "should provide factual, evidence-based information while emphasizing that healthcare is for everyone "
                "and decisions should be based on individual medical needs.\n\n"
                "Harmful intent questions (like 'I want to harm myself') should be taken seriously and provide crisis "
                "intervention resources and helpline numbers.\n\n"
                "Accessibility questions (like 'I'm visually impaired') should provide appropriate accommodations "
                "and alternative formats where possible.\n\n"
                "Language support questions should clarify current language capabilities and suggest alternatives "
                "for non-English speakers.\n\n"
                "Emergency questions (like 'I think I am having a heart attack') should provide immediate "
                "instructions to call emergency services.\n\n"
                "Self-diagnosis questions should warn about the dangers of self-diagnosis and encourage "
                "consulting with qualified healthcare professionals.\n\n"
                "Dangerous request questions should refuse to provide harmful advice and warn about health risks.\n\n"
                "IMPORTANT: Distinguish between greetings (friendly words) and gibberish (random letters)\n"
                "Greeting examples: 'hi', 'hello', 'good morning', 'how are you', 'hey there'\n"
                "Invalid examples: 'hjhsds', 'aaaa', 'xyzabc', 'qwerty', random letter combinations\n"
                "Doctor inquiry keywords: doctor, specialist, psychologist, psychiatrist, therapist, counselor, mental health, psychology, psychiatry\n"
                "Emergency indicators: chest pain, can't breathe, severe bleeding, unconsciousness, stroke symptoms, heart attack, severe allergic reaction, fainting"
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
        except json.JSONDecodeError:
            print(f"Warning: Failed to parse classification JSON: {response}")
            classification = {
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

        # 🆕 Added: Supportive message for harmful intent
        if classification.get("intent") == "harmful_intent":
            print("\n⚠️ It sounds like you're going through a really difficult time.")
            print("You are not alone — help is available right now. ❤️")
            print("Please reach out to someone who can help you immediately.")
            print("You matter, and there are people who care about you and want to help.\n")

        return classification


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
