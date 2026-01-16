# 📬 CampusInbox – Daily Job Alerts System

CampusInbox is a full-stack job alert platform that sends **personalized job notifications via email** based on user preferences.  
Users can save job roles, locations, experience levels, and receive **test alerts instantly** and **daily automated alerts**.

---

## 🚀 Features

- Save job preferences (role, location, experience, work mode)
- Send **instant test job alert emails**
- Automated **daily job alerts**
- Email delivery using Resend
- Scheduler using GitHub Actions
- Scalable backend architecture
- Production-ready system design

---

## 🛠 Tech Stack

**Frontend**
- React
- Tailwind CSS
- Deployed on Vercel

**Backend**
- FastAPI
- Python
- Deployed on Render

**Database**
- PostgreSQL (Persistent storage)

**Email**
- Resend API

**Scheduler**
- GitHub Actions (Cron jobs)

---

## 🔧 System Architecture

```mermaid
graph LR
    U[User / Browser] -->|Job Preferences| FE[React Frontend<br/>Vercel]
    FE -->|REST APIs| BE[FastAPI Backend<br/>Render]

    BE --> DB[(PostgreSQL<br/>Persistent Database)]
    BE -->|Fetch Jobs| JS[Job Sources<br/>LinkedIn / Company Sites]
    BE -->|Send Emails| EM[Resend Email Service]

    GH[GitHub Actions<br/>Scheduler] -->|Daily Cron| BE


sequenceDiagram
    participant U as User
    participant FE as Frontend (Vercel)
    participant BE as Backend (FastAPI)
    participant DB as Database
    participant GH as GitHub Actions
    participant EM as Email Service

    U->>FE: Fill job preferences
    FE->>BE: Save preferences API
    BE->>DB: Store preferences

    U->>FE: Send test alert
    FE->>BE: /send-test-alert
    BE->>EM: Send test email

    GH->>BE: Daily cron trigger
    BE->>DB: Fetch all preferences
    BE->>EM: Send daily job alerts

