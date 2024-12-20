## Article Management System - Readme

### Overview
This is an internal article management system designed for a media company. The system supports functionalities for journalists, editors, and administrators to create, edit, review, and publish articles. It also includes an API for integration with third-party platforms.

---

### Features

#### Part 1: Article Submission Form

**Form Fields:**

- **Page 1:**
  - Title (Text Field)
  - Subtitle (Text Field)
  - Article Content (Text Area)
  - Author Name (Text Field)
  - Email Address (Email Field)

- **Page 2:**
  - Article Image (File Upload)
  - Tags (Checkboxes for predefined tags: Politics, Sports, Tech, etc.)
  - Category (Dropdown: News, Opinion, Feature)
  - Publish Date (Date Field, must be a future date)
  - Agree to Terms (Checkbox)

**Custom Validation:**

- Title must be at least 10 characters long.
- Publish date must be a future date.
- Email field must have a valid format.
- Terms checkbox must be checked.

**Pagination:**
- Split the form into two pages with the ability to navigate between them without losing data.

**Error Handling:**
- User-friendly error messages for validation errors.

---

#### Part 2: Article Management System (Backend & API)

**Authentication:**
- User registration, login, and logout functionality.
- Password reset via email.
- Django's built-in authentication system.

**Authorization:**
- Roles:
  - **Journalist:** Submit and edit their own articles but cannot publish.
  - **Editor:** Review, approve, and publish articles.
  - **Admin:** Full access to create, edit, delete articles and manage users.
- Role-based permissions using Django’s permission system.

**CRUD Operations:**
- Create an `Article` model with fields: title, content, author, image, tags, category, and publish_date.
- Journalists can create and edit their own articles.
- Editors can approve, reject, or publish articles.
- Admins can manage articles and users.

**Django Rest Framework (DRF) API:**
- CRUD operations for the `Article` model.
- Token Authentication for API.
- Role-based access restrictions for API endpoints.
- Pagination, search, and filtering (e.g., filter by category, search by title).
- Email notifications for article submission, approval, or rejection.
- Public endpoint for retrieving published articles.

---

#### Additional Features

- **JWT Authentication:**
  - Implemented JWT-based authentication for API requests.

- **Views:**
  - Paginated list view of articles with filtering (by category, tags, and date).
  - Detailed view for each article (full content, image, author details, status).
  - Grid view for visual representation of articles.
  - Map view for geographic location-based articles (using Google Maps or OpenStreetMap).

- **Image Gallery:**
  - Multiple images can be uploaded for each article.

- **Location-based Search:**
  - Search articles within a geographic area using latitude and longitude coordinates.

- **Swagger API Documentation:**
  - Integrated Swagger (via `drf-yasg`) for API documentation.

- **Custom SQL Queries:**
  - Filter articles by categories, tags, publish date, or author name.

---

### How to Use

#### Create a Virtual Environment:
```bash
make env
```

#### Install Dependencies:
```bash
make install
```

#### Run the Development Server:
```bash
make run
```

#### Apply Migrations:
```bash
make migrate
```

#### Seed Database:
```bash
make seed
```

#### Run Tests:
```bash
make test
```

#### Build and Run Docker:
```bash
make build
make docker-run
```

---

This Makefile is aligned perfectly with the Django project directory structure to streamline development tasks.
