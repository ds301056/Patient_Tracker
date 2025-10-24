# Patient_Tracker

# Patient Management Portfolio Project Plan

## Core Stack
- **Frontend**: Next.js 14 (App Router, TypeScript)
- **Backend API**: Node.js (Next.js API routes) + Python microservice
- **Database**: Azure PostgreSQL Flexible Server
- **Storage**: Azure Blob Storage (patient documents)
- **Infrastructure**: Terraform for IaC
- **CI/CD**: GitHub Actions

## Architecture

### Frontend (Next.js)
- Patient dashboard (list, search, filter)
- Patient detail view (demographics, visits, documents)
- Simple forms (add/edit patient, log visit)
- Document upload interface

### Backend Services
**Next.js API Routes (Node):**
- `/api/patients` - CRUD operations
- `/api/visits` - Visit history
- `/api/documents` - Upload/download handling

**Python Microservice:**
- Analytics endpoint (patient statistics, visit trends)
- Document processing (OCR simulation, metadata extraction)
- Deployed as Azure Container Instance (ephemeral)

### Data Model (PostgreSQL)
```
patients: id, name, dob, contact, medical_record_number
visits: id, patient_id, date, reason, notes
documents: id, patient_id, filename, blob_url, uploaded_at
```

## DevOps Strategy (Cost-Efficient)

### Terraform Modules
1. **Base Infrastructure** (always on, minimal cost)
   - Resource Group
   - Storage Account
   - Database (Burstable B1ms tier, auto-pause enabled)

2. **Ephemeral Resources** (created on-demand)
   - Container Instances for Python service
   - App Service during demo periods
   
### GitHub Actions Workflows
1. **`deploy-infra.yml`** - Provisions infrastructure
2. **`destroy-infra.yml`** - Tears down ephemeral resources
3. **`deploy-app.yml`** - Deploys application code
4. **`scheduled-cleanup.yml`** - Runs nightly to destroy unused resources

### Cost Optimization Features
- Database auto-pause after 60 min inactivity
- Container Instances with manual start/stop
- Static site export option for Next.js (deploy to Azure Static Web Apps - free tier)
- Terraform state in Azure Storage
- Environment variables for "demo mode" vs "development mode"

## Key DevOps Demonstrations

1. **Infrastructure as Code**
   - Modular Terraform structure
   - Separate state per environment
   - Outputs for service URLs

2. **CI/CD Pipeline**
   - Automated testing
   - Preview environments for PRs
   - Production deployment with approval gates
   - Automatic rollback capability

3. **Monitoring & Observability**
   - Azure Application Insights (free tier)
   - Logging aggregation
   - Basic health checks

4. **Security**
   - Key Vault for secrets
   - Managed identities
   - CORS configuration
   - Input validation

## Project Structure
```
patient-portal/
├── frontend/              # Next.js app
├── python-service/        # Flask/FastAPI microservice
├── terraform/
│   ├── modules/
│   │   ├── base/         # Always-on resources
│   │   └── ephemeral/    # On-demand resources
│   └── environments/
├── .github/workflows/
└── docs/
```

## Implementation Phases
1. **Phase 1**: Next.js frontend + local dev setup
2. **Phase 2**: Terraform base infrastructure + PostgreSQL
3. **Phase 3**: Python microservice + containerization
4. **Phase 4**: CI/CD pipelines + ephemeral resource automation
5. **Phase 5**: Documentation + demo scenarios

**Estimated Azure Monthly Cost (during active development)**: $10-20
**Cost when idle**: $0-5 (storage only)

