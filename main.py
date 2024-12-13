from src.gtfs_parser import fetch_gtfs_feed, parse_gtfs_data, save_to_cache, load_static_data, get_station_name, FEED_URLS
from src.graph_builder import build_graph
from src.dijkstra import dijkstra

def display_travel_time(seconds):
    """Convert seconds to minutes and seconds."""
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes} minutes and {remaining_seconds} seconds"

def display_edges(node, edges, stops):
    """Display edges from a node with station names."""
    print(f"Edges from {node} ({get_station_name(node, stops)}):")
    for edge, travel_time in edges:
        edge_name = get_station_name(edge, stops)
        print(f"  -> {edge} ({edge_name}): {travel_time} seconds")

def display_route_with_transfers(path, times, stops, routes):
    """Pretty-print the route with station names, travel times, and transfers."""
    print("\n--- Fastest Route ---")
    
    for i in range(len(path) - 1):
        start = path[i]
        end = path[i + 1]
        travel_time = times[i]

        # Get the route for the current stop and next stop
        start_route = routes.get(start, "Unknown Route")
        end_route = routes.get(end, "Unknown Route")

        # Print the current stop
        print(f"{start} ({get_station_name(start, stops)}) - {start_route}")

        # Check for transfer at the current stop
        if start_route != end_route:
            print(f"   | Transfer to {end_route} at {get_station_name(start, stops)}")

        # Print the travel time to the next stop
        if travel_time is not None:
            print(f"   | {travel_time} seconds")
        else:
            print(f"   | Travel time unavailable to {end} ({get_station_name(end, stops)})")

    # Print the final stop
    print(f"{path[-1]} ({get_station_name(path[-1], stops)}) - {routes.get(path[-1], 'Unknown Route')}")

def get_travel_time(graph, start, end):
    """Retrieve the travel time between two stops."""
    for neighbor, travel_time in graph[start]:
        if neighbor == end:
            return travel_time
    return None  # Return None if no direct connection is found

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
    start_name = get_station_name(start_stop, stops)
    print(f"Start Station: {start_name} ({start_stop})")

    end_stop = input("Enter the end station (Stop ID): ")
    end_name = get_station_name(end_stop, stops)
    print(f"End Station: {end_name} ({end_stop})")

    edges = subway_graph.get(start_stop, [])
    display_edges(start_stop, edges, stops)

    # Find the fastest route
    distance, path = dijkstra(subway_graph, start_stop, end_stop)

    if path:
        # Calculate travel times for each segment
        times = [get_travel_time(subway_graph, start, end) for start, end in zip(path[:-1], path[1:])]
        display_route_with_transfers(path, times, stops, routes)
        print(f"Total travel time: {display_travel_time(distance)}")
    else:
        print(f"No route found from {start_stop} to {end_stop}.")


if __name__ == "__main__":
    main()
