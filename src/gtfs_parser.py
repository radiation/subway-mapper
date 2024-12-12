import requests
from google.transit import gtfs_realtime_pb2
import datetime
import json
import os
import csv

# Base URLs for the MTA feeds
BASE_URL = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds"
FEED_URLS = {
    "ACE": f"{BASE_URL}/nyct%2Fgtfs-ace",
    "BDFM": f"{BASE_URL}/nyct%2Fgtfs-bdfm",
    "G": f"{BASE_URL}/nyct%2Fgtfs-g",
    "JZ": f"{BASE_URL}/nyct%2Fgtfs-jz",
    "NQRW": f"{BASE_URL}/nyct%2Fgtfs-nqrw",
    "L": f"{BASE_URL}/nyct%2Fgtfs-l",
    "123456": f"{BASE_URL}/nyct%2Fgtfs",
    "SIR": f"{BASE_URL}/nyct%2Fgtfs-si"
}

CACHE_DIR = "data/"
CACHE_FILE = os.path.join(CACHE_DIR, "gtfs_cache.json")

def get_station_name(stop_id, stops):
    """Return the station name for a given stop ID."""
    return stops.get(stop_id, {}).get("stop_name", "Unknown Stop")

def load_csv_to_dict(file_path, key_field):
    """Load a CSV file into a dictionary keyed by the specified field."""
    data = {}
    try:
        with open(file_path, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                data[row[key_field]] = row
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
    return data

def load_csv_to_list(file_path):
    """Load a CSV file into a list of dictionaries."""
    data = []
    try:
        with open(file_path, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
    return data

def load_static_data():
    """Load stops, routes, and transfers from static GTFS data."""
    stops = load_csv_to_dict("data/stops.txt", "stop_id")
    routes = load_csv_to_dict("data/routes.txt", "route_id")
    transfers = load_csv_to_list("data/transfers.txt")
    return stops, routes, transfers

def fetch_gtfs_feed(line):
    """Fetch GTFS data for a specific subway line."""
    if line not in FEED_URLS:
        raise ValueError(f"Invalid line code: {line}")

    url = FEED_URLS[line]
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content  # GTFS feed is in binary format
    except requests.exceptions.RequestException as e:
        print(f"Error fetching GTFS feed for line {line}: {e}")
        return None

def parse_gtfs_data(gtfs_binary):
    """Parse GTFS binary data."""
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(gtfs_binary)

    parsed_data = []
    for entity in feed.entity:
        if entity.trip_update:
            trip_id = entity.trip_update.trip.trip_id
            trip_data = {"trip_id": trip_id, "stops": []}

            for stop_time in entity.trip_update.stop_time_update:
                stop_id = stop_time.stop_id
                arrival_time = stop_time.arrival.time
                readable_time = datetime.datetime.fromtimestamp(arrival_time).strftime('%Y-%m-%d %H:%M:%S')
                trip_data["stops"].append({"stop_id": stop_id, "arrival_time": readable_time})

            parsed_data.append(trip_data)
    return parsed_data

def save_to_cache(data):
    """Save parsed data to a cache file."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f)
    print(f"Data cached in {CACHE_FILE}")

def load_from_cache():
    """Load data from the cache file."""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            print(f"Loading cached data from {CACHE_FILE}")
            return json.load(f)
    print("No cached data found.")
    return None

if __name__ == "__main__":
    line = "ACE"
    gtfs_binary = fetch_gtfs_feed(line)

    if gtfs_binary:
        print("\n--- Parsing GTFS Data ---\n")
        parsed_data = parse_gtfs_data(gtfs_binary)
        save_to_cache(parsed_data)
    else:
        print("Fetching failed. Attempting to load from cache.")
        parsed_data = load_from_cache()

    if parsed_data:
        print("\n--- Parsed Data ---\n")
        print(parsed_data)
