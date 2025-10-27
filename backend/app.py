from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

import database
import crud
import schemas
from database import get_db, init_db

app = FastAPI(title="HealthPlus API", version="1.0.0")

# CORS - allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()


@app.get("/")
def welcome():
    return {
        "message": "Welcome to HealthPlus API",
        "version": "1.0.0",
        "docs": "/docs"
    }


# ========================================
# PATIENT ENDPOINTS
# ========================================

@app.get("/api/patients", response_model=List[schemas.Patient])
def list_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all patients with pagination"""
    patients = crud.get_patients(db, skip=skip, limit=limit)
    return patients


@app.get("/api/patients/{patient_id}", response_model=schemas.PatientDetail)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    """Get a single patient with their visits and documents"""
    patient = crud.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@app.post("/api/patients", response_model=schemas.Patient, status_code=201)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    """Create a new patient"""
    return crud.create_patient(db, patient)


@app.put("/api/patients/{patient_id}", response_model=schemas.Patient)
def update_patient(
    patient_id: int,
    patient_update: schemas.PatientUpdate,
    db: Session = Depends(get_db)
):
    """Update a patient"""
    updated_patient = crud.update_patient(db, patient_id, patient_update)
    if not updated_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return updated_patient


@app.delete("/api/patients/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    """Delete a patient"""
    success = crud.delete_patient(db, patient_id)
    if not success:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"message": "Patient deleted successfully"}


# ========================================
# VISIT ENDPOINTS
# ========================================

@app.get("/api/patients/{patient_id}/visits", response_model=List[schemas.Visit])
def get_patient_visits(patient_id: int, db: Session = Depends(get_db)):
    """Get all visits for a patient"""
    # Check if patient exists
    patient = crud.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    visits = crud.get_patient_visits(db, patient_id)
    return visits


@app.post("/api/patients/{patient_id}/visits", response_model=schemas.Visit, status_code=201)
def create_visit(
    patient_id: int,
    visit: schemas.VisitCreate,
    db: Session = Depends(get_db)
):
    """Create a new visit for a patient"""
    # Check if patient exists
    patient = crud.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Ensure patient_id in visit matches URL parameter
    visit.patient_id = patient_id
    return crud.create_visit(db, visit)


# ========================================
# DOCUMENT ENDPOINTS
# ========================================

@app.get("/api/patients/{patient_id}/documents", response_model=List[schemas.Document])
def get_patient_documents(patient_id: int, db: Session = Depends(get_db)):
    """Get all documents for a patient"""
    # Check if patient exists
    patient = crud.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    documents = crud.get_patient_documents(db, patient_id)
    return documents


@app.post("/api/documents/upload", response_model=schemas.Document, status_code=201)
def upload_document(document: schemas.DocumentCreate, db: Session = Depends(get_db)):
    """
    Create a document record.
    Note: Actual file upload to Azure Blob Storage would be handled separately.
    For now, this just creates the metadata record.
    """
    # Check if patient exists
    patient = crud.get_patient(db, document.patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    return crud.create_document(db, document)


# ========================================
# ANALYTICS ENDPOINTS
# ========================================

@app.get("/api/analytics/stats")
def get_stats(db: Session = Depends(get_db)):
    """Get overall statistics"""
    from models import Patient, Visit, Document

    total_patients = db.query(Patient).count()
    total_visits = db.query(Visit).count()
    total_documents = db.query(Document).count()

    # Get recent visits (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_visits = db.query(Visit).filter(Visit.visit_date >= thirty_days_ago).count()

    # Get new patients (last 30 days)
    new_patients = db.query(Patient).filter(Patient.created_at >= thirty_days_ago).count()

    return {
        "total_patients": total_patients,
        "total_visits": total_visits,
        "total_documents": total_documents,
        "recent_visits_30d": recent_visits,
        "new_patients_30d": new_patients,
        "avg_visits_per_patient": round(total_visits / total_patients, 2) if total_patients > 0 else 0
    }


@app.get("/api/analytics/trends")
def get_trends(db: Session = Depends(get_db)):
    """Get visit trends over time"""
    from models import Visit
    from sqlalchemy import func, extract

    # Get visits grouped by month
    visits_by_month = db.query(
        extract('year', Visit.visit_date).label('year'),
        extract('month', Visit.visit_date).label('month'),
        func.count(Visit.id).label('count')
    ).group_by('year', 'month').order_by('year', 'month').all()

    trends = [
        {
            "year": int(year),
            "month": int(month),
            "visit_count": count
        }
        for year, month, count in visits_by_month
    ]

    return {"trends": trends}


# ========================================
# HEALTH CHECK
# ========================================

@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
