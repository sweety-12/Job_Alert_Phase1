# from playwright.sync_api import sync_playwright

# def fetch_naukri_jobs(role, location, max_jobs=40):
#     results = []

#     # Correct Naukri URL pattern
#     url = f"https://www.naukri.com/{role.replace(' ', '-')}-jobs-in-{location.replace(' ', '-')}"
#     print("Opening:", url)

#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True)  # Keep visible for debugging
#         page = browser.new_page()

#         page.goto(url, timeout=60000)

#         # Updated selector from Naukri's HTML
#         page.wait_for_selector("div.jobTuple", timeout=30000)

#         job_cards = page.query_selector_all("div.jobTuple")[:max_jobs]

#         for job in job_cards:
#             try:
#                 title = job.query_selector("a.title").inner_text().strip()
#                 company = job.query_selector("a.subTitle").inner_text().strip()
#                 location_text = job.query_selector("li.location").inner_text().strip()
#                 posted = job.query_selector("span.fright").inner_text().strip()
#                 snippet = job.query_selector("div.job-description").inner_text().strip()
#                 apply_link = job.query_selector("a.title").get_attribute("href")

#                 results.append({
#                     "source": "Naukri",
#                     "title": title,
#                     "company": company,
#                     "location": location_text,
#                     "posted_at": posted,
#                     "snippet": snippet,
#                     "apply_link": apply_link
#                 })
#             except:
#                 pass

#         browser.close()

#     return results


# if __name__ == "__main__":
#     # YOU control the role + location from here
#     jobs = fetch_naukri_jobs("ML Engineer", "india")
#     print(jobs)

from playwright.sync_api import sync_playwright
import time

def fetch_naukri_jobs(role, location, max_jobs=40):
    results = []
    url = f"https://www.naukri.com/{role.replace(' ', '-')}-jobs-in-{location.replace(' ', '-')}"
    print("Fetching:", url)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            page.goto(url, timeout=60000)
            time.sleep(10)  # wait for JS to load

            # Wait for job cards
            page.wait_for_selector("article.jobTuple", timeout=60000)
            job_cards = page.query_selector_all("article.jobTuple")[:max_jobs]

            for job in job_cards:
                try:
                    title = job.query_selector("a.title").inner_text().strip()
                    company = job.query_selector("a.subTitle").inner_text().strip()
                    loc_el = job.query_selector("li.location")
                    location_text = loc_el.inner_text().strip() if loc_el else ""
                    posted_el = job.query_selector("span.fright")
                    posted = posted_el.inner_text().strip() if posted_el else ""
                    snippet_el = job.query_selector("div.job-description")
                    snippet = snippet_el.inner_text().strip() if snippet_el else ""
                    link = job.query_selector("a.title").get_attribute("href")

                    results.append({
                        "source": "Naukri",
                        "title": title,
                        "company": company,
                        "location": location_text,
                        "posted_at": posted,
                        "snippet": snippet,
                        "apply_link": link
                    })
                except:
                    pass
        except Exception as e:
            print("Error fetching jobs:", e)
        finally:
            browser.close()  # this will always run, safely

    return results


if __name__ == "__main__":
    jobs = fetch_naukri_jobs("ML Engineer", "india")
    print(jobs)
