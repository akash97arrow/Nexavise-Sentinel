# Nexavise Sentinel

Nexavise Sentinel is a cybersecurity monitoring and security assessment platform built with React, FastAPI, PostgreSQL, and Docker.

The platform provides authenticated security monitoring, authorized asset management, TCP service scanning, risk-based findings, attack-path generation, security-event detection, alert management, scan history, and HTML security reports.

---

## Features

### Authentication

- User registration
- Bcrypt password hashing
- JWT-based authentication
- Protected APIs
- Session-based frontend authentication
- Logout and session-expiration handling
- User-specific data access

### Asset Management

- Create authorized security assets
- Asset ownership by authenticated user
- Authorization status enforcement
- Target and asset-type tracking
- Only explicitly authorized assets can be scanned

### Network Scanning

The platform performs TCP connectivity checks against authorized targets.

Currently supported common services include:

- FTP - 21
- SSH - 22
- SMTP - 25
- DNS - 53
- HTTP - 80
- POP3 - 110
- IMAP - 143
- HTTPS - 443
- MySQL - 3306
- PostgreSQL - 5432
- HTTP - 8000
- HTTP - 8080

The scanner records:

- Port
- Protocol
- Service
- State
- Scan ID
- Discovery timestamp

Scanning includes target validation, connection timeouts, authorization checks, ownership checks, and a per-asset scan cooldown.

---

## Security Findings

The finding engine analyzes discovered open services and generates security findings.

Examples include:

- Exposed MySQL Service
- Exposed PostgreSQL Service
- Exposed HTTP Service
- Exposed SSH Service
- Other exposed services

Each finding contains:

- Severity
- Risk score
- Risk level
- Description
- Status
- Asset
- Scan result
- Creation timestamp

Findings can be:

