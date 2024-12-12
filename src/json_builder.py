import csv

def load_csv_to_dict(file_path, key_field):
    """Load a CSV file into a dictionary keyed by the specified field."""
    data = {}
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data[row[key_field]] = row
    return data

def load_csv_to_list(file_path):
    """Load a CSV file into a list of dictionaries."""
    data = []
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

stops = load_csv_to_dict("data/stops.txt", "stop_id")
shapes = load_csv_to_list("data/shapes.txt")  # For visualization
routes = load_csv_to_dict("data/routes.txt", "route_id")
transfers = load_csv_to_list("data/transfers.txt")
