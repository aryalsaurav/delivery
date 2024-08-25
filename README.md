# Delivery System

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.10
- pip
- Virtualenv (optional but recommended)


## Setup
### 1. Clone the repo from https://github.com/aryalsaurav/delivery.git
### 2. Create a virtualenv and install the requirements from requirements.txt file
  - python3.10 -m venv env
  - source env/bin/activate
  - pip install -r requirements.txt

### 3. Create file name .env and have
  DB_NAME,
  DB_USER,
  DB_PASSWORD,
  DB_PORT,
  DB_HOST,

### 4. Apply database migration: python manage.py migrate

### 5. Create superuser: python manage.py createsuperuser

### 6. Run server: python manage.py runserver
