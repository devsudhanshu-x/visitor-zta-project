# Zero-Trust Visitor Identity and Just-in-Time Access Management Platform

A secure web-based visitor management platform designed around **Zero-Trust security principles**, providing controlled visitor identity management, authentication, authorization, policy-based access control, and just-in-time access.

---

## 📌 Project Overview

The **Zero-Trust Visitor Identity and Just-in-Time Access Management Platform** is a team-based web application developed using **Python and Flask** with an **Oracle Database**.

The primary goal of the project is to improve visitor access management by ensuring that access is not automatically trusted. Instead, visitor identity and access permissions are verified and controlled according to defined security policies.

The system provides a centralized platform for managing visitor information and controlling access through authentication, authorization, token generation, and a Zero-Trust policy engine.

---

## 🎯 Why Was This Project Created?

Traditional visitor management systems may rely heavily on predefined or implicit trust. Once a visitor is registered or granted access, controlling what that visitor can access can become difficult.

This project was created to demonstrate how **Zero-Trust security concepts** can be applied to visitor management.

The platform follows the basic principle:

> **"Never trust, always verify."**

Instead of automatically trusting a visitor, the system applies authentication and authorization mechanisms before allowing access to protected resources.

---

## ❗ Problem Statement

Organizations need a secure and reliable way to manage visitors and control their access to resources.

A conventional visitor management approach may have limitations such as:

* Insufficient identity verification
* Uncontrolled visitor access
* Lack of policy-based authorization
* Long-lasting access permissions
* Difficulty monitoring access decisions
* Increased security risks from unauthorized access

The proposed system addresses these challenges by introducing a **Zero-Trust based access management approach**.

---

## 💡 Proposed Solution

The proposed platform provides:

* Visitor identity management
* User authentication
* Authorization and role-based access control
* Zero-Trust policy evaluation
* Token generation
* Controlled access to protected resources
* Oracle database integration
* Web-based interface
* Access management based on security policies

Every access request can be evaluated before permission is granted, helping reduce unnecessary trust within the system.

---

## 🎯 Project Objectives

The main objectives of this project are:

1. To develop a secure visitor identity management system.
2. To implement authentication and authorization mechanisms.
3. To apply Zero-Trust principles to visitor access management.
4. To implement policy-based access control.
5. To generate tokens for controlled access.
6. To integrate the application with an Oracle database.
7. To provide a user-friendly web interface.
8. To demonstrate secure backend and database integration.
9. To provide a foundation for just-in-time access management.

---

## 🔐 Zero-Trust Security Approach

The project is based on the principle of **Zero Trust**, where users and visitors are not automatically trusted.

The system focuses on verifying identity and evaluating access before allowing protected operations.

### Zero-Trust Flow

```text
Visitor/User
     |
     v
Authentication
     |
     v
Identity Verification
     |
     v
Authorization
     |
     v
Zero-Trust Policy Engine
     |
     v
Access Decision
     |
     +------------------+
     |                  |
   ALLOW               DENY
     |                  |
     v                  v
Token / Access      Access Blocked
```

This approach helps ensure that access is granted based on security requirements rather than simply assuming that a user is trusted.

---

## ✨ Key Features

### 👤 Visitor Identity Management

The system provides functionality for managing visitor-related identity information in the application.

### 🔑 Authentication

Authentication mechanisms are implemented to verify users before allowing access to protected parts of the application.

### 🛡️ Authorization

Authorization determines whether an authenticated user is permitted to perform a particular operation or access a particular resource.

### ⚙️ Zero-Trust Policy Engine

The policy engine evaluates access requests according to defined Zero-Trust rules and determines whether access should be allowed or denied.

### 🎫 Token Generation

The system supports token generation as part of the controlled access mechanism.

### 🚪 Access Control

Access is controlled through authentication, authorization, and policy evaluation.

### 🗄️ Oracle Database Integration

The application is integrated with an **Oracle Database** for storing and managing application data.

### 🌐 Web Interface

The frontend is developed using:

* HTML
* CSS
* JavaScript

---

## 🛠️ Technology Stack

| Component            | Technology                     |
| -------------------- | ------------------------------ |
| Programming Language | Python                         |
| Backend Framework    | Flask                          |
| Frontend             | HTML, CSS, JavaScript          |
| Database             | Oracle Database                |
| Database Tool        | SQL*Plus                       |
| Backend Development  | Flask Routes                   |
| Security             | Authentication & Authorization |
| Access Management    | Zero-Trust Policy Engine       |
| Version Control      | Git & GitHub                   |

---

## 🏗️ System Architecture

The application follows a web-based architecture consisting of frontend, backend, security logic, and database components.

```text
+-----------------------------+
|        Frontend             |
|     HTML / CSS / JS         |
+-------------+---------------+
              |
              v
+-----------------------------+
|       Flask Backend         |
|      Flask Routes           |
+-------------+---------------+
              |
      +-------+-------+
      |               |
      v               v
+-----------+   +-------------+
| Security  |   |   Policy    |
| Layer     |   |   Engine    |
+-----------+   +-------------+
      |               |
      +-------+-------+
              |
              v
+-----------------------------+
|      Oracle Database        |
|          SQL*Plus           |
+-----------------------------+
```

---

## 🔄 Application Workflow

The general workflow of the system is:

1. A user/visitor interacts with the web application.
2. The request is received by the Flask backend.
3. Authentication is performed where required.
4. The system checks authorization.
5. The Zero-Trust policy engine evaluates the access request.
6. If the request satisfies the required policy, access is permitted.
7. A token can be generated for controlled access where applicable.
8. The required data is retrieved from or stored in the Oracle database.
9. Unauthorized requests are denied.

