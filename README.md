# Task Management System

This full-stack project implements a task management system, consisting of a RESTful API backend with FastAPI (Python) and a SPA frontend with React (Vite). It was developed as part of a practical test, demonstrating skills in development, architecture, DevOps, and project management.

## Features

### Backend (RESTful API)
- Task Creation: Allows registering new tasks.
- Task Listing: Displays all registered tasks.
- Task Filtering: Filters tasks by status (pending, in progress, completed).
- Task Update: Changes the status and other details of a task.
- Task Deletion: Deletes existing tasks.
- Mocked Login: A simple login screen for demonstration purposes, without real JWT authentication.

### Frontend (Web Interface)
- Task Visualization: Displays the task list with filters.
- Task Creation: Form to add new tasks.
- Status Update: Allows changing a task's status.
- Task Deletion: Removes tasks from the list.
- Responsiveness: Interface adaptable to different screen sizes.

## Technologies Used

### Backend
- Python 3.12+
- FastAPI: High-performance web framework.
- Pydantic: For data validation and serialization.
- SQLAlchemy: ORM for database interaction.
- SQLite: Simple database for development and testing.
- Pytest: Framework for automated testing.
- Alembic: Database migration tool.

### Frontend
- React 18+: JavaScript library for building user interfaces.
- Vite: Fast frontend build tool.
- Axios: HTTP client for API communication.
- React Router DOM: For client-side navigation.
- Pure CSS / Tailwind CSS (optional): For styling.

### DevOps & Infrastructure
- Docker / Docker Compose: For containerization and orchestration of the development environment.
- GitHub Actions: For CI/CD automation (Tests, Linting, Image Building).
- Terraform: For Infrastructure as Code (IaC) on AWS (VPC, EC2, Security Group).

## How to Run the Project

This project can be run using Docker Compose for a consistent environment, or natively without Docker.

### General Prerequisites

- Git installed.

---

### Running with Docker (Recommended)

This project is containerized with Docker Compose, simplifying environment setup.

#### Prerequisites
- Docker Desktop installed and running.

#### Steps
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/mtfsantos/task-manager.git
    cd task-manager
    ```
2.  **Configure environment variables:**
    Create a `.env` file in the root of each directory (`backend/.env` and `frontend/.env`) based on the provided `.env.example` files, if necessary. For this project, default configurations via Docker Compose should be sufficient to start.

    Example `backend/.env` (not strictly required for default SQLite):
    ```properties
    DATABASE_URL="sqlite:///./sql_app.db"
    SECRET_KEY="your-super-secret-key" # For mocked login
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

    Example `frontend/.env` (not strictly required, `VITE_API_BASE_URL` is defined in `docker-compose.yml` for Docker network):
    ```properties
    VITE_API_BASE_URL=http://localhost:8000
    ```
3.  **Start the services with Docker Compose:**
    ```bash
    docker compose up --build
    ```
    This command will:
    - Build the Docker images for the backend and frontend.
    - Start the backend container (on port 8000) and the frontend container (on port 3000).

4.  **Access the Application:**
    - Frontend: `http://localhost:3000`
    - Backend API Docs (Swagger UI): `http://localhost:8000/docs`

### Running Locally (Without Docker)

You can run the backend and frontend services directly on your machine.

