def display_route(route, stops):
    """Pretty-print the route with stop names."""
    print("\n--- Fastest Route ---")
    for stop_id in route:
        stop_name = stops.get(stop_id, {}).get("stop_name", "Unknown Stop")
        print(f"{stop_id} ({stop_name})")
