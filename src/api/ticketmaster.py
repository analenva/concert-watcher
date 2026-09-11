import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TICKETMASTER_API_KEY")
API_URL = "https://app.ticketmaster.com/discovery/v2"


def _request(endpoint, params):
    if not API_KEY:
        raise RuntimeError(
            "TICKETMASTER_API_KEY is missing. Add it to a .env file in the project root."
        )

    response = requests.get(
        f"{API_URL}/{endpoint}",
        params={"apikey": API_KEY, **params},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def get_events():
    all_events = []
    page = 0

    while True:
        params = {
            "countryCode": "SE",
            "classificationName": "Music",
            "size": 100,
            "page": page
        }

        data = _request("events.json", params)

        if "_embedded" not in data:
            break

        events = data["_embedded"]["events"]
        all_events.extend(events)

        total_pages = data["page"]["totalPages"]

        page += 1

        if page >= total_pages:
            break

    return all_events


def find_attraction(artist):
    params = {
        "keyword": artist,
        "size": 10
    }

    data = _request("attractions.json", params)

    if "_embedded" not in data:
        return None

    attractions = data["_embedded"].get("attractions", [])

    for attraction in attractions:
        if attraction["name"].lower() == artist.lower():
            return attraction["id"]

    return None
