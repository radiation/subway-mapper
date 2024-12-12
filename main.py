from src.gtfs_parser import fetch_gtfs_feed, parse_gtfs_data, save_to_cache, load_static_data, FEED_URLS
from src.graph_builder import build_graph
from src.dijkstra import dijkstra

def main():
    parsed_data = []
    for line in FEED_URLS.keys():
        print(f"Fetching GTFS data for line: {line}")
        gtfs_binary = fetch_gtfs_feed(line)
        if gtfs_binary:
            parsed_data.extend(parse_gtfs_data(gtfs_binary))

    save_to_cache(parsed_data)

    # Load static GTFS data
    stops, routes, transfers = load_static_data()

    # Build the subway graph
    subway_graph = build_graph(parsed_data, transfers)

    # User input for start and end stations
    start_stop = input("Enter the start station (Stop ID): ")
    end_stop = input("Enter the end station (Stop ID): ")

    # Find the fastest route
    distance, path = dijkstra(subway_graph, start_stop, end_stop)

    if path:
        print(" -> ".join(path))
        print(f"Total travel time: {distance} seconds")
    else:
        print("No route found.")

if __name__ == "__main__":
    main()
