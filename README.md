## Concert watcher

This script fetches music events in Sweden from Ticketmaster and prints events
whose artists appear in `src/config/favorites.py`.

### Setup

1. Install dependencies with `pip install -r requirements.txt`.
2. Create a `.env` file in the project root containing:

	```text
	TICKETMASTER_API_KEY=your_api_key
	```

3. Run the watcher from the project root:

	```text
	python src/pipeline/search.py
	```

The output includes the matching band, event, date, venue, and Ticketmaster URL.
