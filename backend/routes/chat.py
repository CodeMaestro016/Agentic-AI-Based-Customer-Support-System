# Chat API endpoints for the medical workflow system
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging
import sys
import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import asyncio
import json
from datetime import datetime

# Add agents directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "agents"))

from medical_workflow import MedicalWorkflow
from backend.schemas.chat import ChatDetail, ChatMessage
from backend.utils.hash import hash_chat_details
from backend.database.mongodb import upsert_chat_detail
from backend.core.security import get_current_user

# Setup logging
logger = logging.getLogger(__name__)

# Router setup
router = APIRouter(prefix="/api/chat", tags=["chat"])

# Request/Response models
class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    message: str
    chat_history: Optional[List[ChatMessage]] = []
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    classification: Dict[str, Any]
    rag_context: Optional[str] = None
    followup_questions: Optional[str] = None
    session_id: str
    chat_history: List[ChatMessage]

class DocumentRequest(BaseModel):
    document_content: str
    document_type: str = "text"  # "text" or "pdf_path"
    chat_history: Optional[List[ChatMessage]] = []
    session_id: Optional[str] = None

# Global workflow instance (in production, use dependency injection)
workflow_instance = None

def get_workflow():
    """Get or create workflow instance"""
    global workflow_instance
    if workflow_instance is None:
        try:
            workflow_instance = MedicalWorkflow()
            logger.info("Medical workflow initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize medical workflow: {e}")
            raise HTTPException(status_code=500, detail="Failed to initialize medical workflow")
    return workflow_instance

