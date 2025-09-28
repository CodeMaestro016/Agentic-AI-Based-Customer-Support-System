# Medical Workflow Orchestrator - Manages complete conversation flow
# Coordinates Query_Classifier → RAG → Solution_Agent for natural chat

import os
import json
from dotenv import load_dotenv
from Query_Classifier import QueryClassifierAgent
from solution_agent import SolutionAgent
from followup_agent import FollowUpAgent
from rag_agent import answer_query
from Doc_Summerize import read_pdf, crew as doc_crew

# Setup environment
load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

class MedicalWorkflow:
    """Orchestrates medical conversation workflow like real chat"""
    def __init__(self):
        self.query_classifier = QueryClassifierAgent()
        self.solution_agent = SolutionAgent()
        self.followup_agent = FollowUpAgent()
        self.chat_history = []
    
    def process_query(self, user_input):
        """Process user query through complete conversational workflow"""
        
        print(f"\n=== Processing: {user_input} ===")
        
        # Handle document summarization requests
        if user_input.startswith("doc:"):
            return self._handle_document_query(user_input)
        
        # Update chat history BEFORE processing to provide context
        self.chat_history.append({"role": "user", "content": user_input})
        
        # Step 1: Query Classification (JSON only)
        print("Step 1: Query Classification...")
        classification = self.query_classifier.classify_query(user_input, self.chat_history)
        print(f"Classification: {json.dumps(classification, indent=2)}")
        
        # Handle greetings
        if classification.get("intent") == "greeting":
            greeting_response = (
                "Hello! I'm your MediConnect medical assistant. How can I help you today? \n\n"
                "I can assist you with:\n"
                "• Health symptoms and concerns\n"
                "• Finding doctors and specialists\n"
                "• Booking appointments\n"
                "• Medical center information (location, hours, contact)\n"
                "• Insurance and billing questions\n"
                "• Analyzing medical documents\n\n"
                "What would you like to know?"
            )
            self.chat_history.append({"role": "assistant", "content": greeting_response})
            return {
                "classification": classification,
                "rag_context": None,
                "final_response": greeting_response
            }
        
        # Handle invalid queries
        if classification.get("intent") == "invalid_query":
            invalid_response = (
                "I didn't understand that. I'm here to help with medical and health-related questions. "
                "Could you please ask me something about your health or our medical center? For example:\n\n"
                "• 'I have a headache for 2 days'\n"
                "• 'I need to see a doctor'\n"
                "• 'What are your center hours?'\n"
                "• 'Do you accept my insurance?'"
            )
            self.chat_history.append({"role": "assistant", "content": invalid_response})
            return {
                "classification": classification,
                "rag_context": None,
                "final_response": invalid_response
            }
        # Handle emergency cases
        if classification.get("urgency") == "emergency" or classification.get("risk_level") == "emergency":
            emergency_response = (
                "🚨 **EMERGENCY DETECTED** 🚨\n\n"
                "This appears to be a medical emergency. Please:\n"
                "• Call emergency services immediately (911/119)\n"
                "• Go to the nearest emergency room\n"
                "• Do not delay seeking immediate medical attention\n\n"
                "Our AI assistant cannot help with emergency situations."
            )
            self.chat_history.append({"role": "assistant", "content": emergency_response})
            return {
                "classification": classification,
                "rag_context": None,
                "final_response": emergency_response
            }
        
        # Check if RAG (knowledge base search) is needed based on classification
        rag_context = None
        if classification.get("required_resources", {}).get("rag_needed", False):
            print("\nStep 2a: Retrieving knowledge base information...")
            try:
                # Enhanced RAG query based on intent
                rag_query = self._enhance_rag_query(user_input, classification)
                print(f"Enhanced RAG Query: {rag_query}")
                rag_result = answer_query(rag_query)
                rag_context = rag_result  # answer_query returns string directly, not dict
                print(f"RAG Context: {rag_context}")
                print(f"RAG Context Length: {len(rag_context) if rag_context else 0}")
                
                # Provide fallback information if RAG fails
                is_empty = self._is_rag_response_empty(rag_context)
                print(f"Is RAG response empty? {is_empty}")
                
                if not rag_context or is_empty:
                    rag_context = self._get_fallback_info(classification)
                    print("Knowledge base: Using fallback information")
                else:
                    print("Knowledge base: Found relevant information - using RAG context")
                    
            except Exception as e:
                print(f"Knowledge base error: {e}")
                rag_context = self._get_fallback_info(classification)
        
        # Generate single conversational response
        print("\nStep 4: Generating Unified Response...")
        
        # Create context for natural response generation
        response_context = {
            "classification": classification,
            "patient_query": user_input,
            "chat_history": self.chat_history,
            "rag_context": rag_context or "No RAG context available",
            "conversation_stage": self._determine_conversation_stage()
        }
        
        print(f"Passing to Solution Agent - RAG Context: {rag_context}")
        
        unified_response = self.solution_agent.generate_unified_response(**response_context)
        print(f"Unified Response: {unified_response}")
        
        # Update chat history
        self.chat_history.append({"role": "assistant", "content": unified_response})
        
        return {
            "classification": classification,
            "rag_context": rag_context,
            "final_response": unified_response
        }
    
    def _handle_document_query(self, user_input):
        """Handle document summarization workflow"""
        doc_text = user_input.replace("doc:", "").strip()
        
        print("Step 1: Document Summarization...")
        
        # Check if it's PDF file or direct text
        if doc_text.endswith('.pdf'):
            # Handle PDF file path
            pdf_content = read_pdf(doc_text)
            if "Error" in pdf_content:
                print(f"PDF Error: {pdf_content}")
                return {"error": pdf_content}
            doc_input = pdf_content
        else:
            # Handle direct text input
            doc_input = doc_text
        
        # Use document summarization agent
        try:
            doc_result = doc_crew.kickoff(inputs={"pdf_text": doc_input})
            task_result = doc_result.tasks_output[0]
            doc_summary = getattr(task_result, "content", getattr(task_result, "raw", str(task_result)))
            print(f"Document Summary: {doc_summary}")
        except Exception as e:
            print(f"Doc Summarization Error: {e}")
            doc_summary = f"Document summarization failed: {e}"
        
        # Step 2: Generate Solution based on document summary
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
        
        # Step 3: Follow-up Questions
        print("\nStep 3: Generating Follow-up...")
        followup = self.followup_agent.generate_followup(
            solution=solution,
            original_query=user_input,
            classification=classification,
            chat_history=self.chat_history
        )
        print(f"Follow-up: {followup}")
        
        # Update chat history
        self.chat_history.append({"role": "user", "content": user_input})
        self.chat_history.append({"role": "assistant", "content": f"{solution}\n\n{followup}"})
        
        return {
            "classification": classification,
            "document_summary": doc_summary,
            "solution": solution,
            "followup": followup,
            "final_response": f"{solution}\n\n{followup}"
        }
    
    def _enhance_rag_query(self, user_input, classification):
        """Enhance RAG query based on classification intent"""
        intent = classification.get("intent", "")
        
        if intent == "center_information":
            return f"MediConnect medical center address location contact phone number hours {user_input}"
        elif intent == "doctor_inquiry":
            # Enhanced query for different types of doctors/specialists
            base_query = f"doctors available specialists medical staff {user_input}"
            
            # Add specific keywords for different specialties
            if any(keyword in user_input.lower() for keyword in [
                'psychological', 'psychologist', 'psychiatrist', 'mental health', 
                'therapy', 'therapist', 'counselor', 'psychology', 'psychiatry',
                'depression', 'anxiety', 'stress', 'counseling'
            ]):
                base_query = f"psychologist psychiatrist mental health therapist counselor psychology psychiatry doctors specialists available schedule contact details {user_input}"
            elif any(keyword in user_input.lower() for keyword in [
                'neurologist', 'neurology', 'brain', 'nerve', 'nervous system',
                'headache', 'migraine', 'epilepsy', 'stroke', 'neurological'
            ]):
                base_query = f"neurologist neurology brain nerve nervous system specialists doctors available schedule contact details {user_input}"
            elif any(keyword in user_input.lower() for keyword in [
                'cardiologist', 'cardiology', 'heart', 'cardiac'
            ]):
                base_query = f"cardiologist cardiology heart cardiac specialists doctors available schedule contact details {user_input}"
            elif any(keyword in user_input.lower() for keyword in [
                'doctor', 'physician', 'specialist', 'medical staff'
            ]):
                base_query = f"doctors physicians specialists medical staff available schedule contact details consultation appointments {user_input}"
            
            return base_query
        elif intent == "appointment_request":
            return f"appointment booking schedule doctors available times slots consultation {user_input}"
        else:
            return user_input
    
    def _is_rag_response_empty(self, rag_context):
        """Check if RAG response indicates no information found"""
        if not rag_context or rag_context.strip() == "":
            return True
        
        # More precise empty indicators
        empty_indicators = [
            "i don't know", "i'm not sure", "no information available",
            "i cannot find", "i don't have information", "don't know",
            "no relevant information found", "not found in", "no doctors found",
            "no specialists found", "information is not available"
        ]
        
        rag_lower = rag_context.lower().strip()
        
        # Check if the response is just an empty indicator
        for indicator in empty_indicators:
            if indicator in rag_lower and len(rag_lower) < 100:  # Short responses with empty indicators
                return True
        
        # If response contains actual doctor names or useful info, don't consider it empty
        if any(keyword in rag_lower for keyword in [
            "dr.", "doctor", "specialist", "available", "appointment", "schedule", 
            "contact", "phone", "email", "neurologist", "cardiologist", "psychologist"
        ]):
            return False
            
        return False
    
    def _get_fallback_info(self, classification):
        """Get fallback information based on classification intent"""
        intent = classification.get("intent", "")
        
        if intent == "center_information":
            return "MediConnect Medical Center is located at 123 Medical Plaza, Colombo 07. Contact: +94 11 234 5678. Reception hours: 8 AM - 8 PM daily."
        elif intent in ["doctor_inquiry", "appointment_request"]:
            return (
                "Available doctors and specialists:\n"
                "• Dr. Silva (Cardiologist) - Today: 2 PM and 4 PM, Tomorrow: 10 AM and 2 PM\n"
                "• Dr. Perera (General Physician) - Today: 10 AM and 3 PM, Tomorrow: 9 AM and 1 PM\n"
                "• Dr. Fernando (Internal Medicine) - Today: 1 PM and 5 PM, Tomorrow: 11 AM and 4 PM\n"
                "• Dr. Jayawardena (Psychologist) - Today: 9 AM, 2 PM and 5 PM, Tomorrow: 10 AM and 3 PM\n"
                "• Dr. Mendis (Psychiatrist) - Today: 11 AM and 3 PM, Tomorrow: 2 PM and 6 PM\n"
                "• Dr. Kumar (Neurologist) - Today: 2 PM and 5 PM, Tomorrow: 10 AM and 3 PM\n"
                "• Dr. Wijesinghe (Mental Health Counselor) - Today: 10 AM, 1 PM and 4 PM\n\n"
                "Walk-ins accepted until 6 PM. Call +94 11 234 5678 to book appointments."
            )
        else:
            return "No specific information found in knowledge base"
    
    def _determine_conversation_stage(self):
        if not self.chat_history:
            return "initial"
        
        # Count user messages to determine stage
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
        """Save chat history and exit"""
        with open("chat_history.json", "w", encoding="utf-8") as f:
            json.dump(self.chat_history, f, indent=2)
        print("👋 Goodbye! Stay safe.")

def main():
    """Main interactive loop - Complete Workflow with RAG and Doc Support"""
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