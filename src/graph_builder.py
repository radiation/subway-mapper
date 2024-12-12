from collections import defaultdict
import datetime

def add_transfers_to_graph(graph, transfers):
    """Add transfer edges to the graph."""
    for transfer in transfers.values():
        from_stop = transfer["from_stop_id"]
        to_stop = transfer["to_stop_id"]
        transfer_time = int(transfer["min_transfer_time"]) if transfer["min_transfer_time"] else 0
        if from_stop in graph:
            graph[from_stop].append((to_stop, transfer_time))

def build_graph(parsed_data, transfers):
    """Constructs a graph from parsed GTFS data and adds transfers."""
    graph = defaultdict(list)
    
    # Group stops by trip
    for trip in parsed_data:
        stops = trip["stops"]
        for i in range(len(stops) - 1):
            start_stop = stops[i]["stop_id"]
            end_stop = stops[i + 1]["stop_id"]
            
            # Ensure stops are part of the same trip
            start_time = datetime.datetime.strptime(stops[i]["arrival_time"], "%Y-%m-%d %H:%M:%S")
            end_time = datetime.datetime.strptime(stops[i + 1]["arrival_time"], "%Y-%m-%d %H:%M:%S")
            
            # Calculate travel time
            travel_time = int((end_time - start_time).total_seconds())
            if travel_time > 0:  # Ignore invalid or reversed times
                graph[start_stop].append((end_stop, travel_time))

    # Add transfers
    add_transfers_to_graph(graph, transfers)
    return graph
