# linkedin.py  (Phase-0 working version)
import requests
import time
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def search_linkedin(query_titles, locations):
    """
    Scrape LinkedIn public job listings (HTML only).
    This is the same version that worked perfectly in Phase 0.
    """
    results = []
    base_url = "https://www.linkedin.com/jobs/search/"

    q = "+".join(query_titles)
    loc = "+".join(locations)

    # Build URL manually
    url = (
        base_url +
        "?keywords=" + requests.utils.quote(q) +
        "&location=" + requests.utils.quote(loc)
    )

    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(resp.text, "html.parser")

        #cards = soup.select("ul.jobs-search__results-list li")
        cards = soup.select("ul.scaffold-layout__list-container li")


        for c in cards[:40]:
            title_el = c.select_one("h3")
            company_el = c.select_one("h4")
            loc_el = c.select_one(".job-result-card__location")
            link_el = c.select_one("a")
            snippet_el = c.select_one(".job-result-card__snippet")
            posted_el = c.select_one("time")

            title = title_el.get_text(strip=True) if title_el else ""
            company = company_el.get_text(strip=True) if company_el else ""
            location = loc_el.get_text(strip=True) if loc_el else ""
            link = (
                "https://www.linkedin.com" + link_el["href"]
                if link_el and link_el["href"].startswith("/")
                else (link_el["href"] if link_el else "")
            )
            snippet = snippet_el.get_text(strip=True) if snippet_el else ""
            posted = posted_el.get("datetime") if posted_el else ""

            results.append({
                "source": "LinkedIn",
                "title": title,
                "company": company,
                "location": location,
                "posted_at": posted,
                "snippet": snippet,
                "apply_link": link
            })

        time.sleep(1.5)

    except Exception as e:
        print("LinkedIn parser error:", e)

    return results


# Testing the scraper
if __name__ == "__main__":
    titles = ["AI Engineer"]
    locations = ["India"]
    results = search_linkedin(titles, locations)
    print(f"Found {len(results)} jobs")
    print(results)