```text
OPEN
  ↓
RESOLVED
  ↓
OPEN

--------------------------------------------------------------------------------------------------------

Risk Scoring
Nexavise Sentinel uses a deterministic risk-scoring engine.
Risk calculation considers:
- Finding severity
- Target exposure
- Service sensitivity
- Configuration factors

Example risk levels include:

| Service | Example Risk Score | Level |
|---|---:|---|
| MySQL | 60 | HIGH |
| PostgreSQL | 60 | HIGH |
| HTTP | 42 | MEDIUM |
| SSH | 46 | MEDIUM |

--------------------------------------------------------------------------------------------------------

Finding Occurrences
The platform tracks repeated occurrences of findings across scans.
This provides:
- Finding history
- Occurrence count
- Last-seen scan
- Scan-to-finding relationship
This allows a finding to remain tracked across multiple scans instead of being treated as an entirely new issue every time.

--------------------------------------------------------------------------------------------------------

Attack Paths
Nexavise Sentinel generates potential attack paths from exposed services and security findings.
Examples include:
- MySQL database
- PostgreSQL database
- Web service
- SSH remote access
Each attack path contains:
- Entry point
- Asset ID
- Finding ID
- Risk score
- Risk level
- Status
- Creation timestamp
Attack paths support:

OPEN
  ↓
RESOLVED
  ↓
OPEN

--------------------------------------------------------------------------------------------------------

Security Event Detection
The platform provides a rule-based security-event detection engine.
Supported examples include:
- BRUTE_FORCE
- MALWARE_DETECTED
- High-severity events
- Medium-risk events

Example risk mapping:

| Event | Risk Score |
|---|---:|
| Malware detected | 100 |
| Brute-force attack | 90 |
| High severity event | 75 |
| Medium severity event | 50 |
| Normal event | 10 |

When a detected threat is identified, the system automatically creates a security alert.

--------------------------------------------------------------------------------------------------------

Alert Management
Alerts contain:
- Event reference
- Risk score
- Message
- Status
- Creation timestamp
- User ownership
Alert lifecycle:

OPEN
  ↓
RESOLVED

Alerts are isolated by authenticated user ownership.

--------------------------------------------------------------------------------------------------------

Security Dashboard
The React dashboard provides an overview of the security environment.
It displays:
- Total events
- Total alerts
- Open alerts
- Resolved alerts
- High-risk alerts
- Total findings
- Open findings
- Resolved findings
- Critical findings
- Total attack paths
- Open attack paths
- Resolved attack paths
The dashboard also provides:
- Authorized asset cards
- Scan results
- Scan history
- Security findings
- Finding resolution
- Attack-path management
- Security-event creation
- Alert management
- Security report generation

--------------------------------------------------------------------------------------------------------

Security Reports
The platform can generate an HTML security report for an authorized asset.
Reports can contain:
- Asset information
- Authorization status
- Latest scan information
- Scan results
- Security findings
- Risk information
- Attack paths
Report generation is protected by authenticated user ownership.

--------------------------------------------------------------------------------------------------------

Technology Stack
Frontend
- React
- TypeScript
- Vite
- CSS
Backend
- Python
- FastAPI
- SQLAlchemy
- Pydantic
- Python-JOSE
- Passlib
- Bcrypt
Database
- PostgreSQL 16
Database Migrations
- Alembic
Infrastructure
- Docker
- Docker Compose

--------------------------------------------------------------------------------------------------------

Architecture
                    ┌─────────────────────────┐
                    │      React Frontend     │
                    │   TypeScript + Vite     │
                    └────────────┬────────────┘
                                 │
                           REST API + JWT
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │     FastAPI Backend     │
                    ├─────────────────────────┤
                    │ Authentication          │
                    │ User Management         │
                    │ Asset Management        │
                    │ Network Scanner         │
                    │ Finding Engine          │
                    │ Risk Engine             │
                    │ Attack Path Engine      │
                    │ Security Events         │
                    │ Threat Detection        │
                    │ Alert Management        │
                    │ Reports                 │
                    └────────────┬────────────┘
                                 │
                            SQLAlchemy
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │      PostgreSQL 16      │
                    ├─────────────────────────┤
                    │ users                   │
                    │ assets                  │
                    │ scans                   │
                    │ scan_results            │
                    │ findings                │
                    │ finding_occurrences     │
                    │ attack_paths            │
                    │ security_events         │
                    │ alerts                  │
                    └─────────────────────────┘

--------------------------------------------------------------------------------------------------------

Project Structure

Nexavise-Sentinel/
│
├── backend/
│   ├── auth.py
│   ├── database.py
│   ├── dependencies.py
│   ├── detection.py
│   ├── finding_engine.py
│   ├── risk_engine.py
│   ├── attack_path_engine.py
│   ├── scanner.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   │
│   └── routers/
│       ├── users.py
│       ├── assets.py
│       ├── scans.py
│       ├── findings.py
│       ├── finding_occurrences.py
│       ├── attack_paths.py
│       ├── events.py
│       ├── alerts.py
│       ├── reports.py
│       └── report_export.py
│
├── database/
│   └── migrations/
│       └── versions/
│
├── frontend-app/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AlertCard.tsx
│   │   │   ├── AssetCard.tsx
│   │   │   ├── EventCard.tsx
│   │   │   ├── EventForm.tsx
│   │   │   ├── Findings.tsx
│   │   │   ├── ScanHistory.tsx
│   │   │   └── ScanResults.tsx
│   │   │
│   │   ├── App.tsx
│   │   └── App.css
│   │
│   └── package.json
│
├── docs/
├── worker/
├── alembic.ini
├── docker-compose.yml
├── .gitignore
└── README.md

--------------------------------------------------------------------------------------------------------

Database Schema
The current database contains the following main tables:

users
assets
scans
scan_results
findings
finding_occurrences
attack_paths
security_events
alerts

Alembic uses the following table to track database migrations:

alembic_version

--------------------------------------------------------------------------------------------------------

Setup
Prerequisites
Install:
- Python 3.11+
- Node.js
- npm
- Docker Desktop
- Git

--------------------------------------------------------------------------------------------------------

1. Clone the Repository

git clone https://github.com/akash97arrow/Nexavise-Sentinel.git
cd Nexavise-Sentinel

--------------------------------------------------------------------------------------------------------

2. Start PostgreSQL

Start PostgreSQL using Docker Compose:
docker compose up -d

Check the running containers:
docker ps

--------------------------------------------------------------------------------------------------------

3. Configure Environment Variables

Create a .env file in the project root.
Example:

DATABASE_URL=postgresql+psycopg://<username>:<password>@localhost:5432/<database>
SECRET_KEY=<strong-random-secret>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

Do not commit .env or secrets to Git.

--------------------------------------------------------------------------------------------------------

4. Backend Setup

Create the Python virtual environment:
python -m venv .venv

Activate it:
.\.venv\Scripts\Activate.ps1

Install the required packages:
pip install fastapi uvicorn sqlalchemy psycopg[binary] python-dotenv python-jose passlib bcrypt alembic

--------------------------------------------------------------------------------------------------------

5. Run Database Migrations

Check the current migration:
alembic current

Upgrade the database to the latest migration:
alembic upgrade head

--------------------------------------------------------------------------------------------------------

6. Start the Backend

From the project root:
uvicorn backend.main:app --reload

Backend:
http://127.0.0.1:8000

Swagger API documentation:
http://127.0.0.1:8000/docs

--------------------------------------------------------------------------------------------------------

7. Start the Frontend

Open another terminal:
cd frontend-app
npm install
npm run dev

Open the URL displayed by Vite.

--------------------------------------------------------------------------------------------------------

Testing

Nexavise Sentinel should only be used against systems and assets for which authorization has been obtained.

A safe local demonstration target is:
127.0.0.1

Example workflow:
Login
  ↓
Create / Select Authorized Asset
  ↓
Start Scan
  ↓
Discover TCP Services
  ↓
Generate Findings
  ↓
Calculate Risk
  ↓
Generate Attack Paths
  ↓
Create Security Events
  ↓
Detect Threats
  ↓
Generate Alerts
  ↓
Resolve Findings / Alerts / Attack Paths
  ↓
Generate Security Report

--------------------------------------------------------------------------------------------------------

API Documentation

Interactive API documentation is available through FastAPI Swagger:
http://127.0.0.1:8000/docs

The API includes endpoints for:
- Authentication
- Users
- Assets
- Scans
- Scan results
- Findings
- Finding occurrences
- Attack paths
- Security events
- Alerts
- Dashboard statistics
- Security reports

--------------------------------------------------------------------------------------------------------

Security Considerations

The current implementation includes:
- Password hashing
- JWT authentication
- Protected APIs
- User ownership checks
- Authorized asset enforcement
- Target validation
- Scan cooldown protection
- Input validation
- Error handling
- HTML escaping for generated reports
- Database migrations
- Environment-based secrets
- Safe local testing workflow
The application is designed to perform security assessment only against authorized targets.

--------------------------------------------------------------------------------------------------------

Current Project Status

The core Nexavise Sentinel platform is implemented and tested.
- React frontend
- TypeScript
- Vite
- FastAPI backend
- PostgreSQL
- Docker Compose
- SQLAlchemy
- Alembic migrations
- User registration
- Bcrypt password hashing
- JWT authentication
- Protected APIs
- User ownership
- Authorized asset management
- TCP service scanner
- Scan history
- Scan results
- Finding engine
- Risk scoring
- Finding occurrences
- Attack-path generation
- Security-event detection
- Alert generation
- Alert resolution
- Finding resolution
- Attack-path resolution
- Dashboard statistics
- Security report export
- Frontend loading states
- Frontend error handling
- Session-expiration handling
- Production frontend build
- End-to-end testing

--------------------------------------------------------------------------------------------------------

Future Improvements

Possible future enhancements include:
1. Automated asset discovery
2. Broader service fingerprinting
3. Vulnerability database integration
4. CVE enrichment
5. Threat intelligence integration
6. Background scan workers
7. Advanced role-based access control
8. Audit-log expansion
9. Attack-path visualization
10. Production deployment
11. Centralized observability
12. Advanced vulnerability assessment

--------------------------------------------------------------------------------------------------------

Project

Nexavise Sentinel

Cybersecurity monitoring and security assessment platform.

Repository:
https://github.com/akash97arrow/Nexavise-Sentinel

