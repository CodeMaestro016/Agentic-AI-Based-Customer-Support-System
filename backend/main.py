import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import auth
from backend.routes import chat
from backend.routes import admin
from backend.database.mongodb import connect_to_mongo, close_mongo_connection
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Customer Support System Backend",
    description="Agentic AI-Based Customer Support System API",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add routes
app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(admin.router)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check"""
    return {
        "status": "healthy",
        "message": "Customer Support System Backend is running",
        "version": "1.0.0",
        "services": {
            "database": "MongoDB connection tested during startup",
            "authentication": "Available at /api/auth",
            "chat_workflow": "Available at /api/chat",
            "agents": "medical_workflow, query_classifier, rag_agent, solution_agent, followup_agent, doc_summarizer"
        },
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "auth": "/api/auth",
            "chat": "/api/chat"
        }
    }

# API status endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Customer Support System API",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database connection"""
    try:
        await connect_to_mongo()
        logger.info("Application startup completed successfully")
    except Exception as e:
        logger.warning(f"Failed to connect to MongoDB: {e}")
        logger.warning("⚠️ Application starting without database connection - some features may not work")
        logger.info("💡 To fix this: Install MongoDB locally or set up MongoDB Atlas")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection"""
    await close_mongo_connection()
    logger.info("Application shutdown completed")
