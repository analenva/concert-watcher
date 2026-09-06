import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TICKETMASTER_API_KEY")


def get_events():
    url = "https://app.ticketmaster.com/discovery/v2/events.json"

    all_events = []
    page = 0

    while True:
        params = {
            "apikey": API_KEY,
            "countryCode": "SE",
            "classificationName": "Music",
            "size": 100,
            "page": page
        }

        response = requests.get(url, params=params)

        print(response.status_code)

        data = response.json()

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
    url = "https://app.ticketmaster.com/discovery/v2/attractions.json"

    params = {
        "apikey": API_KEY,
        "keyword": artist,
        "size": 10
    }

    response = requests.get(url, params=params)

    print(response.status_code)

    data = response.json()

    if "_embedded" not in data:
        return None

    attractions = data["_embedded"].get("attractions", [])

    for attraction in attractions:
        if attraction["name"].lower() == artist.lower():
            return attraction["id"]

    return None
