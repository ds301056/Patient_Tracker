from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="HealthPlus API")

# CORS - allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def welcome():
    return {"message": "Welcome to HealthPlus"}


# ========================================
# STRUCTURE PLAN
# ========================================

# 1. MODELS (database tables)
#    - Patient (id, name, dob, contact, medical_record_number)
#    - Visit (id, patient_id, date, reason, notes)
#    - Document (id, patient_id, filename, url, uploaded_at)

# 2. DATABASE CONNECTION
#    - SQLAlchemy setup
#    - PostgreSQL connection
#    - Session management

# 3. API ENDPOINTS
#    
#    Patients:
#    - GET    /api/patients          - List all patients
#    - GET    /api/patients/{id}     - Get single patient
#    - POST   /api/patients          - Create patient
#    - PUT    /api/patients/{id}     - Update patient
#    - DELETE /api/patients/{id}     - Delete patient
#    
#    Visits:
#    - GET    /api/patients/{id}/visits  - Get patient visits
#    - POST   /api/patients/{id}/visits  - Add visit
#    
#    Documents:
#    - GET    /api/patients/{id}/documents  - List documents
#    - POST   /api/documents/upload         - Upload document
#    - GET    /api/documents/{id}/download  - Download document
#    
#    Analytics:
#    - GET    /api/analytics/stats          - Overall stats
#    - GET    /api/analytics/trends         - Visit trends

# 4. FOLDER STRUCTURE (future)
#    backend/
#    ├── app.py              # Main app (this file)
#    ├── models.py           # Database models
#    ├── database.py         # DB connection
#    ├── schemas.py          # Pydantic models (request/response)
#    ├── crud.py             # Database operations
#    └── requirements.txt    # Dependencies


# Azure details // What we can use from your existing setup:
# azure: {
#   subscriptionId: '7ea8d2a5-4906-4c6e-ad61-3a5d22e0c741',  // ✅ Use this
#   region: 'eastus',                                         // ✅ Keep same region
#   acrLoginServer: 'acrephemeraldemo182553.azurecr.io',     // ✅ Can reuse your ACR
# }

# // What we'll create NEW for HealthPlus:
# healthplus: {
#   resourceGroup: 'rg-healthplus-dev',                      // New RG
#   postgresServer: 'healthplus-psql',                       // New database
#   storageAccount: 'healthplusdocs',                        // New storage
#   containerInstance: 'healthplus-api',                     // New container
# }

# ========================================


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)