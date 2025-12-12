
import requests
from bs4 import BeautifulSoup

def fetch_linkedin_jobs(query, location, max_jobs=40):
    query = query.replace(" ", "%20")
    location = location.replace(" ", "%20")

    url = (
        "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
        f"?keywords={query}&location={location}"
    )

    response = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0"
    })

    if response.status_code != 200:
        print("Failed to fetch LinkedIn data")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    postings = soup.find_all("li")

    results = []
    for post in postings[:max_jobs]:
        title = post.find("h3")
        company = post.find("h4")
        loc = post.find("span", class_="job-search-card__location")
        link = post.find("a", class_="base-card__full-link")
        time = post.find("time")

        results.append({
            "source": "LinkedIn",
            "title": title.text.strip() if title else "",
            "company": company.text.strip() if company else "",
            "location": loc.text.strip() if loc else "",
            "posted_at": time["datetime"] if time else "",
            "snippet": "",
            "apply_link": link["href"] if link else ""
        })

    print(f"Found {len(results)} jobs")
    return results


# Linkedin masking the jobs in mail 

# import time
# from playwright.sync_api import sync_playwright

# def fetch_linkedin_jobs(query, location, max_jobs=40):
#     results = []
#     url = (
#         "https://www.linkedin.com/jobs/search/"
#         f"?keywords={query}&location={location}"
#     )

#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True)
#         page = browser.new_page()
#         page.goto(url, timeout=60000)

#         # Wait for job cards to load
#         page.wait_for_selector(".jobs-search__results-list li", timeout=20000)

#         # Query job cards
#         cards = page.query_selector_all(".jobs-search__results-list li")

#         for c in cards[:max_jobs]:
#             title = c.query_selector("h3")
#             company = c.query_selector("h4")
#             loc_el = c.query_selector(".job-search-card__location")
#             link_el = c.query_selector("a")
#             date_el = c.query_selector("time")
#             snippet_el = c.query_selector(".job-search-card__snippet")

#             results.append({
#                 "source": "LinkedIn",
#                 "title": title.inner_text().strip() if title else "",
#                 "company": company.inner_text().strip() if company else "",
#                 "location": loc_el.inner_text().strip() if loc_el else "",
#                 "posted_at": date_el.get_attribute("datetime") if date_el else "",
#                 "snippet": snippet_el.inner_text().strip() if snippet_el else "",
#                 "apply_link": link_el.get_attribute("href") if link_el else ""
#             })

#         browser.close()

#     print(f"Found {len(results)} jobs")
#     return results


# if __name__ == "__main__":
#     print(fetch_linkedin_jobs("ML Engineer", "india"))
