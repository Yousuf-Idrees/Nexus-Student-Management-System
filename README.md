# Nexus Premium: Intelligent Student Management System

Nexus Premium is a full-stack student management application built with Python, Streamlit, and MySQL. It combines object-oriented database abstractions, role-based access control (RBAC) with SHA-256 hashed credentials, interactive analytical dashboards, bulk CSV data processing, and a natural language query chatbot.

---

## Key Features

- **Role-Based Authentication (RBAC):** Separate access controls for administrators (Full CRUD, Bulk CSV, System Settings) and standard users (Read-Only Directory, Chatbot Access).
- **Glassmorphism UI/UX:** Styled using custom CSS, animations, metric badges, and interactive components.
- **Full Database CRUD Operations:** Parameterized MySQL queries preventing SQL injection during record insertion, lookup, updates, and deletion.
- **Bulk CSV Batch Import:** Ingest student records directly from CSV files via `csv.DictReader`.
- **Conversational AI Assistant:** Rule-based natural language processor (`Chatbot.py`) enabling conversational inquiries about student counts, list filtering, and specific record retrieval.
- **Analytics Dashboard:** Live system health indicators, total enrollments, average student age calculations, and top academic grade distributions using Pandas.

---

## Application Architecture

```text
Streamlit Dashboard (app.py)
   │
   ├── Role Authentication ──> credentials.json / users.json (SHA-256)
   │
   ├── Object Model ─────────> student.py (Student Class)
   │
   ├── Database Layer ───────> Database.py (MySQL Connector + Parameterized Queries)
   │
   └── AI Query Engine ──────> Chatbot.py (Regex & Rule-Based Intent Parser)

File Structure:

.
├── app.py              # Main Streamlit web application & UI layouts
├── Database.py         # MySQL connection manager & parameterized CRUD operations
├── Chatbot.py          # Rule-based natural language assistant module
├── student.py          # Student object entity model
├── credentials.json    # Hashed administrator credentials
├── users.json          # Persistent user account registry
├── students.csv        # Sample CSV batch import file
└── README.md           # Project documentation

Database Schema (MySQL)
Create the required database and table structure before running the application:

CREATE DATABASE IF NOT EXISTS Students_db;
USE Students_db;

CREATE TABLE IF NOT EXISTS Students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    grade VARCHAR(10) NOT NULL
);

Installation & Setup:

1. Prerequisites:
Python 3.9+
MySQL Server running locally on port 3306

2. Clone Repository:
git clone [https://github.com/YourUsername/Nexus-Student-Management.git](https://github.com/YourUsername/Nexus-Student-Management.git)
cd Nexus-Student-Management

3. Install Dependencies:
pip install streamlit mysql-connector-python pandas

4. Database Configuration
Ensure MySQL is running locally. Update connection credentials in Database.py if your database user or password differs from default settings:
# Database.py
def __init__(self, host='localhost', user='root', password='', database='Students_db'):
    ...



Running the Application
Launch the Streamlit web server:
streamlit run app.py
