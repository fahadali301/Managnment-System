# University Management System

A Django-based university admin portal with JWT auth, modular APIs, and a modern dashboard.

## Current Modules

- `company`: user/auth endpoints
- `academics`: university, departments, programs, terms, courses, sections
- `students`: student profiles and enrollments
- `managment_system`: project config and dashboard route

## API Routes

- `/api/v1/auth/` -> register, login, profile
- `/api/v1/academics/` -> academics master data
- `/api/v1/students/` -> student profiles and enrollments

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver
```

## Database

- PostgreSQL is used when `POSTGRES_DB` is set.
- SQLite is used as fallback if Postgres env vars are not provided.

## Health Check

```bash
python3 manage.py check
python3 manage.py test academics students company
```

## Student Add Flow (A to Z)

Detailed guide: `docs/student-onboarding.md`

Quick dependency order:

1. University
2. Department
3. Program
4. Term
5. Course
6. Section
7. User
8. StudentProfile
9. Enrollment

## Notes

- Dashboard student count comes from `StudentProfile` records.
- Program/university consistency is validated in `StudentProfileSerializer`.
- Section seat capacity is validated in `EnrollmentSerializer`.
