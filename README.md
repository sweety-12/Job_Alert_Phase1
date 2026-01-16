graph LR
    U[User / Browser] -->|Preferences Form| FE[React Frontend<br/>Vercel]
    FE -->|API Requests| BE[FastAPI Backend<br/>Render]
    BE --> DB[(Database<br/>Persistent Storage)]

    GH[GitHub Actions Scheduler] -->|Cron Trigger| BE
    BE -->|Fetch Jobs| JS[Job Sources<br/>LinkedIn / Company Pages]
    BE -->|Send Emails| EM[Resend Email Service]
