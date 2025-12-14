# import json
import os
from database.db import get_db_connection
from platforms.linkedin_playwright import fetch_linkedin_jobs
from .email_service import send_email

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# # PREF_DB = os.path.join(BASE_DIR, "database/preferences_db.json")
# PREF_DB = os.path.join(BASE_DIR, "database", "preferences_db.json")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PREF_DB = os.path.join(BASE_DIR, "database", "preferences_db.json")

def build_html_email(jobs, job_role, location):
     
    html = f"""
    <h2>Daily Job Alerts for {job_role} in {location}</h2>
    <p>Here are the latest job listings:</p>
    <ul>
    """
    for job in jobs:

        html += f"""
        <li>
            <b>{job['title']}</b> — {job.get('company', 'Unknown')}<br>
            <a href="{job['apply_link']}">Apply Now</a>
        </li>
        """
    html += "</ul><p>Good luck with your applications!</p>"
    return html


def send_daily_alerts():
    print("=== Running Daily Alerts ===")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM preferences")
    preferences = cursor.fetchall()

    conn.close()

    for pref in preferences:
        job_role = pref["job_role"]
        location = pref["location"]
        email = pref["email"]

        print(f"Fetching jobs for: {job_role} — {location} — {email}")

        jobs = fetch_linkedin_jobs(job_role, location)
        print(f"Found {len(jobs)} jobs")

        if jobs:
            html_content = build_html_email(jobs, job_role, location)
            send_email(email, f"Daily {job_role} Jobs", html_content)
            #send_email(email, job_role, jobs)

    print("=== Alerts Sent ===")
    return True

# if __name__ == "__main__":
#     send_daily_alerts()



# # def load_preferences():
# #     with open(PREF_DB, "r") as f:
# #         return json.load(f)


# # def send_daily_alerts():
# #     print("=== Running Daily Alerts ===")

# #     prefs = load_preferences()

# #     for pref in prefs:
# #         role = pref["job_role"]
# #         location = pref["location"]
# #         email = pref["email"]

# #         print(f"Fetching jobs for: {role} — {location} — {email}")

# #         jobs = fetch_linkedin_jobs(role, location)

# #         html = build_email_html(jobs)

# #         send_email(
# #             recipient=email,
# #             subject=f"Daily Job Alerts for {role}",
# #             html_content=html,
# #         )

# #     print("=== Alerts Sent ===")


# # def build_email_html(jobs):
# #     # if not jobs:
# #     #     return "<h3>No new jobs found today.</h3>"

# #     html = "<h2>Your Daily Job Alerts</h2><ul>"

# #     for job in jobs:
# #         html += f"""
# #         <li>
# #             <b>{job['title']}</b> — {job['company']}<br>
# #             {job['location']}<br>
# #             <a href="{job['apply_link']}">Apply Here</a>
# #         </li><br>
# #         """

# #     html += "</ul>"
# #     return html

# def shorten(url):
#     # Remove long tracking params — keeps the main link working
#     return url.split("?")[0][:60] + ("..." if len(url) > 60 else "")

# def send_daily_alerts():
#     """Read all user preferences & send job alerts."""

#     # Load saved user preferences
#     try:
#         with open(PREF_DB, "r") as f:
#             prefs = json.load(f)
#     except Exception as e:
#         return {"error": f"Failed to read DB: {str(e)}"}

#     if not prefs:
#         return {"message": "No user preferences found"}

#     print("\n=== Running Daily Alerts ===")

#     for pref in prefs:
#         try:
#             role = pref.get("role") or pref.get("job_role")
#             location = pref.get("location", "India")
#             email = pref.get("email")

#             if not role or not email:
#                 print("Skipping entry — incomplete data:", pref)
#                 continue

#             print(f"\nFetching jobs for: {role} — {location} — {email}")

#             jobs = fetch_linkedin_jobs(role, location)
#             print(f"Found {len(jobs)} jobs")

#             if not jobs:
#                 body = f"No new jobs found for: {role}"
#             else:
#                 body = "\n".join([f"{job['title']} - {job['company']} - {job['apply_link']}" for job in jobs[:10]])

#             subject = f"Your Daily Job Alerts — {role} ({location})"

#             # try sending email
#             send_email(email, subject, body)

#         except Exception as e:
#             print("Error for one user:", str(e))
#             continue

#     return {"message": "Daily alerts sent successfully!"}


# # else:
# #         # Start the HTML container
# #         body = """
# #         <html>
# #         <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333333;">
# #             <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
# #                 <h2 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;">
# #                     Here are today's top job matches for you:
# #                 </h2>
# #         """

# #         for i, job in enumerate(jobs[:10], start=1):
# #             Apply_link = shorten(job["apply_link"])
            
# #             # Append each job as an HTML card
# #             body += f"""
# #                 <div style="border: 1px solid #e1e1e1; border-radius: 8px; padding: 20px; margin-bottom: 20px; background-color: #ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
# #                     <h3 style="margin-top: 0; color: #2c3e50; font-size: 18px;">
# #                         {i}. {job['title']}
# #                     </h3>
                    
# #                     <p style="margin: 5px 0; font-size: 14px;">
# #                         <strong style="color: #7f8c8d;">Company:</strong> {job['company']}
# #                     </p>
                    
# #                     <p style="margin: 5px 0; font-size: 14px;">
# #                         <strong style="color: #7f8c8d;">Location:</strong> {job.get('location', 'Not specified')}
# #                     </p>
                    
# #                     <div style="margin-top: 15px;">
# #                         <a href="{Apply_link}" style="background-color: #3498db; color: #ffffff; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 14px; display: inline-block;">
# #                             Apply Now
# #                         </a>
# #                     </div>
# #                 </div>
# #             """

# #         # Close the HTML tags
# #         body += """
# #             </div>
# #             <p style="text-align: center; font-size: 12px; color: #999;">
# #                 Automated Job Alert
# #             </p>
# #         </body>
# #         </html>
# #         """