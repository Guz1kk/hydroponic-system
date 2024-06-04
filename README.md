# Django API Project

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Project](#running-the-project)
- [API Documentation](#api-documentation)

## Installation

1. **Clone the repository:**

      git clone https://github.com/Guz1kk/hydroponic-system.git

      cd hydroponic-system

2. **Create and activate a virtual environment:**

      python -m venv venv

      source venv/bin/activate

3. **Install the dependencies:**

      pip install -r requirements.txt

## Configuration

1. **Edit .env file:**

2. **Set up the database:**

      python manage.py makemigrations

      python manage.py migrate

3. **Create superuser:**

      python manage.py createsuperuser


## Running the Project

1. **Start the development server:**

      python manage.py runserver

2. **Access the API:**

Open your web browser and go to http://127.0.0.1:8000/.

## API Documentation

1. **View the API documentation:**

Open your web browser and go to one of following links:

      'http://127.0.0.1:8000/swagger/'
      'http://127.0.0.1:8000/redoc/'
