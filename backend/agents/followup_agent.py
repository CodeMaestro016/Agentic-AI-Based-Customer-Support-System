# Follow-up Agent - Handles conversation continuity and natural follow-up questions
# Provides context-aware questions without repetition

import os
import json
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI

# Setup environment
load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

class FollowUpAgent:
    """Manages conversation continuity and follow-up questions"""
    def __init__(self):
        # Follow-up agent for medical conversation continuity
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
        
        # Task for context-aware follow-up questions
        self.task = Task(
            description=(
                "Based on the solution provided: {solution}\n"
                "For the original query: {original_query}\n"
                "And classification: {classification}\n"
                "Chat history: {chat_history}\n\n"
                "You are a conversational medical assistant. Generate follow-up questions that:\n\n"
                "1. DON'T repeat questions already asked in chat history\n"
                "2. Are relevant to the current conversation context\n"
                "3. Help gather missing information naturally\n"
                "4. AVOID generic questions like 'Is there anything else I can help you with?'\n"
                "5. AVOID repetitive questions like 'Would you like to book an appointment?' after it's already been asked\n\n"
                "Logic for follow-ups:\n"
                "- NEW symptom mentioned: Ask duration and severity\n"
                "- Duration/location provided: Ask about other aspects or next steps\n"
                "- Doctor request made: Ask about preferences (time, specialist type)\n"
                "- RAG info provided: Ask if they need more details\n"
                "- General health info provided: Ask specific clarifying questions\n"
                "- Medicine inquiry response: Ask if they'd like to book an appointment with a doctor\n"
                "- Accessibility request: Offer additional help or alternative explanations\n"
                "- Language support request: Suggest contacting the medical center for multilingual support\n"
                "- Bias/discrimination response: Reinforce commitment to equitable care\n"
                "- Privacy response: Assure continued confidentiality\n"
                "- AI role clarification: Ask about specific health concerns they have\n"
                "- Greeting response: Ask how you can help with their healthcare needs\n"
                "- Thank you response: Acknowledge gratitude and offer continued assistance\n\n"
                "IMPORTANT: Avoid asking 'Would you like me to help you book an appointment?' multiple times\n"
                "Check chat history to see if this question was already asked\n"
                "IMPORTANT: Generate ONLY ONE follow-up question, not multiple questions\n"
                "IMPORTANT: AVOID generic catch-all questions like 'Is there anything else I can help you with?'\n"
                "IMPORTANT: AVOID redundant questions that repeat what was just said\n"
                "IMPORTANT: Keep questions SIMPLE and DIRECT - avoid complex multi-part questions\n"
                "IMPORTANT: Ask only ONE specific question at a time\n"
                "IMPORTANT: Keep questions EXTREMELY BRIEF and DIRECT\n\n"
                "Special handling:\n"
                "- For harmful_intent, emergency, or dangerous_request: Do NOT generate follow-ups, just end the conversation\n"
                "- For self_diagnosis warnings: Encourage professional consultation\n"
                "- For greeting or thank you responses: Provide appropriate acknowledgments\n"
                "- For ai_role queries: Ask about specific health concerns they have\n\n"
                "Examples of GOOD simple questions:\n"
                "- 'How long have you had this symptom?'\n"
                "- 'Would you like to see a doctor about this?'\n"
                "- 'When would you prefer to schedule an appointment?'\n"
                "- 'Do you have any other concerns?'\n\n"
                "Examples of BAD complex questions:\n"
                "- 'Since you want to see a doctor, do you have a preference for which type of specialist you would like to see, or would you prefer a general physician?' (Too complex)\n"
                "- 'Is there anything specific you would like to know more about regarding your symptoms? Would you like to schedule a consultation with a doctor to discuss your headache and explore treatment options?' (Multiple questions)\n\n"
                "Keep it natural and conversational - ONLY ONE simple, direct question in 10-15 words maximum."
            ),
            expected_output=(
                "ONE extremely simple, direct follow-up question (10-15 words max) that builds on the conversation without repetition."
            ),
            agent=self.agent
        )
        
        # Crew setup for follow-up agent
        self.crew = Crew(
            agents=[self.agent],
            tasks=[self.task],
            verbose=True,
        )
    
    def generate_followup(self, solution, original_query, classification, chat_history=None):
        """Generate follow-up questions after solution"""
        if chat_history is None:
            chat_history = []
            
        result = self.crew.kickoff(inputs={
            "solution": solution,
            "original_query": original_query,
            "classification": classification,
            "chat_history": chat_history
        })
        
        # Extract the agent's response
        task_result = result.tasks_output[0]
        response = getattr(task_result, "content", getattr(task_result, "raw", str(task_result)))
        
        return response
    
    def save_chat_history(self, chat_history):
        """Save chat history to file"""
        with open("chat_history.json", "w", encoding="utf-8") as f:
            json.dump(chat_history, f, indent=2)

if __name__ == "__main__":
    # Test the Follow-up Agent
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