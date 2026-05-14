import requests

# ======================================================
# ADZUNA API KEYS
# ======================================================

APP_ID = "785d81b6"
APP_KEY = "cd567dc896e3dd98a7fc7a93f7f1e2da"

# ======================================================
# FETCH JOBS
# ======================================================

def fetch_jobs(domain, state):

    url = (
        f"https://api.adzuna.com/v1/api/jobs/us/search/1"
        f"?app_id={APP_ID}"
        f"&app_key={APP_KEY}"
        f"&results_per_page=50"
        f"&what={domain}"
        f"&where={state}"
        f"&max_days_old=1"
    )

    response = requests.get(url)

    data = response.json()

    jobs = []

    results = data.get("results", [])

    # ======================================================
    # SAFE LOOP
    # ======================================================

    for item in results:

        # SKIP INVALID ITEMS

        if not isinstance(item, dict):
            continue

        company_data = item.get(
            "company",
            {}
        )

        location_data = item.get(
            "location",
            {}
        )

        if not isinstance(company_data, dict):
            company_data = {}

        if not isinstance(location_data, dict):
            location_data = {}

        jobs.append({

            "title": item.get(
                "title",
                "N/A"
            ),

            "company": company_data.get(
                "display_name",
                "N/A"
            ),

            "location": location_data.get(
                "display_name",
                "USA"
            ),

            "url": item.get(
                "redirect_url",
                "#"
            ),

            "description": item.get(
                "description",
                ""
            )[:300],

            "publication_date": item.get(
                "created",
                "Recently Posted"
            )

        })

    return jobs