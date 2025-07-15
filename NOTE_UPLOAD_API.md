# 📝 Note Upload API Flow Documentation

This document explains the proper hierarchical flow for uploading notes following the **Scheme → Semester → Subject** structure.

## 🔄 Complete Note Upload Flow

### Step 1: Get Available Schemes and Semesters

**Endpoint**: `GET /api/academics/upload/schemes/`
**Auth**: Required (any authenticated user)

```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     http://127.0.0.1:8001/api/academics/upload/schemes/
```

**Response**:

```json
{
  "message": "Found 3 schemes with available subjects",
  "schemes": [
    {
      "scheme": 2021,
      "available_semesters": [1, 2, 3, 4, 5, 6]
    },
    {
      "scheme": 2022,
      "available_semesters": [1, 2, 3, 4]
    },
    {
      "scheme": 2023,
      "available_semesters": [1, 2]
    }
  ],
  "note": "Select a scheme and semester to see available subjects for note upload"
}
```

### Step 2: Get Subjects for Selected Scheme and Semester

**Endpoint**: `GET /api/academics/upload/subjects/?scheme=2023&semester=1`
**Auth**: Required (any authenticated user)

```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     "http://127.0.0.1:8001/api/academics/upload/subjects/?scheme=2023&semester=1"
```

**Response**:

```json
{
  "scheme": 2023,
  "semester": 1,
  "message": "Found 4 subjects for scheme 2023, semester 1",
  "subjects": [
    {
      "id": 29,
      "name": "Calculus and Linear Algebra",
      "code": "MA101",
      "scheme": 2023,
      "semester": 1,
      "credits": 4,
      "is_active": true,
      "created_at": "2025-07-05T20:38:30.486836Z",
      "updated_at": "2025-07-05T20:38:30.486852Z"
    },
    {
      "id": 30,
      "name": "Physics for Engineers",
      "code": "PH101",
      "scheme": 2023,
      "semester": 1,
      "credits": 3,
      "is_active": true,
      "created_at": "2025-07-05T20:38:30.487822Z",
      "updated_at": "2025-07-05T20:38:30.487834Z"
    }
    // ... more subjects
  ]
}
```

### Step 3: Upload Note with Scheme, Semester, and Subject

**Endpoint**: `POST /api/academics/notes/upload/`
**Auth**: Required (Students, Admins, Technical Heads)

```bash
curl -X POST \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "Content-Type: multipart/form-data" \
     -F "title=Linear Algebra Notes Chapter 1" \
     -F "description=Comprehensive notes covering matrices and determinants" \
     -F "scheme=2023" \
     -F "semester=1" \
     -F "subject=29" \
     -F "file=@/path/to/your/notes.pdf" \
     http://127.0.0.1:8001/api/academics/notes/upload/
```

**Response**:

```json
{
  "message": "Note uploaded successfully",
  "note": {
    "id": 1,
    "title": "Linear Algebra Notes Chapter 1",
    "description": "Comprehensive notes covering matrices and determinants",
    "subject_details": {
      "id": 29,
      "name": "Calculus and Linear Algebra",
      "code": "MA101",
      "scheme": 2023,
      "semester": 1,
      "credits": 4
    },
    "uploaded_by": {
      "id": 4,
      "username": "student1",
      "email": "student1@eesa.com",
      "role": "student"
    },
    "file": "/media/notes/2023/1/MA101/notes.pdf",
    "is_approved": false,
    "approved_by": null,
    "approved_at": null,
    "created_at": "2025-07-05T21:00:00Z"
  }
}
```

## 🚨 Error Handling

### Missing Scheme/Semester Parameters

```json
{
  "error": "Both scheme and semester parameters are required",
  "required_params": ["scheme", "semester"]
}
```

### Invalid Scheme/Semester Combination

```json
{
  "error": "No subjects found for scheme 2024, semester 1",
  "scheme": 2024,
  "semester": 1,
  "subjects": []
}
```

### Subject Validation Errors

```json
{
  "subject": ["Selected subject does not belong to scheme 2023, semester 1"]
}
```

### Invalid Semester Range

```json
{
  "error": "Semester must be between 1 and 8"
}
```

## 🎯 Frontend Implementation Guide

### React/JavaScript Example

```javascript
// Step 1: Get available schemes
const getSchemes = async () => {
  const response = await fetch("/api/academics/upload/schemes/", {
    headers: { Authorization: `Bearer ${accessToken}` },
  });
  return await response.json();
};

// Step 2: Get subjects for selected scheme/semester
const getSubjects = async (scheme, semester) => {
  const response = await fetch(
    `/api/academics/upload/subjects/?scheme=${scheme}&semester=${semester}`,
    { headers: { Authorization: `Bearer ${accessToken}` } }
  );
  return await response.json();
};

// Step 3: Upload note
const uploadNote = async (noteData) => {
  const formData = new FormData();
  formData.append("title", noteData.title);
  formData.append("description", noteData.description);
  formData.append("scheme", noteData.scheme);
  formData.append("semester", noteData.semester);
  formData.append("subject", noteData.subjectId);
  formData.append("file", noteData.file);

  const response = await fetch("/api/academics/notes/upload/", {
    method: "POST",
    headers: { Authorization: `Bearer ${accessToken}` },
    body: formData,
  });
  return await response.json();
};
```

## 🔐 Permission Requirements

- **Step 1 & 2**: Any authenticated user can view schemes and subjects
- **Step 3**: Only Students, Admins, and Technical Heads can upload notes
- **Note Approval**: Teachers, Admins, and assigned Student Reviewers

## 📋 Validation Rules

1. **Scheme**: Must be a valid integer with available subjects
2. **Semester**: Must be between 1-8 and have subjects in the selected scheme
3. **Subject**: Must belong to the specified scheme and semester, and be active
4. **File**: Required for note upload
5. **Title**: Required field for the note

This hierarchical flow ensures proper academic structure and prevents users from selecting invalid subject combinations!
