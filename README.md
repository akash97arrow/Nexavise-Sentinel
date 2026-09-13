# Nexavise Sentinel

Nexavise Sentinel is a cybersecurity monitoring and alerting MVP designed to demonstrate a simple security-event detection workflow.

The application allows an authenticated user to create security events, analyzes those events using a rule-based detection engine, assigns a risk score, generates alerts for detected threats, and provides a dashboard for monitoring and resolving alerts.

---

## 1. Project Overview

Nexavise Sentinel demonstrates the following security monitoring workflow:

```text
Security Event
      ↓
Detection Engine
      ↓
Threat Analysis
      ↓
Risk Score
      ↓
Alert Generation
      ↓
Security Dashboard
      ↓
Alert Resolution

---

## 2. Key Features

### Authentication

- User registration
- Password hashing using bcrypt
- JWT-based authentication
- Protected security-event and alert APIs
- Session-based frontend authentication
- Logout functionality

### Security Event Monitoring

- Create security events
- Store events in PostgreSQL
- View recent security events
- Track source IP addresses
- Track event severity

### Threat Detection

The current rule-based detection engine identifies:

- `BRUTE_FORCE`
- `MALWARE_DETECTED`
- High-severity events
- Medium-risk events

### Risk Scoring

| Event | Risk Score |
|---|---:|
| Malware detected | 100 |
| Brute-force attack | 90 |
| High severity event | 75 |
| Medium severity event | 50 |
| Normal event | 10 |

### Alert Management

- Automatically create alerts when a threat is detected
- Display alert risk scores
- Display alert status
- Resolve alerts from the dashboard

### Dashboard

The React dashboard displays:

- Total events
- Total alerts
- Open alerts
- High-risk alerts
- Recent security alerts
- Security events
- Risk score visualization
- Severity indicators

---

## 3. Technology Stack

### Frontend

- React
- TypeScript
- Vite
- CSS

### Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- JWT
- Passlib
- bcrypt

### Database

- PostgreSQL 16

### Infrastructure

- Docker
- Docker Compose

------

## 4. Architecture

Nexavise Sentinel follows a simple frontend-backend-database architecture.

```text
                    ┌─────────────────────┐
                    │    React Frontend   │
                    │  TypeScript + Vite  │
                    └──────────┬──────────┘
                               │
                         REST API + JWT
                               │
                               ▼
                    ┌─────────────────────┐
                    │   FastAPI Backend   │
                    ├─────────────────────┤
                    │ Authentication      │
                    │ Event API            │
                    │ Alert API            │
                    │ Detection Engine     │
                    │ Dashboard API        │
                    └──────────┬──────────┘
                               │
                          SQLAlchemy
                               │
                               ▼
                    ┌─────────────────────┐
                    │    PostgreSQL 16    │
                    ├─────────────────────┤
                    │ users               │
                    │ security_events     │
                    │ alerts              │
                    └─────────────────────┘

                    ---

## 5. Project Structure

```text
Nexavise-Sentinel/
│
├── backend/
│   ├── auth.py
│   ├── create_tables.py
│   ├── database.py
│   ├── dependencies.py
│   ├── detection.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   │
│   └── routers/
│       ├── users.py
│       ├── events.py
│       └── alerts.py
│
├── database/
│
├── docs/
│
├── frontend/
│
├── frontend-app/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AlertCard.tsx
│   │   │   ├── EventCard.tsx
│   │   │   ├── EventForm.tsx
│   │   │   └── StatCard.tsx
│   │   │
│   │   ├── App.tsx
│   │   ├── App.css
│   │   └── Login.tsx
│   │
│   └── package.json
│
├── worker/
│
├── docker-compose.yml
├── .gitignore
└── README.md


---

## 6. Database Schema

Nexavise Sentinel currently uses three main database tables.

### Users

Stores authenticated user accounts.

```text
users
----------------
id
name
email
password_hash


---

## 7. Docker PostgreSQL Setup

Nexavise Sentinel uses PostgreSQL 16 through Docker Compose.

The database configuration is:

```text
Database: sentinel
User: sentinel
Port: 5432


---

## 8. Backend Setup

The backend is built with Python and FastAPI.

### 1. Activate the Virtual Environment

From the project root:

```powershell
.\.venv\Scripts\Activate.ps1


---

## 9. Frontend Setup

The frontend is built using React, TypeScript, and Vite.

### 1. Open the Frontend Directory

From the project root:

```powershell
cd frontend-app

---

## 10. API Endpoints

### Authentication

#### Register User

```text
POST /users


---

## 11. Detection Engine and Risk Scoring

Nexavise Sentinel currently uses a deterministic, rule-based detection engine.

When a security event is created, the backend analyzes the event type and severity.

### Detection Flow

```text
Security Event
      ↓
Detection Engine
      ↓
Threat Analysis
      ↓
Risk Score
      ↓
Alert Generation


---

## 12. Authentication and Security

Nexavise Sentinel uses several security mechanisms in the current MVP.

### Password Security

User passwords are hashed using bcrypt before being stored in the database.

The database stores:

```text
password_hash


---

## 13. Demo Workflow

The following workflow demonstrates the main functionality of Nexavise Sentinel.

### Step 1 — Start the Application

Start PostgreSQL using Docker Compose:

```powershell
docker compose up -d


---

## 14. Assumptions

The current MVP is built with the following assumptions:

- Security events are simulated locally for demonstration purposes.
- Source IP addresses are provided as part of the submitted event data.
- Threat detection is based on deterministic rules.
- Risk scores are assigned according to the implemented detection rules.
- PostgreSQL is used as the persistent database.
- Docker Compose is used to run PostgreSQL locally.
- Authentication is designed for the MVP demonstration environment.
- The application is not intended to perform unauthorized activity against external systems.

---


---

## 15. Limitations

Nexavise Sentinel is currently an MVP intended for demonstration and assessment purposes.

The current version does not yet include:

- Real network scanning
- Real endpoint telemetry collection
- Automated asset discovery
- Advanced vulnerability scanning
- CVE enrichment
- SIEM integrations
- Production-grade secret management
- Advanced role-based access control
- Distributed background workers
- Machine-learning-based threat detection
- Automated attack-path analysis
- Production deployment configuration

These capabilities can be added in future iterations.

---


---

## 16. Future Improvements

The following capabilities can be added in future versions:

1. Automated asset discovery
2. Network and service scanning
3. Vulnerability detection
4. CVE enrichment
5. Threat intelligence integration
6. Attack-path visualization
7. Background security workers
8. Advanced risk scoring
9. Role-based access control
10. Audit logging
11. Secure environment-based secret management
12. Automated security reports
13. Production deployment support

---


---

## 17. Safe Testing

The application is designed to demonstrate security monitoring using simulated events in a local environment.

Example test event:

```text
Event Type:
BRUTE_FORCE

Source IP:
10.0.0.50

Description:
Repeated failed login attempts detected

Severity:
HIGH


---

## 18. Project Status

Current MVP functionality:

- [x] PostgreSQL database
- [x] Docker Compose setup
- [x] FastAPI backend
- [x] SQLAlchemy models
- [x] User registration
- [x] Password hashing
- [x] JWT authentication
- [x] Security event API
- [x] Rule-based detection engine
- [x] Risk scoring
- [x] Alert generation
- [x] Alert resolution
- [x] Dashboard statistics
- [x] React dashboard
- [x] Security event display
- [x] Alert display
- [x] Risk score visualization
- [x] Severity indicators
- [x] Security event creation form
- [x] Logout/session handling

---

## 19. License

This project was developed as a cybersecurity product-development assessment MVP.