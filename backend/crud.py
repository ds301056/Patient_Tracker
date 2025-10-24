from sqlalchemy.orm import Session
from models import Patient, Visit, Document, User
from schemas import PatientCreate, PatientUpdate, VisitCreate, DocumentCreate, UserCreate
from datetime import datetime
import random
import string


def generate_mrn():
    """Generate a unique Medical Record Number"""
    # Format: MRN-YYYYMMDD-XXXX
    date_part = datetime.now().strftime("%Y%m%d")
    random_part = ''.join(random.choices(string.digits, k=4))
    return f"MRN-{date_part}-{random_part}"


# ============= PATIENT CRUD =============

def create_patient(db: Session, patient: PatientCreate):
    """Create a new patient"""
    db_patient = Patient(
        **patient.model_dump(),
        medical_record_number=generate_mrn()
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


def get_patient(db: Session, patient_id: int):
    """Get a single patient by ID"""
    return db.query(Patient).filter(Patient.id == patient_id).first()


def get_patient_by_mrn(db: Session, mrn: str):
    """Get a patient by Medical Record Number"""
    return db.query(Patient).filter(Patient.medical_record_number == mrn).first()


def get_patients(db: Session, skip: int = 0, limit: int = 100):
    """Get all patients with pagination"""
    return db.query(Patient).offset(skip).limit(limit).all()


def update_patient(db: Session, patient_id: int, patient_update: PatientUpdate):
    """Update a patient"""
    db_patient = get_patient(db, patient_id)
    if not db_patient:
        return None
    
    update_data = patient_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_patient, key, value)
    
    db_patient.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_patient)
    return db_patient


def delete_patient(db: Session, patient_id: int):
    """Delete a patient"""
    db_patient = get_patient(db, patient_id)
    if not db_patient:
        return False
    
    db.delete(db_patient)
    db.commit()
    return True


# ============= VISIT CRUD =============

def create_visit(db: Session, visit: VisitCreate):
    """Create a new visit"""
    db_visit = Visit(**visit.model_dump())
    db.add(db_visit)
    db.commit()
    db.refresh(db_visit)
    return db_visit


def get_patient_visits(db: Session, patient_id: int):
    """Get all visits for a patient"""
    return db.query(Visit).filter(Visit.patient_id == patient_id).all()


# ============= DOCUMENT CRUD =============

def create_document(db: Session, document: DocumentCreate):
    """Create a new document record"""
    db_document = Document(**document.model_dump())
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document


def get_patient_documents(db: Session, patient_id: int):
    """Get all documents for a patient"""
    return db.query(Document).filter(Document.patient_id == patient_id).all()


# ============= USER CRUD =============

def create_user(db: Session, user: UserCreate):
    """Create a new user"""
    # TODO: Hash the password properly (use bcrypt)
    db_user = User(
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        role=user.role,
        hashed_password=f"hashed_{user.password}"  # PLACEHOLDER - use proper hashing
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()