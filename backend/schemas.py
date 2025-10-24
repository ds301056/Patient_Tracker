from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional, List


# ============= PATIENT SCHEMAS =============

class PatientBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    gender: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    blood_type: Optional[str] = None
    allergies: Optional[str] = None


class PatientCreate(PatientBase):
    """Schema for creating a new patient"""
    pass


class PatientUpdate(BaseModel):
    """Schema for updating a patient - all fields optional"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    blood_type: Optional[str] = None
    allergies: Optional[str] = None


class Patient(PatientBase):
    """Schema for patient response"""
    id: int
    medical_record_number: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============= VISIT SCHEMAS =============

class VisitBase(BaseModel):
    visit_date: datetime
    reason: str
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    notes: Optional[str] = None


class VisitCreate(VisitBase):
    """Schema for creating a new visit"""
    patient_id: int


class Visit(VisitBase):
    """Schema for visit response"""
    id: int
    patient_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ============= DOCUMENT SCHEMAS =============

class DocumentBase(BaseModel):
    filename: str
    file_type: Optional[str] = None
    description: Optional[str] = None


class DocumentCreate(DocumentBase):
    """Schema for creating a new document"""
    patient_id: int
    file_url: str
    file_size: Optional[int] = None


class Document(DocumentBase):
    """Schema for document response"""
    id: int
    patient_id: int
    file_url: str
    file_size: Optional[int] = None
    uploaded_at: datetime

    class Config:
        from_attributes = True


# ============= USER SCHEMAS =============

class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    role: str = "staff"


class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str


class User(UserBase):
    """Schema for user response"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ============= PATIENT WITH RELATIONSHIPS =============

class PatientDetail(Patient):
    """Patient with visits and documents"""
    visits: List[Visit] = []
    documents: List[Document] = []

    class Config:
        from_attributes = True