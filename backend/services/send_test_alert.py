from services.email_service import send_email
from platforms.linkedin_playwright import fetch_linkedin_jobs
from database.db import get_db_connection

def send_test_alert(email: str):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT job_role, location, experience, work_mode FROM preferences WHERE email = ?",
        (email,)
    )

    row = cursor.fetchone()
    conn.close()

    if not row:
        return {"error": "No preferences found for this email"}

    job_role, location, experience, work_mode = row

    # Fetch jobs using preferences
    jobs = fetch_linkedin_jobs(job_role, location)

    html_content = f"""
    <h2>🚀 Test Job Alert</h2>
    <p>Role: {job_role}</p>
    <p>Location: {location}</p>
    <p>Found <b>{len(jobs)}</b> jobs for you.</p>
    """

    send_email(
        recipient=email,
        subject="Your Test Job Alert",
        html_content=html_content
    )

    return {"message": "Test alert sent successfully"}








# from services.email_service import send_email
# from platforms.linkedin_playwright import fetch_linkedin_jobs
# # from database.db import get_user_by_email
# from database.db import get_db_connection

# def send_test_alert(email: str):
#     user = get_db_connection(email)

#     if not user:
#         return {"error": "User not found"}

#     jobs = fetch_linkedin_jobs(user)

#     html_content = f"""
#     <h2>Test Job Alert</h2>
#     <p>Found {len(jobs)} jobs based on your preferences.</p>
#     """

#     send_email(
#         recipient=email,
#         subject="Test Job Alert",
#         html_content=html_content
#     )

#     return {"message": "Test alert sent successfully"}







# # # from fastapi import APIRouter, HTTPException
# # # from pydantic import BaseModel
# # from services.email_service import send_email
# # from services.job_service import fetch_jobs_for_user
# # from db import get_user_by_email

# # router = APIRouter()

# # class TestAlertRequest(BaseModel):
# #     email: str

# # @router.post("/send-test-alert")
# # def send_test_alert(data: TestAlertRequest):

# #     user = get_user_by_email(data.email)
# #     if not user:
# #         raise HTTPException(status_code=404, detail="User not found")

# #     jobs = fetch_jobs_for_user(
# #         job_role=user.job_role,
# #         location=user.location,
# #         experience=user.experience,
# #         work_mode=user.work_mode,
# #     )

# #     if not jobs:
# #         return {"message": "No jobs found right now"}

# #     html = build_job_email_html(jobs, user)

# #     success = send_email(
# #         recipient=user.email,
# #         subject="🚀 Your Test Job Alert",
# #         html_content=html
# #     )

# #     if not success:
# #         raise HTTPException(status_code=500, detail="Email failed")

# #     return {"message": "Test alert sent successfully!"}
