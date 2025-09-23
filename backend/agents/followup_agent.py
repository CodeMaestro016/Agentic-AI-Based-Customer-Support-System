import os
import json
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

class FollowUpAgent:
    def __init__(self):
        self.agent = Agent(
            role="Medical Follow-up Specialist",
            goal=(
                "Ask relevant follow-up questions after a medical solution is provided. "
                "Gather additional information to better understand the patient's condition "
                "and provide more personalized guidance."
            ),
            backstory=(
                "You are an AI assistant that asks clarifying questions after providing "
                "initial medical guidance. You help gather more details about symptoms "
                "to offer better support while maintaining empathy and professionalism."
            ),
            llm=llm,
            verbose=True,
            memory=True,
            allow_delegation=False,
        )
        
        self.task = Task(
            description=(
                "Based on the solution provided: {solution}\n"
                "For the original query: {original_query}\n"
                "And classification: {classification}\n"
                "Chat history: {chat_history}\n\n"
                "You are a conversational medical assistant. Generate follow-up questions that:\n\n"
                "1. DON'T repeat questions already asked in chat history\n"
                "2. Are relevant to the current conversation context\n"
                "3. Help gather missing information naturally\n\n"
                "Logic for follow-ups:\n"
                "- NEW symptom mentioned: Ask duration and severity\n"
                "- Duration/location provided: Ask about other aspects or next steps\n"
                "- Doctor request made: Ask about preferences (time, specialist type)\n"
                "- RAG info provided: Ask if they need more details or want to book\n\n"
                "Examples:\n"
                "- First symptom: 'How long have you been experiencing this? Can you rate the pain 1-10?'\n"
                "- After details: 'Would you prefer a morning or afternoon appointment?'\n"
                "- After doctor info: 'Would you like me to help you book an appointment with Dr. Smith?'\n\n"
                "Keep it natural and conversational - max 1-2 relevant questions."
            ),
            expected_output=(
                "1-2 natural follow-up questions that build on the conversation without repetition."
            ),
            agent=self.agent
        )
        
        self.crew = Crew(
            agents=[self.agent],
            tasks=[self.task],
            verbose=True,
        )
    
    def generate_followup(self, solution, original_query, classification, chat_history=None):
        if chat_history is None:
            chat_history = []
            
        result = self.crew.kickoff(inputs={
            "solution": solution,
            "original_query": original_query,
            "classification": classification,
            "chat_history": chat_history
        })
        
        task_result = result.tasks_output[0]
        response = getattr(task_result, "content", getattr(task_result, "raw", str(task_result)))
        
        return response
    
    def save_chat_history(self, chat_history):
        with open("chat_history.json", "w", encoding="utf-8") as f:
            json.dump(chat_history, f, indent=2)

if __name__ == "__main__":
    followup_agent = FollowUpAgent()
    
    test_history = [
        {"role": "user", "content": "I have headaches for 3 days"},
        {"role": "agent", "content": "Can you describe the severity and any other symptoms?"}
    ]
    
    test_response = followup_agent.generate_followup(
        chat_history=test_history,
        latest_response="Based on your symptoms, I recommend rest and monitoring."
    )
    
    print("Follow-up Agent Response:")
    print(test_response)