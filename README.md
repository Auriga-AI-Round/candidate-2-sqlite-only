# Hospital Management (Flask)

Simple API for patients, doctors, appointments.

Storage is **SQLite** (`hospital.db`), created on first run.

## Setup
```bash
pip install flask
python app.py   # http://localhost:5000
```

Implemented: patient/doctor create+list, appointment booking with a same-time clash
check. No overlap handling, search, or billing.

## Submission
App URL: http://localhost:5000
API base: http://localhost:5000/api
Username:
Password:
Endpoints:
  - GET /api/patients
  - GET /api/doctors
  - GET /api/appointments
