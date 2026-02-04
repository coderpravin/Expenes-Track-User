# Expenses Machine - Expense Tracker

This is a Django-based Expense Tracker application designed to help users track their expenses, generate reports, and visualize their spending over time. It supports asynchronous tasks using Celery and Redis.

## Project Structure

The project is structured as follows:

-   **`project/`**: Main Django project configuration (`settings.py`, `urls.py`, etc.).
-   **`expenses/`**: App for managing expenses.
-   **`timeline/`**: App for timeline visualization.
-   **`templates/`**: HTML templates for the frontend.
-   **`static/`**: Static files (CSS, JS, Images).
-   **`manage.py`**: Django's command-line utility.

## Prerequisites

Before running the project, ensure you have the following installed:

1.  **Python 3.10+**: [Download Python](https://www.python.org/downloads/)
2.  **Redis**: Required for Celery (Async tasks).
    -   **Windows**: [Memurai](https://www.memurai.com/) (Redis-compatible) or run Redis via WSL/Docker.
    -   **Linux/Mac**: Install via your package manager (e.g., `sudo apt install redis-server`).

## Installation & Setup

1.  **Clone the repository** (if you haven't already):
    ```bash
    git clone https://github.com/yourusername/ExpenseTracker_Mech.git
    cd ExpenseTracker_Mech/Expenes-Track-User
    ```

2.  **Create a Virtual Environment**:
    It is recommended to use a virtual environment to manage dependencies.
    ```bash
    python -m venv venv
    ```

3.  **Activate the Virtual Environment**:
    -   **Windows (Command Prompt)**:
        ```cmd
        venv\Scripts\activate
        ```
    -   **Windows (PowerShell)**:
        ```powershell
        .\venv\Scripts\Activate.ps1
        ```
    -   **Mac/Linux**:
        ```bash
        source venv/bin/activate
        ```

4.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Environment Variables**:
    Create a `.env` file in the `project/` directory (next to `settings.py`) or in the root `Expenes-Track-User` directory (depending on how you want to manage it, but settings loads from `BASE_DIR / ".env"` which is the `project` inner folder's parent).
    
    The code looks for `.env` in `Expenes-Track-User/project/`.
    
    Add the following variables to `.env`:
    ```ini
    EMAIL_HOST_USER=your_email@gmail.com
    EMAIL_HOST_PASSWORD=your_app_specific_password
    # Add other keys if necessary (e.g., SECRET_KEY, DEBUG)
    ```

6.  **Apply Migrations**:
    Initialize the database (SQLite by default).
    ```bash
    cd project
    python manage.py migrate
    ```

7.  **Create a Superuser** (Optional, for Admin access):
    ```bash
    python manage.py createsuperuser
    ```

## Running the Application

To run the full application, you need to run three separate processes (terminals):

1.  **Start Redis Server**:
    Ensure your Redis server is running.
    -   **Windows**: If installed as a service, it might be running already. Verify with `redis-cli ping`.

2.  **Start Django Development Server**:
    In your first terminal (with venv activated):
    ```bash
    cd project
    python manage.py runserver
    ```
    Access the app at: `http://127.0.0.1:8000/`

3.  **Start Celery Worker**:
    In a second terminal (with venv activated):
    This processes background tasks (e.g., email sending, report generation).
    ```bash
    cd project
    celery -A project worker -l info
    ```
    *Note: On Windows, you might need to use `celery -A project worker --pool=solaris -l info` or `--pool=solo` if the default prefork pool has issues.*

## Features

-   **Dashboard**: Overview of expenses.
-   **Add Expense**: Log daily expenses with categories.
-   **Timeline**: Visualize spending history.
-   **Reports**: Export data to CSV/PDF (powered by `openpyxl` and `xhtml2pdf`).
-   **Email Notifications**: Async email alerts via Celery.

## Troubleshooting

-   **Redis Connection Error**: Ensure Redis is installed and running on `localhost:6379`.
-   **Celery Issues on Windows**: If Celery doesn't process tasks, try running with `-P solo`:
    ```bash
    celery -A project worker -l info -P solo
    ```