---

## 📂 Project Structure

The project is organized into separate backend, frontend, and configuration components.

```text
visitor-zta-project/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   ├── models.py
│   │
│   ├── routes/
│   │   ├── access_routes.py
│   │   ├── auth_routes.py
│   │   ├── console_routes.py
│   │   ├── pages_routes.py
│   │   ├── policy_routes.py
│   │   └── visitor_routes.py
│   │
│   ├── services/
│   │   ├── logger_service.py
│   │   ├── policy_engine.py
│   │   └── token_service.py
│   │
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── dashboard.js
│   │
│   └── templates/
│       ├── access_status.html
│       ├── audit_log.html
│       ├── base.html
│       ├── host_dashboard.html
│       ├── login.html
│       ├── security_console.html
│       └── visitor_register.html
│
├── requirements.txt
├── run.py
├── seed_data.py
├── .gitignore
└── README.md
```

---

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/devsudhanshu-x/visitor-zta-project.git
```

### 2. Navigate to the Project Directory

```bash
cd visitor-zta-project
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux/macOS

```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🗄️ Database Configuration

This project uses **Oracle Database** as its database system.

**SQL*Plus** can be used to manage and configure the Oracle database.

Before running the application, configure the required database settings according to your local Oracle Database setup.

The application uses the following environment configuration:

```text
DATABASE_NAME
```

> **Note:** Do not upload passwords, secret keys, database credentials, or other sensitive information to GitHub.

---

## 🔐 Environment Variables

Create a `.env` file in the project directory and configure the required environment variables.

Example:

```env
DATABASE_NAME=your_database_name
```

Use your own local database configuration values.

The `.env` file should remain private and should not be committed to GitHub.

---

## ▶️ Running the Application

After completing the setup and database configuration, run:

```bash
python run.py
```

The Flask application will then start on the configured local server.

Open the displayed local URL in your web browser.

---

## 🧪 Testing

Testing was performed as part of the development process to verify the functionality of the application.

The project testing work included checking:

* Frontend functionality
* Backend routes
* Authentication
* Authorization
* Database integration
* Access control
* Zero-Trust policy behavior
* Token-related functionality

---

## 📚 Documentation

Documentation was prepared to explain the project's:

* Purpose
* Architecture
* Technologies
* Security approach
* Backend implementation
* Database integration
* Project workflow
* Setup and execution process

---

## 🚀 Deployment

Deployment activities were also handled as part of the project development process, including preparing the application for execution and maintaining the project through GitHub.

---

# 👥 Team Members

This is a **Team Project** developed by:

### 👨‍💻 Sudhanshu Singh

**Role:** Backend & Database Developer

### Contributions

* Flask route development
* Backend development
* Oracle database integration
* Authentication
* Authorization
* Zero-Trust policy engine
* Token generation
* Access control
* Frontend testing
* Project documentation
* Deployment
* GitHub repository management

---

### 👨‍💻 Isa Khatri

**Role:** Frontend Developer

### Contribution

* Frontend development
* User interface implementation
* HTML development
* CSS styling
* JavaScript-based frontend functionality

---

## 🤝 Team Contribution

The project was developed collaboratively.

```text
              PROJECT
                 |
        +--------+--------+
        |                 |
        v                 v
 Sudhanshu Singh       Isa Khatri
 Backend & Database    Frontend
        |                 |
        v                 v
 Flask / Database      HTML / CSS / JS
 Security Logic       User Interface
```

The backend and database components were developed and integrated with the frontend to create the complete web-based visitor access management platform.

---

## 🌱 Future Scope

The project can be further enhanced with additional capabilities such as:

* Advanced visitor identity verification
* Multi-factor authentication
* More granular access policies
* Real-time access monitoring
* Improved audit and reporting capabilities
* Role-based administrative dashboards
* Automated access expiration
* Enhanced security monitoring
* Cloud deployment
* Integration with additional identity management systems

---

## 🔒 Security Considerations

Security is a core part of this project.

Important security practices include:

* Do not expose database credentials.
* Do not commit `.env` files.
* Use strong authentication credentials.
* Apply authorization checks to protected resources.
* Validate user input.
* Apply access policies before granting protected access.
* Keep application dependencies updated.

---

## 📌 Project Highlights

> **Backend:** Python + Flask
> **Frontend:** HTML + CSS + JavaScript
> **Database:** Oracle Database
> **Database Management:** SQL*Plus
> **Security Model:** Zero Trust
> **Project Type:** Team Project
> **Primary Backend & Database Developer:** Sudhanshu Singh
> **Frontend Developer:** Isa Khatri


## 📖 Conclusion

The **Zero-Trust Visitor Identity and Just-in-Time Access Management Platform** demonstrates how Zero-Trust security concepts can be applied to visitor identity and access management.

By combining **Python, Flask, HTML, CSS, JavaScript, and Oracle Database**, the project provides a foundation for secure visitor management with authentication, authorization, policy-based access control, and controlled access mechanisms.

The project also provides practical experience in **backend development, database integration, security implementation, frontend development, testing, documentation, deployment, and GitHub-based project management**.

---

## 👨‍💻 Authors

**Sudhanshu Singh**
Backend & Database Developer

**Isa Khatri**
Frontend Developer

---

## 🔗 Repository

**GitHub:**
https://github.com/devsudhanshu-x/visitor-zta-project

---

## ⭐ Acknowledgement

This project was developed as a collaborative academic project to gain practical experience in **web development, database management, backend engineering, and Zero-Trust security concepts**.
