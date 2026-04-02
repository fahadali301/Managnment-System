# Student Onboarding (A to Z)

This guide explains how to add students correctly in this project.

## Prerequisites

- Server running
- Admin user created (`python3 manage.py createsuperuser`)
- Base academic data exists

## Data Dependency Order

Add data in this order:

1. University
2. Department (inside University)
3. Program (inside Department)
4. Term
5. Course
6. Section (course + term)
7. User account for student
8. Student profile
9. Enrollment

---

## Option A: Add Student via Django Admin

1. Open `/admin/` and login.
2. Add University, Department, Program from `academics` models.
3. Add a new user from `company -> Users`.
4. Add Student Profile from `students -> Student profiles`:
   - Select the user
   - Select matching university and program
   - Set `student_id`, semester, active status
5. Add Enrollment from `students -> Enrollments`:
   - Select student profile
   - Select section
   - Status = `enrolled`

### Important Validation

- Program must belong to selected university.
- Enrollment is blocked if section capacity is full.

---

## Option B: Add Student via API

Base URL examples are for local run (`http://127.0.0.1:8000`).

### 1) Register user

`POST /api/v1/auth/register/`

```json
{
  "username": "student_001",
  "email": "student1@example.com",
  "full_name": "Student One",
  "password": "StrongPass@123",
  "password2": "StrongPass@123"
}
```

### 2) Login and get token

`POST /api/v1/auth/login/`

```json
{
  "username": "student_001",
  "password": "StrongPass@123"
}
```

Use returned `access` token as Bearer token.

### 3) Create Student Profile

`POST /api/v1/students/profiles/`

```json
{
  "user": 10,
  "university": 1,
  "program": 2,
  "student_id": "STU-2026-0001",
  "current_semester": 1,
  "is_active": true
}
```

### 4) Enroll Student in Section

`POST /api/v1/students/enrollments/`

```json
{
  "student": 1,
  "section": 3,
  "status": "enrolled"
}
```

---

## Troubleshooting

- `{"program": ... does not belong ...}` -> choose matching university/program.
- `{"section": "Section capacity is full."}` -> increase section capacity or choose another section.
- `401 Unauthorized` -> access token missing/expired.
- Student not showing on dashboard -> verify `students_studentprofile` entry exists.

