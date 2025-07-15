# 🔰 EESA Backend - Phase 1

**Electrical Engineering Students Association (EESA) Backend API** - A comprehensive Django REST API backend for CUSAT EESA website with role-based access control, note sharing, project portal, and event management.

## 🚀 Features

### 👥 User Management & Authentication

- **5 User Roles**: Student, Teacher, Technical Head, Admin, Alumni
- **JWT Authentication** with access & refresh tokens
- **Role-based permissions** for all endpoints
- Custom user model with additional fields for alumni

### 📚 Academic Structure

- **Hierarchical Subject System**: Scheme → Semester → Subject
- **Student Management**: Full academic information with auto-calculated year of study
- **Bulk Operations**: Semester promotion with auto year-of-study updates

### 📝 Note Sharing System

- Students upload notes for specific subjects
- **Multi-level Approval System**:
  - Teachers can approve any note
  - Student reviewers can approve notes from their assigned year
  - Admins can approve any note
- Notes stay verified permanently once approved

### 🧪 Reviewer System

- Technical Heads assign **one student reviewer per academic year**
- Reviewers can only verify notes from students of the **same year**
- Integrated with scheme and year filtering

### 💼 Project Portal

- Students submit projects with team information
- **Categories**: Web Development, Mobile App, ML, IoT, Robotics, etc.
- Project creators can edit their projects anytime
- Team members with LinkedIn integration

### 📅 Event Management

- Admins/Technical Heads post EESA events
- Events display on homepage as scrolling ticker
- Comprehensive event scheduling with venue information

## 🛠️ Technology Stack

- **Backend**: Django 5.2.4 + Django REST Framework
- **Authentication**: JWT (Simple JWT)
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **File Storage**: Local storage with media handling
- **API Documentation**: Built-in DRF browsable API

## 📦 Installation & Setup

### Prerequisites

- Python 3.8+
- Virtual environment support

### 1. Clone & Setup

```bash
# Clone the repository
git clone <repository-url>
cd eesa

# Virtual environment is already configured
# Activate it if needed:
source .venv/bin/activate  # On macOS/Linux
# .venv\Scripts\activate   # On Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your settings
nano .env
```

### 4. Database Setup

```bash
# Apply migrations
python manage.py migrate

# Create sample data (optional)
python manage.py create_sample_data
python manage.py create_sample_subjects
```

### 5. Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## 🔑 API Endpoints

### Authentication

```
POST /api/auth/register/          # User registration
POST /api/auth/login/             # User login
GET  /api/auth/profile/           # Get user profile
PUT  /api/auth/profile/update/    # Update profile
POST /api/auth/token/refresh/     # Refresh JWT token
```

### Student Management

```
GET  /api/students/                    # List students (filtered by scheme/year)
GET  /api/students/<id>/               # Student details
PUT  /api/students/<id>/update/        # Update student (admin/tech_head)
POST /api/students/bulk-promote/       # Bulk semester promotion
GET  /api/students/my-profile/         # Current student's profile
```

### Reviewer Management

```
GET  /api/students/reviewers/          # List active reviewers
POST /api/students/reviewers/assign/   # Assign reviewer
DEL  /api/students/reviewers/<id>/remove/  # Remove reviewer
```

### Academic System

```
GET  /api/academics/upload/schemes/       # Get available schemes & semesters
GET  /api/academics/upload/subjects/      # Get subjects by scheme & semester
GET  /api/academics/subjects/             # Get subjects by scheme & semester
POST /api/academics/subjects/create/      # Create subject (admin/tech_head)
GET  /api/academics/notes/                # List notes (with filtering)
POST /api/academics/notes/upload/         # Upload note (hierarchical flow)
POST /api/academics/notes/approve/        # Approve note
GET  /api/academics/notes/my/             # Current user's notes
GET  /api/academics/notes/pending/        # Pending approval notes
DEL  /api/academics/notes/<id>/delete/    # Delete note
```

### Project Portal

