from collections import defaultdict
import datetime

def add_transfers_to_graph(graph, transfers):
    """Add transfer edges to the graph."""
    for transfer in transfers:  # Iterate directly over the list
        from_stop = transfer["from_stop_id"]
        to_stop = transfer["to_stop_id"]
        transfer_time = int(transfer.get("min_transfer_time", 0))  # Default to 0 if missing

        # Add the transfer edge
        if from_stop in graph:
            graph[from_stop].append((to_stop, transfer_time))

def build_graph(parsed_data, transfers):
    """Constructs a graph from parsed GTFS data and adds transfers."""
    graph = defaultdict(dict)  # Use a dict of dicts to store minimum weights

    for trip in parsed_data:
        stops = trip["stops"]
        for i in range(len(stops) - 1):
            start_stop = stops[i]["stop_id"]
            end_stop = stops[i + 1]["stop_id"]

            start_time = datetime.datetime.strptime(stops[i]["arrival_time"], "%Y-%m-%d %H:%M:%S")
            end_time = datetime.datetime.strptime(stops[i + 1]["arrival_time"], "%Y-%m-%d %H:%M:%S")

            travel_time = int((end_time - start_time).total_seconds())
            if travel_time > 0:  # Ensure valid travel times
                # Only keep the minimum travel time for the edge
                if end_stop not in graph[start_stop] or graph[start_stop][end_stop] > travel_time:
                    graph[start_stop][end_stop] = travel_time

    # Convert dict of dicts to adjacency list
    adjacency_list = defaultdict(list)
    for start_stop, edges in graph.items():
        for end_stop, travel_time in edges.items():
            adjacency_list[start_stop].append((end_stop, travel_time))

    # Add transfers
    add_transfers_to_graph(adjacency_list, transfers)
    return adjacency_list
