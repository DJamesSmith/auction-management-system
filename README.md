
# Auction Management System

A web-based auction platform built with **Python, Django, Django REST Framework, and PostgreSQL**. The system enables registered users to create auction listings, browse items, place bids, and view auction results. Administrators manage users, categories, auction approvals, bids, and transaction records.

## Features

- **User Management:** Registration, authentication, profile management, password change, and password reset.
- **Role-Based Access Control:** Separate permissions for administrators and general users.
- **Auction Management:** Create, edit, cancel, and manage auction listings with images, categories, pricing, and schedules.
- **Auction Approval:** Administrative approval or rejection of submitted listings.
- **Auction Discovery:** Browse auctions, search by item name, and filter by category.
- **Bidding System:** Validated bids, minimum bid increments, and bid history.
- **Winner Identification:** Identify the highest valid bidder when an auction closes.
- **Transaction Management:** Maintain transaction records for completed auctions.
- **User Dashboard:** Track personal auctions, bids, winning auctions, and profile information.
- **Admin Dashboard:** Monitor users, auctions, active listings, completed auctions, and bids.

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, Django |
| REST API | Django REST Framework |
| Database | PostgreSQL |
| Database Access | Django ORM |
| Authentication | Django Authentication or JWT |
| Frontend | HTML, CSS, Bootstrap or React |

## Auction Workflow

1. User registration and login.
2. Auction listing creation.
3. Administrative review and approval.
4. Auction activation according to its schedule.
5. Bidding by eligible registered users.
6. Auction closure and winner identification.
7. Transaction record creation and completion.

## Getting Started

### Prerequisites

- Python
- PostgreSQL
- Git

### Installation

**1. Clone the repository**

```bash
git clone <repository-url>
cd <repository-directory>
```

**2. Create and activate a virtual environment**

```bash
python -m venv <env_name>
source <env_name>/bin/activate
```

On Windows:

```powershell
.venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure the database**

Create a PostgreSQL database and configure the required database credentials and environment variables according to the project settings. Keep sensitive credentials in a local `.env` file if supported, and never commit secrets to version control.

**5. Apply database migrations**

```bash
python manage.py migrate
```

**6. Create an administrator account**

```bash
python manage.py createsuperuser
```

**7. Start the development server**

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## Security and Data Integrity

The system is designed to enforce backend authorization, validate auction and bidding operations, securely hash passwords, and use database transactions or locking where necessary to handle concurrent bids safely.

## Project Scope

The initial release focuses on the core auction lifecycle, bidding, winner identification, and transaction records.

The following features are outside the initial scope:

- Online payment gateway integration
- Shipping and delivery management
- Ratings and reviews
- Complex notification systems
- Advanced reporting

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

Copyright (c) 2026 Tathagata Das and Dion James Smith