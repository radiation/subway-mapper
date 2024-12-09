import heapq

def dijkstra(graph, start, end):
    """Find the shortest path using Dijkstra's algorithm."""
    priority_queue = [(0, start, [])]  # (current_distance, current_node, path)
    visited = set()
    
    while priority_queue:
        current_distance, current_node, path = heapq.heappop(priority_queue)
        
        if current_node in visited:
            continue
        visited.add(current_node)
        path = path + [current_node]
        
        # If we reached the destination, return the result
        if current_node == end:
            return current_distance, path
        
        # Explore neighbors
        for neighbor, weight in graph[current_node]:
            if neighbor not in visited:
                heapq.heappush(priority_queue, (current_distance + weight, neighbor, path))
    
    return float("inf"), []  # No path found
