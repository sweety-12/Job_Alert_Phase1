# from playwright.sync_api import sync_playwright
# import time

# def fetch_foundit_jobs(query, location, max_jobs=40):
#     results = []
#     # Build search URL — this format works currently
#     url = f"https://www.foundit.in/search/{query.replace(' ', '-')}-jobs-in-{location.replace(' ', '-')}"
#     print("Fetching:", url)

#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True)
#         page = browser.new_page()
#         page.goto(url, timeout=60000)

#         # Wait for job listing container — update selector as per actual site
#         try:
#             page.wait_for_selector("div.card-wrap", timeout=30000)
#         except:
#             print("Timeout/Error — no job listings container found")
#             browser.close()
#             return results

#         job_cards = page.query_selector_all("div.card-wrap")[:max_jobs]

#         for job in job_cards:
#             try:
#                 title_el = job.query_selector("h3.card-heading > a")
#                 company_el = job.query_selector("div.company-name > a")
#                 loc_el = job.query_selector("div.info > span.loc")
#                 date_el = job.query_selector("div.info > span.posted-on")
#                 link = title_el.get_attribute("href") if title_el else None

#                 results.append({
#                     "source": "Foundit",
#                     "title": title_el.inner_text().strip() if title_el else "",
#                     "company": company_el.inner_text().strip() if company_el else "",
#                     "location": loc_el.inner_text().strip() if loc_el else "",
#                     "posted_at": date_el.inner_text().strip() if date_el else "",
#                     "apply_link": link
#                 })
#             except Exception as e:
#                 continue

#         browser.close()

#     return results

# if __name__ == "__main__":
#     jobs = fetch_foundit_jobs("ML Engineer", "india")
#     print(f"Found {len(jobs)} jobs")
#     for j in jobs:
#         print(j)

import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

BASE_URL = "https://www.foundit.in/search"

def build_search_url(role: str, location: str) -> str:
    # Foundit supports both path- and query-based search; this keeps it close
    # to the visible URL patterns on the site.
    role_slug = role.replace(" ", "-").lower()
    loc_slug = location.replace(" ", "-").lower()
    # Example pattern: /ml-engineer-jobs-in-india?query=ml+engineer
    return f"{BASE_URL}/{role_slug}-jobs-in-{loc_slug}?query={role.replace(' ', '+')}"

def fetch_foundit_jobs(role, location, max_jobs=40, headless=True):
    url = build_search_url(role, location)
    print("Fetching:", url)
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        page.goto(url, timeout=60000, wait_until="networkidle")

        try:
            # 1. Wait for ANY job card/container that actually appears on Foundit
            # Common patterns: joblist, job-card, job-tuple, etc.
            # Adjust selector if the site changes again.
            page.wait_for_selector("div[class*='job'], li[class*='job']", timeout=30000)
        except PlaywrightTimeoutError:
            print("Timeout/Error — no job listings container found")
            browser.close()
            return results

        # Optional: scroll to load more jobs (basic infinite scroll support)
        last_height = None
        for _ in range(10):
            current_height = page.evaluate("document.body.scrollHeight")
            if current_height == last_height:
                break
            last_height = current_height
            page.mouse.wheel(0, 2000)
            time.sleep(1.5)

        # 2. Query potential job-card elements
        # This is deliberately broad; you can tighten once you inspect the DOM.
        job_cards = page.query_selector_all("article, div[class*='job'], li[class*='job']")
        print(f"Found {len(job_cards)} raw job nodes")

        for job in job_cards:
            if len(results) >= max_jobs:
                break
            try:
                # Try a few reasonable selectors for title, company, etc.
                title_el = (
                    job.query_selector("h3 a") or
                    job.query_selector("h3") or
                    job.query_selector("a[class*='job-title']")
                )
                company_el = (
                    job.query_selector("h4 a") or
                    job.query_selector("h4") or
                    job.query_selector("span[class*='company']") or
                    job.query_selector("p[class*='company']")
                )
                location_el = (
                    job.query_selector("span[class*='location']") or
                    job.query_selector("p[class*='location']") or
                    job.query_selector("li[class*='location']")
                )
                posted_el = (
                    job.query_selector("span[class*='posted']") or
                    job.query_selector("p[class*='posted']") or
                    job.query_selector("li[class*='posted']")
                )
                link_el = (
                    job.query_selector("a[class*='job-title']") or
                    job.query_selector("h3 a") or
                    job.query_selector("a")
                )

                # Skip if there is no obvious title
                if not title_el:
                    continue

                title = title_el.inner_text().strip()
                company = company_el.inner_text().strip() if company_el else ""
                location_text = location_el.inner_text().strip() if location_el else ""
                posted_at = posted_el.inner_text().strip() if posted_el else ""
                apply_link = link_el.get_attribute("href") if link_el else ""

                # Ensure absolute URL
                if apply_link and apply_link.startswith("/"):
                    apply_link = "https://www.foundit.in" + apply_link

                results.append({
                    "source": "Foundit",
                    "title": title,
                    "company": company,
                    "location": location_text,
                    "posted_at": posted_at,
                    "apply_link": apply_link
                })
            except Exception:
                # Ignore malformed job cards and continue
                continue

        browser.close()

    return results


if __name__ == "__main__":
    jobs = fetch_foundit_jobs("ML Engineer", "india", max_jobs=40, headless=True)
    print(f"Found {len(jobs)} jobs")
    for j in jobs:
        print(j)
