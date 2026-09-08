# Receipt Management System (DM571)

University project in software engineering. A Flask web application
implementing a receipt reimbursement workflow: salesmen submit receipts,
accountants validate them, and managers give final approval or rejection.

Full report — requirements analysis, C4 diagrams, UML, test coverage and
API specification: [ReceiptSystemReport.pdf](ReceiptSystemReport.pdf)

## Workflow

    PENDING --(accountant validates)--> HANDLED --(manager decides)--> APPROVED
                                                                   \-> REJECTED

Four roles with distinct permissions:

| Role | Can do |
|---|---|
| Salesman | Submit receipts, view only their own |
| Accountant | View pending receipts, mark as handled |
| Manager | Approve or reject handled receipts, submit their own |
| Admin | Overview of all users, receipts and handling logs |

Managers cannot approve or reject their own receipts, a deliberate fraud
control enforced in the domain layer. Every state change is appended to the
receipt's handling log with a user ID and timestamp.

## Architecture

Three layers with clear separation:

- **Presentation** - Flask routes, Jinja templates
- **Application** - `UserApplication` and `ReceiptApplication` hold the
  business rules and state transitions
- **Data** - domain models, factories, in-memory storage

The Factory pattern (`UserFactory`, `ReceiptFactory`) centralises object
creation and validation; enums (`UserRole`, `ReceiptStatus`) keep internal
states type-safe.

Storage is in-memory by design, to keep the MVP simple. Data does not survive
a restart and the store is not thread-safe. A real deployment would swap the
data layer for PostgreSQL without touching the layers above it.

## Testing

Unit tests with pytest cover the domain and application layers: role
permissions, fraud rules and status transitions.

| Module | Coverage |
|---|---|
| models.py | 81% |
| user_application.py | 80% |
| receipt_application.py | 73% |
| Total | 56% |

Flask routes are deliberately untested at unit level.

    pytest
    pytest --cov

## Mobile API

An OpenAPI 3.2 specification was written for a future mobile client, designed
to Level 2 of the Richardson Maturity Model: resource URLs, correct HTTP
verbs, meaningful status codes and API-key authentication on every endpoint.
The API itself is not implemented.

## Running

    pip install flask
    python app.py

Then open http://localhost:5000. Demo accounts are seeded in `database.py`.

## Technologies
Python, Flask, Jinja, pytest, pytest-cov, OpenAPI


## Team
Karim Amin, Mohammad Amin, Jon Termkolli Gashi, Taaha Khan.
Report authorship is credited per section in Appendix A.

## Disclaimer
Developed for educational purposes as part of a university course.
