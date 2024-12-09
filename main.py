from src.gtfs_parser import fetch_gtfs_feed, parse_gtfs_data, save_to_cache, load_from_cache
from src.graph_builder import build_graph
from src.dijkstra import dijkstra

def main():
    # Define subway line and fetch data
    line = "ACE"
    print(f"Fetching GTFS data for line: {line}")
    gtfs_binary = fetch_gtfs_feed(line)

    # Parse and cache GTFS data
    if gtfs_binary:
        print("Parsing GTFS data...")
        parsed_data = parse_gtfs_data(gtfs_binary)
        save_to_cache(parsed_data)
    else:
        print("Fetching failed. Attempting to load from cache...")
        parsed_data = load_from_cache()

    # Build the subway graph
    if parsed_data:
        print("Building graph...")
        subway_graph = build_graph(parsed_data)

        # User input for start and end stations
        start_stop = input("Enter the start station (Stop ID): ")
        end_stop = input("Enter the end station (Stop ID): ")

        # Find the fastest route
        print("Calculating the fastest route...")
        distance, path = dijkstra(subway_graph, start_stop, end_stop)

        if path:
            print("\n--- Fastest Route ---")
            print(f"Fastest route from {start_stop} to {end_stop}:")
            print(" -> ".join(path))
            print(f"Total travel time: {distance} seconds")
        else:
            print(f"No route found from {start_stop} to {end_stop}.")
    else:
        print("No data available for processing.")

if __name__ == "__main__":
    main()
