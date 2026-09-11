import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.api.ticketmaster import get_events
from src.config.favorites import FAVORITE_BANDS


def _normalise_name(name):
    return " ".join(name.casefold().split())


def find_favorite_concerts(events, favorite_bands=FAVORITE_BANDS):
    favorite_bands_by_name = {
        _normalise_name(band): band for band in favorite_bands
    }
    concerts = []

    for event in events:
        attractions = event.get("_embedded", {}).get("attractions", [])
        matching_bands = []

        for attraction in attractions:
            artist = attraction.get("name")
            if artist and _normalise_name(artist) in favorite_bands_by_name:
                matching_bands.append(favorite_bands_by_name[_normalise_name(artist)])

        if not matching_bands:
            continue

        start = event.get("dates", {}).get("start", {})
        venues = event.get("_embedded", {}).get("venues", [])
        venue = venues[0].get("name", "Unknown venue") if venues else "Unknown venue"
        concerts.append({
            "bands": sorted(set(matching_bands)),
            "event": event.get("name", "Unnamed event"),
            "date": start.get("localDate", "Unknown date"),
            "time": start.get("localTime", "Unknown time"),
            "venue": venue,
            "url": event.get("url", "No URL"),
        })

    return concerts


def main():
    events = get_events()
    concerts = find_favorite_concerts(events)

    print("Total events:", len(events))
    print("Favorite concerts in Sweden:", len(concerts))

    for concert in concerts:
        print(f"\nFOUND: {', '.join(concert['bands'])}")
        print("Event:", concert["event"])
        print("Date:", concert["date"])
        print("Time:", concert["time"])
        print("Venue:", concert["venue"])
        print("URL:", concert["url"])


if __name__ == "__main__":
    main()
