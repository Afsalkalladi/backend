<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# EESA Backend - Copilot Instructions

This is a Django REST API backend for the Electrical Engineering Students Association (EESA) at CUSAT. Here are the key guidelines for development:

## 🏗️ Architecture Guidelines

### Role-Based Access Control

- Always implement proper role-based permissions using the custom permission classes in `accounts/permissions.py`
- 5 user roles: Student, Teacher, Technical Head, Admin, Alumni
- Use `@permission_classes` decorator for all views

### Academic Structure

- Follow the hierarchical structure: **Scheme → Semester → Subject**
- When implementing subject-related features, always require scheme and semester selection first
- Students must be filterable by scheme and year of joining

### Data Models

- Use the custom User model from `accounts.models.User`
- Follow the established naming conventions for models and fields
- Implement proper `__str__` methods for all models

## 🔒 Security Best Practices

### Authentication

- Use JWT authentication (SimpleJWT)
- Implement proper token refresh mechanisms
- Always validate user permissions in views

### Data Validation

- Use DRF serializers for all API endpoints
- Implement proper field validation
- Handle file uploads securely in the media directory

## 📝 API Development

### Serializers

- Create separate serializers for different use cases (Create, Update, List, Detail)
- Use nested serializers for related data when appropriate
- Implement proper validation methods

### Views

- Use function-based views with decorators for consistency
- Return consistent response formats with proper status codes
- Include meaningful error messages

### URL Patterns

- Follow RESTful conventions
- Use descriptive URL names
- Group related endpoints logically

## 🗄️ Database Guidelines

### Models

- Use proper field types and constraints
- Implement database indexes for frequently queried fields
- Use `auto_now_add` and `auto_now` for timestamp fields

### Migrations

- Always create migrations for model changes
- Name migrations descriptively
- Test migrations on sample data

## 📚 Feature-Specific Guidelines

### Note Sharing System

- Notes require approval from Teachers, Admins, or Student Reviewers
- Implement the `can_be_approved_by()` method logic correctly
- Handle file uploads with proper path structure

### Student Management

- Auto-calculate year of study based on semester
- Implement bulk operations for semester promotion
- Maintain academic year groupings

### Reviewer System

- One reviewer per scheme+year combination
- Reviewers can only approve notes from their assigned year
- Implement proper assignment/deactivation logic

### Project Portal

- Allow project creators to edit their own projects
- Support team member management
- Implement proper category filtering

### Event Management

- Only Admins and Technical Heads can create events
- Support upcoming events ticker functionality
- Handle timezone considerations

## 🧪 Testing & Development

### Sample Data

- Use management commands for creating test data
- Follow the existing patterns in `create_sample_data.py`
- Create realistic sample scenarios

### Error Handling

- Return appropriate HTTP status codes
- Provide clear error messages
- Handle edge cases gracefully

## 📦 Code Organization

### File Structure

- Keep related functionality in appropriate apps
- Use consistent naming for serializers, views, and URLs
- Implement admin interfaces for all models

### Documentation

- Document complex business logic
- Use docstrings for all classes and methods
- Keep README.md updated with new features

## 🚀 Performance Considerations

### Database Optimization

- Use `select_related()` and `prefetch_related()` appropriately
- Implement database indexes for filtering fields
- Consider pagination for large datasets

### API Efficiency

- Return only necessary data in list views
- Implement proper filtering and search
- Use appropriate serializers for different contexts

Remember to maintain consistency with the existing codebase and follow Django/DRF best practices throughout development.
