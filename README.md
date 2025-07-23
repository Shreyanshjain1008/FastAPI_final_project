# FastAPI API with JWT Authentication & Roles

A robust REST API built with Python and FastAPI. It demonstrates a complete CRUD implementation for managing users, with data persisted in a SQL database and secured by JWT-based authentication and role-based access control.

## ✨ Features

-   **FastAPI**: High-performance, asynchronous web framework.
-   **JWT Authentication**: Secure user login and session management.
-   **Password Hashing**: Uses `bcrypt` to securely store user passwords.
-   **Role-Based Access Control (RBAC)**: Differentiates between `user` and `admin` roles to protect specific endpoints.
-   **SQLAlchemy ORM**: Powerful database interaction and modeling.
-   **Alembic Migrations**: Manages database schema changes safely.
-   **Pydantic**: Handles data validation and settings management from `.env` files.
-   **Redis Caching**: Caches frequently accessed data to improve performance.

---

## 🚀 Setup and Run

Follow these steps to get the application running locally.

1. Prerequisites
- Python 3.8+
- Docker (for running Redis) or a local Redis installation.

2. Clone the Repository

3. Create and Activate a Virtual Environment

4. Install Dependencies

5. Start Redis

6. Set Up the Database
Run the Alembic migration command to create the database and all tables.

7. Run the Application

8. The API is now live and accessible at http://127.0.0.1:8000

⚙️ API Endpoints
Test all endpoints through the interactive Swagger UI at http://127.0.0.1:8000/docs.

Method	Path	            Description	                            Authentication
POST	/register	        Create a new user account.	            Public
POST	/token	            Log in to get a JWT access token.	    Public
GET	    /users/me/	        Get the profile of the current user.	Required
GET	    /users/	            Retrieve a list of all users. (Cached)	Admin Only
PUT	    /users/{user_id}	Update an existing user.	            Admin Only
DELETE	/users/{user_id}	Delete a user by ID.	                Admin Only