# NOIR

A premium, visually driven social platform for creative professionals.

## Prerequisites

- Python 3.10+
- Django 5.2+

## Setup & Running Locally

1. **Activate the virtual environment** (Windows PowerShell):
   ```powershell
   .\venv\Scripts\activate
   ```

2. **Run migrations** (if you haven't already):
   ```powershell
   python manage.py migrate
   ```

3. **Seed the database** with demo content (optional but recommended):
   ```powershell
   python manage.py seed_demo
   ```

4. **Create a superuser** (for admin access):
   ```powershell
   python manage.py createsuperuser
   ```

5. **Start the development server**:
   ```powershell
   python manage.py runserver 8000
   ```
   *(We are currently running it on port 8002 for you).*

## Accessing the Platform
- **Main Platform:** [http://localhost:8000](http://localhost:8000) (or whichever port you started it on).
- **Django Admin:** [http://localhost:8000/admin](http://localhost:8000/admin)

*(To log in immediately, you can use the admin credentials you created, or one of the seeded demo users, e.g., Username: `alexmorrow`, Password: `password123`)*
