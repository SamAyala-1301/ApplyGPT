


import requests
from bs4 import BeautifulSoup

def scrape_naukri_jobs(role_query: str) -> list:
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    search_term = role_query.lower().replace(" ", "-")
    url = f"https://www.naukri.com/{search_term}-jobs-in-india"

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("⚠️ Naukri blocked or returned bad status:", response.status_code)
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    job_cards = soup.select("article.jobTuple")

    results = []
    for card in job_cards[:10]:  # limit to 10 jobs
        title_elem = card.select_one("a.title")
        company_elem = card.select_one("a.subTitle")
        location_elem = card.select_one("li.location")
        jd_elem = card.select_one("ul.tags.has-description")

        title = title_elem.get_text(strip=True) if title_elem else "N/A"
        company = company_elem.get_text(strip=True) if company_elem else "N/A"
        location = location_elem.get_text(strip=True) if location_elem else "N/A"
        jd = jd_elem.get_text(strip=True) if jd_elem else "No description"
        link = title_elem['href'] if title_elem and title_elem.has_attr('href') else "#"

        results.append({
            "title": title,
            "company": company,
            "location": location,
            "link": link,
            "jd": jd
        })

    return results