```
GET  /api/projects/              # List projects
GET  /api/projects/<id>/         # Project details
POST /api/projects/create/       # Create project
PUT  /api/projects/<id>/update/  # Update project (creator only)
DEL  /api/projects/<id>/delete/  # Delete project
GET  /api/projects/my/           # Current user's projects
GET  /api/projects/featured/     # Featured projects (homepage)
```

### Event Management

```
GET  /api/events/              # List events
GET  /api/events/<id>/         # Event details
POST /api/events/create/       # Create event (admin/tech_head)
PUT  /api/events/<id>/update/  # Update event
DEL  /api/events/<id>/delete/  # Delete event
GET  /api/events/upcoming/     # Upcoming events (ticker)
GET  /api/events/my/           # Current user's events
```

## 👥 Sample Users

After running `create_sample_data`:

| Username  | Password   | Role           | Description                   |
| --------- | ---------- | -------------- | ----------------------------- |
| admin     | admin123   | Admin          | Full system access            |
| tech_head | tech123    | Technical Head | Student & reviewer management |
| teacher1  | teacher123 | Teacher        | Note approval rights          |
| student1  | student123 | Student        | Alice Johnson (S2021, Sem 6)  |
| student2  | student123 | Student        | Bob Smith (S2021, Sem 6)      |
| student3  | student123 | Student        | Charlie Brown (S2022, Sem 4)  |
| student4  | student123 | Student        | Diana Prince (S2023, Sem 2)   |
| alumni1   | alumni123  | Alumni         | John Graduate (2020 passout)  |

## 🔒 Permission System

### Role Hierarchy

- **Admin**: Full access to everything
- **Technical Head**: Student management, reviewer assignment, event management
- **Teacher**: Note approval, student viewing
- **Student**: Note upload, project creation, profile management
- **Alumni**: Profile management, viewing capabilities

### Key Permission Rules

1. **Student Listing**: Only Teachers, Technical Heads, and Admins
2. **Note Approval**: Teachers, Admins, and assigned Student Reviewers
3. **Bulk Operations**: Only Admins and Technical Heads
4. **Event Creation**: Only Admins and Technical Heads
5. **Project Editing**: Only project creators (and Admins for deletion)

## 🗂️ Database Schema

### Core Models

- **User**: Custom user model with role-based fields
- **Student**: Academic information linked to User
- **Subject**: Hierarchical structure (Scheme → Semester → Subject)
- **Note**: File uploads with approval workflow
- **Project**: Student projects with team information
- **Event**: EESA event management
- **Reviewer**: Student reviewer assignments

### Key Relationships

- User → Student (OneToOne)
- Student → Reviewer (ForeignKey)
- Subject → Note (ForeignKey)
- User → Project (ForeignKey as creator)
- Project → TeamMember (ForeignKey)
- User → Event (ForeignKey as creator)

## 🔧 Management Commands

```bash
# Create sample data
python manage.py create_sample_data

# Create sample subjects
python manage.py create_sample_subjects

# Create superuser
python manage.py createsuperuser
```

## 📁 Project Structure

```
eesa/
├── accounts/           # User management & authentication
├── academics/          # Subjects & notes system
├── events/            # Event management
├── projects/          # Project portal
├── students/          # Student & reviewer management
├── eesa_backend/      # Main Django settings
├── media/             # Uploaded files
├── requirements.txt   # Python dependencies
├── manage.py         # Django management script
└── README.md         # This file
```

## 🚀 Production Deployment

### Environment Variables

```bash
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@localhost:5432/eesa_db
```

### Static Files

```bash
python manage.py collectstatic
```

### Database Migration

```bash
python manage.py migrate
```

## 🎯 Phase 2 Plans

- Email notifications for note approvals
- Advanced search and filtering
- File type validation and virus scanning
- API rate limiting
- Caching implementation
- Comprehensive logging and monitoring
- Mobile app API optimizations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For technical support or feature requests, contact the EESA technical team.

---

**Built with ❤️ for CUSAT Electrical Engineering Students Association**