@router.post("/message", response_model=ChatResponse)
async def send_message(request: ChatRequest, current_user: dict = Depends(get_current_user), workflow: MedicalWorkflow = Depends(get_workflow)):
    """
    Send a message to the medical AI assistant
    
    This endpoint processes user queries through the complete medical workflow:
    1. Query Classification
    2. RAG retrieval (if needed)
    3. Solution generation
    4. Response formatting
    """
    try:
        # Set chat history if provided
        if request.chat_history:
            workflow.chat_history = [
                {"role": msg.role, "content": msg.content} 
                for msg in request.chat_history
            ]
        
        # Process the query in a thread pool to avoid blocking the async event loop
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            result = await loop.run_in_executor(executor, workflow.process_query, request.message)
        
        # Use user ID as session ID for grouping all chats per user
        session_id = current_user["id"]

        # Convert chat history back to response format
        chat_history = [
            ChatMessage(role=msg["role"], content=msg["content"])
            for msg in workflow.chat_history
        ]

        # Prepare unhashed chat history for response
        unhashed_chat_history = [msg.dict() for msg in chat_history]

        # Prepare hashed chat details for saving
        hashed_chat_history = [
            {
                "role": msg["role"],
                "content": hash_chat_details(msg["content"]),
                "timestamp": msg.get("timestamp")
            }
            for msg in workflow.chat_history
        ]
        hashed_data = {
            "session_id": session_id,
            "user_id": current_user["id"],
            "message": hash_chat_details(request.message),
            "chat_history": hashed_chat_history,
            "response": hash_chat_details(result["final_response"]),
            "classification": result["classification"],
            "rag_context": result.get("rag_context"),
            "followup_questions": result.get("followup_questions"),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        # Hash the hashed data for integrity
        hashed_data_json = json.dumps(hashed_data, sort_keys=True, default=str)
        hashed_details = hash_chat_details(hashed_data_json)
        hashed_data["hashed_details"] = hashed_details

        # Save hashed data to MongoDB asynchronously
        asyncio.create_task(upsert_chat_detail(hashed_data))

        return ChatResponse(
            response=result["final_response"],
            classification=result["classification"],
            rag_context=result.get("rag_context"),
            followup_questions=result.get("followup_questions"),
            session_id=session_id,
            chat_history=chat_history
        )
        
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

@router.post("/document", response_model=ChatResponse)
async def process_document(request: DocumentRequest, current_user: dict = Depends(get_current_user), workflow: MedicalWorkflow = Depends(get_workflow)):
    """
    Process a medical document (text or PDF)
    
    This endpoint handles document summarization through the workflow:
    1. Document processing
    2. Medical summarization
    3. Solution generation based on document content
    """
    try:
        # Set chat history if provided
        if request.chat_history:
            workflow.chat_history = [
                {"role": msg.role, "content": msg.content} 
                for msg in request.chat_history
            ]
        
        # Format document query
        if request.document_type == "pdf_path":
            doc_query = f"doc:{request.document_content}"
        else:
            doc_query = f"doc:{request.document_content}"
        
        # Process the document in a thread pool to avoid blocking the async event loop
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            result = await loop.run_in_executor(executor, workflow.process_query, doc_query)
        
        # Use user ID as session ID for grouping all chats per user
        session_id = current_user["id"]

        # Convert chat history back to response format
        chat_history = [
            ChatMessage(role=msg["role"], content=msg["content"])
            for msg in workflow.chat_history
        ]

        # Prepare unhashed chat history for response
        unhashed_chat_history = [msg.dict() for msg in chat_history]

        # Prepare hashed chat details for saving
        hashed_chat_history = [
            {
                "role": msg["role"],
                "content": hash_chat_details(msg["content"]),
                "timestamp": msg.get("timestamp")
            }
            for msg in workflow.chat_history
        ]
        hashed_data = {
            "session_id": session_id,
            "user_id": current_user["id"],
            "message": hash_chat_details(f"Document processing: {request.document_type} - Content: {request.document_content}"),
            "chat_history": hashed_chat_history,
            "response": hash_chat_details(result["final_response"]),
            "classification": result["classification"],
            "rag_context": result.get("document_summary"),
            "followup_questions": result.get("followup_questions"),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        # Hash the hashed data for integrity
        hashed_data_json = json.dumps(hashed_data, sort_keys=True, default=str)
        hashed_details = hash_chat_details(hashed_data_json)
        hashed_data["hashed_details"] = hashed_details

        # Save hashed data to MongoDB asynchronously
        asyncio.create_task(upsert_chat_detail(hashed_data))
        
        return ChatResponse(
            response=result["final_response"],
            classification=result["classification"],
            rag_context=result.get("document_summary", "No document summary available"),
            followup_questions=result.get("followup_questions"),
            session_id=session_id,
            chat_history=chat_history
        )
        
    except Exception as e:
        logger.error(f"Error processing document: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check for chat service"""
    try:
        # Test workflow initialization
        workflow = get_workflow()
        return {
            "status": "healthy",
            "service": "Medical Chat API",
            "agents": "medical_workflow, query_classifier, rag_agent, solution_agent, followup_agent, doc_summarizer",
            "workflow_initialized": workflow is not None
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")

@router.delete("/session/{session_id}")
async def clear_session(session_id: str, workflow: MedicalWorkflow = Depends(get_workflow)):
    """Clear chat history for a session"""
    try:
        # In a real application, you'd manage sessions per user
        # For now, just clear the current workflow history
        workflow.chat_history = []
        
        return {
            "status": "success",
            "message": f"Session {session_id} cleared",
            "session_id": session_id
        }
        
    except Exception as e:
        logger.error(f"Error clearing session: {e}")
        raise HTTPException(status_code=500, detail=f"Error clearing session: {str(e)}")

@router.get("/test")
async def test_workflow():
    """Test endpoint to verify all agents are working"""
    try:
        workflow = get_workflow()
        
        # Test classification
        test_query = "I have a headache"
        classification = workflow.query_classifier.classify_query(test_query)
        
        return {
            "status": "success",
            "message": "All agents are working properly",
            "test_query": test_query,
            "test_classification": classification,
            "available_agents": [
                "query_classifier",
                "rag_agent", 
                "solution_agent",
                "followup_agent",
                "doc_summarizer"
            ]
        }
        
    except Exception as e:
        logger.error(f"Workflow test failed: {e}")
        raise HTTPException(status_code=500, detail=f"Workflow test failed: {str(e)}")