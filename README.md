
# Enterprise E-Commerce SDET Automation Platform

An e-commerce backend and test automation project demonstrating
REST API testing, authentication, database operations, reusable
automation utilities, and continuous integration.

## Project Goals

- Build a Flask-based e-commerce REST API.
- Implement product and order operations.
- Implement JWT-based authentication and role-based access control.
- Organize application logic into services and repositories.
- Build a reusable Python API client for automated tests.
- Validate API behavior, error handling, and database operations.
- Protect sensitive values in application logs.
- Execute automated tests through GitHub Actions.

## Technology Stack

- Python
- Flask
- SQLite
- Pytest
- Requests
- PyJWT
- JSON Schema
- Git and GitHub
- GitHub Actions

## Project Structure

```text
app/
  auth/             Authentication and authorization
  database/         Database connection and initialization
  errors/           Error response handling
  orders/           Order API routes
  products/         Product API routes
  repositories/     Database access
  services/         Business logic
  validators/       Request validation

config/             Environment-based configuration
framework/
  clients/          Reusable API client
  endpoints/        API endpoint helpers
  exceptions/       Custom API exceptions
  utilities/        Logging and sanitization helpers

schemas/            JSON schemas
test_data/          Test data
tests/
  api/              API tests
  framework/        Framework utility tests
  repository/       Repository tests
  service/          Service tests

.github/workflows/  GitHub Actions pipeline
run.py              Flask application entry point
requirements.txt    Python dependencies
```

## Prerequisites

- Python 3.14
- Git

## Setup on Windows PowerShell

Clone the repository:

```powershell
git clone https://github.com/azarcostark/Enterprise-E-Commerce-SDET-Automation-Platform.git
cd Enterprise-E-Commerce-SDET-Automation-Platform
```

Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Configure the JWT secret for the current terminal session:

```powershell
$env:JWT_SECRET = "replace-with-a-local-development-secret"
```

Initialize the database:

```powershell
python -m app.database.init_db
python -m app.database.migration_v3_orders
```

Start the API:

```powershell
python run.py
```

The API runs locally at:

`http://127.0.0.1:5000`

Health endpoint:

`GET http://127.0.0.1:5000/health`

## Running the Automated Tests

Keep the Flask API running in one terminal. In a second terminal,
activate the virtual environment and configure the same JWT secret.

Then run:

```powershell
python -m pytest -v
```

The current local regression baseline is **65 passing tests**.
Test results may change as the project evolves.

## Continuous Integration

The GitHub Actions workflow is located at:

`.github/workflows/tests.yml`

It installs dependencies, initializes the database, starts the API,
checks the health endpoint, and executes the automated test suite.

View workflow runs:

https://github.com/azarcostark/Enterprise-E-Commerce-SDET-Automation-Platform/actions

## Security Notes

- The JWT secret is read from an environment variable.
- Do not commit `.env` files or real credentials.
- Log sanitization masks configured sensitive fields.
- Use a strong, unique secret outside local development.

## Current Scope

This repository currently focuses on backend API functionality,
database access, authentication, reusable API automation utilities,
automated testing, and CI execution.

UI automation and Docker should be considered future work unless
and until their implementation is added and verified.
