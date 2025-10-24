from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    """User model - for staff/doctors who use the system"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(String, default="staff")  # staff, doctor, admin
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    # patients = relationship("Patient", back_populates="assigned_doctor")


class Patient(Base):
    """Patient model - core entity"""
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    medical_record_number = Column(String, unique=True, index=True, nullable=False)
    
    # Personal Info
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String)  # Male, Female, Other
    
    # Contact Info
    email = Column(String)
    phone = Column(String)
    address = Column(Text)
    
    # Medical Info
    blood_type = Column(String)  # A+, B+, O-, etc.
    allergies = Column(Text)  # Store as comma-separated or JSON
    
    # System Info
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # assigned_doctor_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    # assigned_doctor = relationship("User", back_populates="patients")
    visits = relationship("Visit", back_populates="patient", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="patient", cascade="all, delete-orphan")


class Visit(Base):
    """Visit/Appointment model"""
    __tablename__ = "visits"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    
    visit_date = Column(DateTime, nullable=False)
    reason = Column(String, nullable=False)
    diagnosis = Column(Text)
    treatment = Column(Text)
    notes = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    patient = relationship("Patient", back_populates="visits")


class Document(Base):
    """Document/File model"""
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    
    filename = Column(String, nullable=False)
    file_type = Column(String)  # pdf, jpg, png, etc.
    file_url = Column(String, nullable=False)  # Local path or Azure Blob URL
    file_size = Column(Integer)  # in bytes
    description = Column(Text)
    
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    patient = relationship("Patient", back_populates="documents")