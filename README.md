# Hospital Appointment Booking System

**A full-stack, database-driven web application for managing hospital appointments, featuring role-based access control for Admins, Doctors, and Patients.**

---

**Live Application URL:** **[https://hospital-appointment-system1-rdqx.onrender.com](https://hospital-appointment-system1-rdqx.onrender.com)**

## Overview

This project is a complete and secure web platform built from the ground up using Python and the Flask framework. It provides a seamless experience for patients to book appointments with available doctors, for doctors to manage their schedules, and for administrators to have a complete overview of the system's operations. The application is designed with a professional, scalable architecture, features a stunning and fully animated user interface, and is deployed live on the internet using modern cloud-hosting practices.

## Key Features

This application demonstrates a wide range of modern web development concepts and includes a full suite of features:

#### 1. Role-Based Access Control (RBAC)
* **Three Distinct User Roles:** The system securely manages three types of users:
    * **Patient:** The standard user who can register, log in, and book appointments.
    * **Doctor:** A promoted user who has a private dashboard to view appointments assigned to them.
    * **Admin:** A superuser with full system oversight, including the ability to manage user roles and view all appointments.
* **Secure Dashboards:** Each role is automatically redirected to their own specific dashboard upon login.
* **Protected Routes:** Custom security decorators (`@admin_required`, `@doctor_required`) prevent users from accessing pages they are not authorized to see, even if they type the URL manually.

#### 2. Complete User Authentication & Management
* **Secure Registration:** New users can create an account, with backend validation to prevent duplicate usernames or emails.
* **Authentication System:** Secure login and session management using Flask-Login, with hashed passwords that are never stored in plain text.
* **Password Reset Functionality:** A full "Forgot Password" workflow that sends a secure, timed token to the user's registered email.
* **Profile Deletion:** Users have the ability to permanently delete their own accounts and all associated data.
* **Admin User Management:** A dedicated admin page to view all registered users and promote them to the 'doctor' role.

#### 3. Dynamic Appointment System
* **Patient Booking:** Patients can book appointments by selecting a reason, a specific doctor from a dynamic list, and a future date and time.
* **Data Validation:** The backend prevents users from booking appointments in the past.
* **Personalized Schedules:** Dashboards for patients and doctors show only the appointments relevant to them.
* **Appointment Deletion:** Both patients and admins can delete appointments with a confirmation step.

#### 4. Stunning & Modern User Interface
* **Fully Animated UI:** The authentication pages feature a floating, frosted-glass design with dynamic, color-shifting backgrounds and animated, drifting "blobs."
* **Interactive Forms:** All forms provide instant success or error feedback without requiring a page reload, using modern JavaScript (`fetch` API).
* **Consistent Design:** A single, master stylesheet ensures a polished and consistent look and feel across all pages of the application.

## Technology Stack

This project leverages a modern, professional technology stack:

* **Backend:** Python 3, Flask, Gunicorn
* **Database:** PostgreSQL (for production), SQLite (for local development)
* **Database Connectivity (ORM):** Flask-SQLAlchemy
* **Frontend:** HTML5, CSS3, "Vanilla" JavaScript
* **Authentication:** Flask-Login, Werkzeug (for password hashing)
* **Email & Tokens:** Flask-Mail, itsdangerous
* **Deployment:** Render (Cloud Hosting), Git & GitHub (Version Control)

## Database Design: A Relational Model

The heart of the application is a **relational PostgreSQL database**, designed for efficiency and data integrity.



The database consists of two main tables linked by Foreign Keys, demonstrating a classic **one-to-many** relationship structure.

#### `user` Table
This table is the master roster for every person in the system.
| Column        | Type          | Constraints                   |
| :------------ | :------------ | :---------------------------- |
| `id`          | Integer       | **Primary Key** |
| `role`        | String        | Not Null, Default: 'patient'  |
| `username`    | String        | Not Null, Unique              |
| `email`       | String        | Not Null, Unique              |
| `password_hash`| String        | Not Null                      |

#### `appointment` Table
This table stores every appointment and links back to the `user` table twice.
| Column        | Type          | Constraints                       |
| :------------ | :------------ | :-------------------------------- |
| `id`          | Integer       | **Primary Key** |
| `title`       | String        | Not Null                          |
| `date`        | DateTime      | Not Null                          |
| `user_id`     | Integer       | **Foreign Key** (to `user.id`)    |
| `doctor_id`   | Integer       | **Foreign Key** (to `user.id`)    |

The connection between these tables is managed by **SQLAlchemy**, a powerful Object-Relational Mapper (ORM). This allows for clean, safe, and readable Python code (e.g., `appointment.booker.username`) to navigate the complex relationships without writing raw SQL.

## Local Development Setup

To run this project on your local machine, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/ompop-pro21/hospital-appointment-system1.git](https://github.com/ompop-pro21/hospital-appointment-system1.git)
    cd hospital-appointment-system1
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    .venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Create a `.env` file** in the root directory and add your local secrets:
    ```
    SECRET_KEY='a_long_and_random_secret_key'
    MAIL_USERNAME='your_email@gmail.com'
    MAIL_PASSWORD='your_16_character_google_app_password'
    MAIL_DEFAULT_SENDER='your_email@gmail.com'
    ```
5.  **Initialize the local database and create the first admin user:**
    ```bash
    flask seed-db
    ```
6.  **Run the application:**
    ```bash
    python run.py
    ```
    The application will be available at `http://127.0.0.1:5000`.

## Deployment

This application is configured for professional deployment on cloud platforms like Render.
* **Production Server:** Uses **Gunicorn**, a robust WSGI server.
* **Persistent Database:** Connects to a managed **PostgreSQL** database.
* **Secure Configuration:** All secrets (like database URLs and email passwords) are managed securely through **Environment Variables** and are never exposed in the source code, thanks to the `.gitignore` and `.env` setup.
* **Automated Builds:** The `Build Command` on Render (`pip install -r requirements.txt`) ensures a clean and reproducible environment for every deployment.

---

