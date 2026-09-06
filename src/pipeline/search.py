from src.api.ticketmaster import get_events


favorite_bands = [
    "The Sisters of Mercy",
    "Ghost",
    "Lacrimosa",
    "In This Moment",
    "Dimmu Borgir",
    "Lacuna Coil"
]

favorite_bands_lower = {band.lower() for band in favorite_bands}

events = get_events()

print("Total events:", len(events))

for event in events:
    attractions = event.get("_embedded", {}).get("attractions", [])

    for attraction in attractions:
        artist = attraction.get("name")

        if artist and artist.lower() in favorite_bands_lower:
            date = event.get("dates", {}).get("start", {}).get("localDate")
            time = event.get("dates", {}).get("start", {}).get("localTime")

            venues = event.get("_embedded", {}).get("venues", [])
            venue = venues[0].get("name") if venues else "Unknown venue"

            event_url = event.get("url", "No URL")

            print("\nFOUND:", artist)
            print("Event:", event.get("name"))
            print("Date:", date)
            print("Time:", time)
            print("Venue:", venue)
            print("URL:", event_url)
