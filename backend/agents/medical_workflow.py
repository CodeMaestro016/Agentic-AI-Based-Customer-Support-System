import os
import json
from dotenv import load_dotenv
from Query_Classifier import QueryClassifierAgent
from solution_agent import SolutionAgent
from followup_agent import FollowUpAgent
from rag_agent import answer_query
from Doc_Summerize import read_pdf, crew as doc_crew

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

class MedicalWorkflow:
    def __init__(self):
        self.query_classifier = QueryClassifierAgent()
        self.solution_agent = SolutionAgent()
        self.followup_agent = FollowUpAgent()
        self.chat_history = []
    
    def process_query(self, user_input):
        
        print(f"\n=== Processing: {user_input} ===")
        
        if user_input.startswith("doc:"):
            return self._handle_document_query(user_input)
        
        self.chat_history.append({"role": "user", "content": user_input})
        
        print("Step 1: Query Classification...")
        classification = self.query_classifier.classify_query(user_input, self.chat_history)
        print(f"Classification: {json.dumps(classification, indent=2)}")
        
        rag_context = None
        if classification.get("required_resources", {}).get("rag_needed", False):
            print("\nStep 2a: Retrieving knowledge base information...")
            try:
                explicitly_asking_for_info = any(word in user_input.lower() for word in [
                    'address', 'location', 'contact', 'phone', 'number', 'where',
                    'doctor', 'specialist', 'appointment', 'schedule', 'book', 'available'
                ])
                
                if explicitly_asking_for_info:
                    if any(word in user_input.lower() for word in ['address', 'location', 'contact', 'phone', 'number', 'where']):
                        rag_query = f"MediConnect medical center address location contact phone number {user_input}"
                    elif any(word in user_input.lower() for word in ['doctor', 'specialist', 'appointment', 'schedule', 'book', 'available']):
                        rag_query = f"doctors available specialists appointments {user_input}"
                
                rag_result = answer_query(rag_query)
                rag_context = rag_result["answer"]
                print(f"RAG Context: {rag_context}")
                
                if not rag_context or rag_context.lower().strip() in [
                    "i don't know", "i'm not sure", "no information available",
                    "i cannot find", "i don't have information"
                ] or "don't know" in rag_context.lower():
                    if explicitly_asking_for_info:
                        if any(word in user_input.lower() for word in ['address', 'location', 'contact', 'phone', 'where']):
                            rag_context = "MediConnect Medical Center is located at 123 Medical Plaza, Colombo 07. Contact: +94 11 234 5678. Reception hours: 8 AM - 8 PM daily."
                        elif any(word in user_input.lower() for word in ['doctor', 'specialist', 'appointment', 'schedule', 'book', 'available']):
                            rag_context = "Available doctors today: Dr. Silva (Cardiologist) at 2 PM and 4 PM, Dr. Perera (General Physician) at 10 AM and 3 PM, Dr. Fernando (Internal Medicine) at 1 PM and 5 PM. Walk-ins accepted until 6 PM."
                        print("Knowledge base: Using fallback MediConnect information")
                    else:
                        rag_context = "No specific information found in knowledge base"
                        print("Knowledge base: No fallback needed for symptom query")
                else:
                    print("Knowledge base: Found relevant information")
                    
            except Exception as e:
                print(f"Knowledge base error: {e}")
                rag_context = "Knowledge base system unavailable"
        
        print("\nStep 4: Generating Unified Response...")
        
        response_context = {
            "classification": classification,
            "patient_query": user_input,
            "chat_history": self.chat_history,
            "rag_context": rag_context,
            "conversation_stage": self._determine_conversation_stage()
        }
        
        unified_response = self.solution_agent.generate_unified_response(**response_context)
        print(f"Unified Response: {unified_response}")
        
        self.chat_history.append({"role": "assistant", "content": unified_response})
        
        return {
            "classification": classification,
            "rag_context": rag_context,
            "final_response": unified_response
        }
    
    def _handle_document_query(self, user_input):
        doc_text = user_input.replace("doc:", "").strip()
        
        print("Step 1: Document Summarization...")
        
        if doc_text.endswith('.pdf'):
            pdf_content = read_pdf(doc_text)
            if "Error" in pdf_content:
                print(f"PDF Error: {pdf_content}")
                return {"error": pdf_content}
            doc_input = pdf_content
        else:
            doc_input = doc_text
        
        try:
            doc_result = doc_crew.kickoff(inputs={"pdf_text": doc_input})
            task_result = doc_result.tasks_output[0]
            doc_summary = getattr(task_result, "content", getattr(task_result, "raw", str(task_result)))
            print(f"Document Summary: {doc_summary}")
        except Exception as e:
            print(f"Doc Summarization Error: {e}")
            doc_summary = f"Document summarization failed: {e}"
        
        print("\nStep 2: Generating Solution from Document...")
        classification = {
            "intent": "document_request",
            "urgency": "low",
            "required_resources": {"summarization_needed": True},
            "risk_level": "low"
        }
        
        solution = self.solution_agent.generate_solution(
            classification=classification,
            patient_query=f"Please provide guidance based on this document summary: {doc_summary}",
            chat_history=self.chat_history
        )
        print(f"Solution: {solution}")
        
        print("\nStep 3: Generating Follow-up...")
        followup = self.followup_agent.generate_followup(
            solution=solution,
            original_query=user_input,
            classification=classification,
            chat_history=self.chat_history
        )
        print(f"Follow-up: {followup}")
        
        self.chat_history.append({"role": "user", "content": user_input})
        self.chat_history.append({"role": "assistant", "content": f"{solution}\n\n{followup}"})
        
        return {
            "classification": classification,
            "document_summary": doc_summary,
            "solution": solution,
            "followup": followup,
            "final_response": f"{solution}\n\n{followup}"
        }
    
    def _determine_conversation_stage(self):
        if not self.chat_history:
            return "initial"
        
        user_messages = [msg for msg in self.chat_history if msg["role"] == "user"]
        
        if len(user_messages) == 1:
            return "first_response"
        elif len(user_messages) == 2:
            return "follow_up_info"
        elif any("doctor" in msg["content"].lower() for msg in user_messages):
            return "doctor_request"
        else:
            return "ongoing_conversation"
    
    def save_and_exit(self):
        with open("chat_history.json", "w", encoding="utf-8") as f:
            json.dump(self.chat_history, f, indent=2)
        print("👋 Goodbye! Stay safe.")

def main():
    workflow = MedicalWorkflow()
    
    print("Medical AI Workflow System")
    print("Supported Flows:")
    print("1. Simple: Query_Classifier → Solution_Agent → Follow-up_Agent")
    print("2. With RAG: Query_Classifier → RAG_Agent → Solution_Agent → Follow-up_Agent")
    print("3. Document: doc:[text/file] → Doc_Summarize → Solution_Agent → Follow-up_Agent")
    print("\n👉 Enter medical queries to test the complete workflow")
    print("👉 For documents, prefix with 'doc:'")
    print("👉 Type 'exit' to quit.\n")
    
    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            workflow.save_and_exit()
            break
        
        result = workflow.process_query(user_input)
        
        if "error" in result:
            print(f"Error: {result['error']}")
            continue
            
        print("\n" + "="*60)
        print("FINAL RESPONSE TO USER:")
        print(result["final_response"])
        print("="*60 + "\n")

if __name__ == "__main__":
    main()