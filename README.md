# Blogging_api
Alx Capstone Project

# Django Blog API

## Overview

This project is a RESTful API for a blog platform built with Django and Django Rest Framework (DRF). It supports functionality like creating blog posts, managing categories and tags, searching posts, and more. The API is secured using authentication, and only authorized users can perform certain actions.

## Features

- **Blog Post Management:** Create, update, delete, and retrieve blog posts.
- **Category and Tag Management:** Manage categories and tags using Django REST framework viewsets.
- **Pagination:** Paginated responses for blog post lists.
- **Search and Filtering:** Search posts by title, content, tags, and author.
- **Custom Permissions:** Restrict actions based on user roles.
- **User Profiles:** Custom user model with additional fields such as bio and birthdate.

## Prerequisites

Ensure you have the following installed:

- Python (version 3.7 or above)
- Django (version 3.x or above)
- Django REST Framework (DRF)
- Django Filter
- MySQL or any preferred database (optional)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/blog-api.git
    ```

2. Navigate to the project directory:

    ```bash
    cd blog-api
    ```

3. Set up a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # For Windows, use `venv\Scripts\activate`
    ```

4. Install required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. Set up the database (if using MySQL, adjust settings in `settings.py`):

    ```bash
    python manage.py migrate
    ```

6. Create a superuser to access the Django admin interface:

    ```bash
    python manage.py createsuperuser
    ```

7. Run the development server:

    ```bash
    python manage.py runserver
    ```

## API Endpoints

### Blog Post Endpoints

- **List all posts:**
    - `GET /posts/`
    - Permissions: Public (read-only)
    - Query Params: `page`, `page_size`, `order=asc|desc`

- **Create a new post:**
    - `POST /posts/create/`
    - Permissions: Authenticated users
    - Body Params: `title`, `content`, `category`, `tags`

- **Retrieve post details:**
    - `GET /posts/<int:pk>/`
    - Permissions: Public (read-only)

- **Update a post:**
    - `PUT /posts/update/<int:pk>/`
    - Permissions: Authenticated and Author-only

- **Delete a post:**
    - `DELETE /posts/delete/<int:pk>/`
    - Permissions: Authenticated and Author-only

- **List posts by category:**
    - `GET /posts/category/<int:pk>/`
    - Permissions: Public (read-only)

- **List posts by author:**
    - `GET /posts/author/<int:pk>/`
    - Permissions: Public (read-only)

- **Search for posts:**
    - `GET /posts/search/?search=<query>`
    - Permissions: Public (read-only)

### Category and Tag Endpoints

- **List all categories:**
    - `GET /categories/`
    - Permissions: Public (read-only)

- **Create a new category:**
    - `POST /categories/`
    - Permissions: Authenticated (Admin or Author-only)

- **List all tags:**
    - `GET /tags/`
    - Permissions: Public (read-only)

- **Create a new tag:**
    - `POST /tags/`
    - Permissions: Authenticated (Admin or Author-only)

### Authentication Endpoints

- **Register a new user:**
    - `POST /register/`
    - Body Params: `username`, `password`, `email`, `birthdate`

- **Login:**
    - `POST /login/`
    - Body Params: `username`, `password`
