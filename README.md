# VCLab-BE

## **VCLab** (DRF)

Welcome to the VCLab API repository! This document provides essential information for onboarding and development.

## Getting Started

### Prerequisites

Before you begin, ensure you have this version of python installed in your local machine.

- python3.9.0+

### Features

- Token based authentication and authorization using JSON Web Token (JWT).

### Installation

Clone the project

```bash
  git clone https://github.com/ooplaza/VCLab-BE.git
```

Go to the project directory

```bash
  cd <Project_Name>
```

Install and create a separate working environment

```bash
  pip install virtualenv
```

```bash
  python -m virtualenv "environment_name"
```

Activate the environment

```bash
  environment_name/Scripts/Activate.ps1
```

Install dependencies

```bash
  pip install -r requirements.txt
```

### Development

#### Running the Development Server

Run the migration command

```bash
  python manage.py migrate
```

Create an admin account by providing the following requirements

```bash
  python manage.py createsuperuser
```

Start the server

```bash
  python manage.py runserver
```

The API documentation be accessible at http://localhost:8000/

### **API Base Endpoint**

http://localhost:8000/api/

### **API Documentation**

http://localhost:8000

### Testing

Running the test command to generate a report

```bash
  coverage run --omit="*/venv/*" manage.py test
```

Terminal based test report

```bash
  python -m coverage report
```

UI version of test report

```bash
  coverage html
```
