from collections import defaultdict
import datetime

def build_graph(parsed_data):
    """Constructs a graph from parsed GTFS data."""
    graph = defaultdict(list)
    
    for trip in parsed_data:
        stops = trip["stops"]
        for i in range(len(stops) - 1):
            start_stop = stops[i]["stop_id"]
            end_stop = stops[i + 1]["stop_id"]
            
            # Calculate travel time in seconds
            start_time = datetime.datetime.strptime(stops[i]["arrival_time"], "%Y-%m-%d %H:%M:%S")
            end_time = datetime.datetime.strptime(stops[i + 1]["arrival_time"], "%Y-%m-%d %H:%M:%S")
            travel_time = int((end_time - start_time).total_seconds())
            
            # Add edge to the graph
            graph[start_stop].append((end_stop, travel_time))
    return graph
