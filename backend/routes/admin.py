# Admin routes for PDF ingestion and management

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from datetime import datetime, timezone
from bson import ObjectId
import os
import shutil
import tempfile
from pathlib import Path

from backend.schemas.user import AdminLogin, AdminPublic, Token
from backend.utils.hash import verify_password
from backend.database.mongodb import get_db
from backend.core.security import create_access_token, get_current_user
from backend.agents.ingest import ingest

# Router with /admin prefix
router = APIRouter(prefix="/admin", tags=["admin"])

# Admin credentials (in production, store in database with proper security)
ADMIN_EMAIL = "admin@mediconnect.lk"
ADMIN_PASSWORD_HASH = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj2Qc9QzQzQz"  # "admin123"

@router.post("/login", response_model=Token)
async def admin_login(payload: AdminLogin):
    """Admin login endpoint"""
    # Check admin credentials
    if payload.email != ADMIN_EMAIL:
        raise HTTPException(
            status_code=401,
            detail="Invalid admin credentials"
        )
    
    # Verify password (in production, use proper password hashing)
    if payload.password != "admin123":
        raise HTTPException(
            status_code=401,
            detail="Invalid admin credentials"
        )
    
    # Generate admin JWT token
    access_token = create_access_token(subject="admin")
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/me", response_model=AdminPublic)
async def get_admin_info():
    """Get admin information"""
    return {
        "id": "admin",
        "email": ADMIN_EMAIL,
        "created_at": datetime.now(timezone.utc),
        "is_admin": True
    }

@router.post("/upload-pdf")
async def upload_pdf(
    file: UploadFile = File(...),
    force_reindex: bool = Form(False),
    db=Depends(get_db)
):
    """Upload and ingest PDF file, then save/update metadata in MongoDB."""
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    # Resolve project-root data directory (outside backend and frontend)
    project_root = Path(__file__).parent.parent.parent
    data_dir = project_root / "data"
    data_dir.mkdir(exist_ok=True)

    file_path = data_dir / file.filename

    try:
        # Save uploaded file to disk
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Ingest and get manifest (handles delete + re-embed on update)
        manifest = ingest(str(file_path), force_reindex=force_reindex) or {}

        # Save metadata in MongoDB when db is available
        if db is not None:
            meta = {
                "title": file.filename,
                "path": str(file_path),
                "sha256": manifest.get("sha256"),
                "num_chunks": manifest.get("num_chunks", 0),
                "content_type": file.content_type or "application/pdf",
                "size_bytes": file_path.stat().st_size if file_path.exists() else None,
                "uploaded_at": datetime.now(timezone.utc),
                "force_reindex": bool(force_reindex),
            }
            # Upsert on title (filename); consider a better key later if needed
            await db["pdfs"].update_one(
                {"title": file.filename},
                {"$set": meta, "$setOnInsert": {"created_at": datetime.now(timezone.utc)}},
                upsert=True,
            )

        return {
            "status": "success",
            "message": f"PDF '{file.filename}' uploaded and ingested successfully",
            "filename": file.filename,
            "file_path": str(file_path),
            "manifest": manifest,
        }

    except Exception as e:
        # Clean up file if ingestion fails
        if file_path.exists():
            try:
                file_path.unlink()
            except Exception:
                pass
        raise HTTPException(status_code=500, detail=f"Failed to ingest PDF: {str(e)}")

@router.get("/ingest-status")
async def get_ingest_status():
    """Get current ingestion status"""
    # Always point to backend/chroma_mediconnect
    manifest_path = Path(__file__).parent.parent / "chroma_mediconnect" / "manifest.json"
    
    if not manifest_path.exists():
        return {
            "status": "no_data",
            "message": "No PDFs have been ingested yet",
            "last_ingestion": None,
            "total_chunks": 0
        }
    
    try:
        import json
        with open(manifest_path, "r") as f:
            manifest = json.load(f)
        
        return {
            "status": "success",
            "message": "Ingestion data available",
            "last_ingestion": manifest.get("source"),
            "total_chunks": manifest.get("num_chunks", 0),
            "file_hash": manifest.get("sha256", "")[:16] + "..."
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to read manifest: {str(e)}",
            "last_ingestion": None,
            "total_chunks": 0
        }

@router.post("/reingest")
async def reingest_existing():
    """Re-ingest existing PDF files"""
    data_dir = Path("data")
    
    if not data_dir.exists():
        raise HTTPException(
            status_code=404,
            detail="No data directory found"
        )
    
    pdf_files = list(data_dir.glob("*.pdf"))
    
    if not pdf_files:
        raise HTTPException(
            status_code=404,
            detail="No PDF files found in data directory"
        )
    
    try:
        # Re-ingest the first PDF found
        pdf_path = pdf_files[0]
        ingest(str(pdf_path), force_reindex=True)
        
        return {
            "status": "success",
            "message": f"Re-ingested PDF: {pdf_path.name}",
            "filename": pdf_path.name
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to re-ingest PDF: {str(e)}"
        )

@router.get("/health")
async def admin_health_check():
    """Health check for admin service"""
    return {
        "status": "healthy",
        "service": "Admin PDF Ingestion API",
        "endpoints": [
            "POST /admin/login",
            "GET /admin/me", 
            "POST /admin/upload-pdf",
            "GET /admin/ingest-status",
            "POST /admin/reingest"
        ]
    }
