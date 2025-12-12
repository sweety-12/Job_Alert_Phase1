import requests
from bs4 import BeautifulSoup
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_indeed_jobs(query, location, max_jobs=40):
    results = []

    url = (
        "https://in.indeed.com/jobs?"
        f"q={requests.utils.quote(query)}&"
        f"l={requests.utils.quote(location)}"
    )

    print("Fetching:", url)

    try:
        html = requests.get(url, headers=HEADERS, timeout=15).text
        soup = BeautifulSoup(html, "html.parser")

        # The JSON data is inside <script id="mosaic-data">
        script = soup.find("script", id="mosaic-data")

        if not script:
            print("❌ No JSON script found — page blocked or changed.")
            return []

        data = json.loads(script.text)

        job_list = (
            data.get("mosaic-provider-jobcards", {})
                .get("metaData", {})
                .get("props", {})
                .get("pageProps", {})
                .get("jobRequest", {})
                .get("jobs", [])
        )

        if not job_list:
            print("❌ No job data found inside JSON.")
            return []

        for job in job_list[:max_jobs]:
            results.append({
                "source": "Indeed",
                "title": job.get("title", ""),
                "company": job.get("company", ""),
                "location": job.get("formattedLocation", ""),
                "posted_at": job.get("pubDate", ""),
                "snippet": job.get("snippet", "").replace("<b>", "").replace("</b>", ""),
                "apply_link": "https://in.indeed.com/viewjob?jk=" + job.get("jobkey", "")
            })

        return results

    except Exception as e:
        print("Error:", e)
        return []


if __name__ == "__main__":
    jobs = fetch_indeed_jobs("ML Engineer", "India")
    print("Found", len(jobs), "jobs")
    for j in jobs[:3]:
        print(j)