#### General Prerequisites
- Python 3.12+: [Download Python](https://www.python.org/downloads/)
- Node.js (LTS - v18+ recommended): [Download Node.js](https://nodejs.org/en/download/) (includes npm)

#### 1. Backend Setup and Execution

1.  **Navigate to the backend directory:**
    ```bash
    cd <your-project-root>/backend
    ```
2.  **Create and activate a virtual environment (recommended):**
    *   **On Windows:**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    *   **On macOS/Linux:**
        ```bash
        python -m venv venv
        source venv/bin/activate
        ```
3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Create the environment variables file (`.env`):**
    In the `backend/` directory, create a file named `.env` and copy the content from `backend/.env.example`.
    ```properties
    DATABASE_URL=sqlite:///./sql_app.db
    SECRET_KEY="your-super-secret-key-replace-me-in-production"
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```
5.  **Execute the FastAPI server:**
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ```
    The backend will typically run on `http://localhost:8000`. Access the API documentation at `http://localhost:8000/docs`.

#### 2. Frontend Setup and Execution

1.  **Open a new terminal** and navigate to the frontend directory:
    ```bash
    cd <your-project-root>/frontend
    ```
2.  **Install Node.js dependencies:**
    ```bash
    npm install
    ```
3.  **Create the environment variables file (`.env`):**
    In the `frontend/` directory, create a file named `.env` and copy the content from `frontend/.env.example`. Ensure `VITE_API_BASE_URL` points to your locally running backend.
    ```properties
    VITE_API_BASE_URL=http://localhost:8000
    ```
4.  **Execute the Vite development server:**
    ```bash
    npm run dev
    ```
    The frontend will typically run on `http://localhost:3000` or `http://localhost:5173`.

#### 3. Accessing the Application (Local)

1.  Ensure **both** the Backend and Frontend servers are running in separate terminals.
2.  Open your browser and navigate to the frontend address (e.g., `http://localhost:3000`).

---

### Mocked Login

To access the application functionalities, use the following credentials on the login screen:
- Username: `user`
- Password: `password`

## Database Migrations (Alembic)

Alembic is used to manage database schema changes over time.

### Setup

1.  **Install Alembic:**
    Make sure your Python virtual environment is active in the `backend` directory.
    ```bash
    pip install alembic
    ```

2.  **Initialize Alembic:**
    This creates the `alembic` directory and `alembic.ini` file in your `backend` root.
    ```bash
    alembic init alembic
    ```

3.  **Configure `alembic/env.py`:**
    This file defines how Alembic connects to your database and identifies your SQLAlchemy models.
    -   Ensure `sys.path` includes the `backend` root to allow imports like `app.db.base` and `app.core.config`.
    -   Set `target_metadata = Base.metadata` to link Alembic to your SQLAlchemy models.
    -   **Important:** Modify `run_migrations_offline()` and `run_migrations_online()` to get the database URL from your application's `settings` (e.g., `settings.DATABASE_URL`), ensuring consistency with your FastAPI application's database configuration. This typically involves importing `settings` from `app.core.config`.

4.  **Remove `Base.metadata.create_all()`:**
    Remove the `Base.metadata.create_all(bind=engine)` call from `backend/app/main.py`'s `lifespan` function. Alembic will now handle schema creation and updates.

### Usage

All Alembic commands should be run from the `backend` directory with your Python virtual environment activated.

1.  **Generate a new migration:**
    This command compares your current SQLAlchemy models with the database schema and generates a new migration script if differences are found.
    ```bash
    alembic revision --autogenerate -m "Description of your changes"
    ```
    A new file will be created in `alembic/versions/`. Review its contents before applying.

2.  **Apply migrations:**
    This command applies all pending migrations to your database.
    ```bash
    alembic upgrade head
    ```
    `head` refers to the latest revision available in your `alembic/versions` directory.

3.  **Check current database revision:**
    Shows the identifier of the last migration applied to your database.
    ```bash
    alembic current
    ```

4.  **View migration history:**
    Displays the history of all migration scripts available.
    ```bash
    alembic history
    ```

5.  **Check for pending schema changes:**
    This command checks if there are differences between your models and the current database schema without generating a migration file. It exits with a non-zero code if changes are detected, useful for CI/CD pipelines.
    ```bash
    alembic check
    ```

---

## Running Tests

### Backend
To run the backend tests (using `pytest`):

```bash
cd backend
source venv/bin/activate # or .\venv\Scripts\activate
python3 -m pytest tests
```

## Deployment (AWS via Terraform)

Example Terraform configuration to provision resources.

### Prerequisites

- AWS account configured.
- AWS CLI configured with credentials.
- Terraform CLI installed.

### Steps

1.  **Navigate to the Terraform directory:**
    ```bash
    cd infra/aws
    ```
2.  **Initialize Terraform:**
    ```bash
    terraform init
    ```
3.  **Plan the infrastructure:**
    ```bash
    terraform plan
    ```
    This will show what will be created. Make sure to replace `your-key-pair` in `main.tf` and `variables.tf` with the name of an existing EC2 key pair in your account.
4.  **Apply the infrastructure:**
    ```bash
    terraform apply --auto-approve
    ```
    After application, the public IP of the EC2 instance will be displayed. You would then need to SSH into the instance and configure the deployment of the containers (e.g., `git clone` and `docker compose up`).

Warning: This Terraform setup is a basic example and does not include advanced security considerations or high availability for a production environment.

## Additional Documentation

- [Architecture](docs/Architecture.md): Details technical decisions, justifications, and proposals for evolution and scalability.
- [Team Task Distribution](docs/Team_Task_Distribution.md): Simulation of how the development of this project could be organized among a team of developers.