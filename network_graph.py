import csv
import json

stops_csv = 'stops.txt'
trips_csv = 'trips.txt'
stop_times_csv = 'stop_times.txt'

stops = {}
routes = {}

with open(stops_csv, mode='r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        stop_id = row['stop_id']
        stops[stop_id] = {
            'stop_id': stop_id,
            'stop_name': row['stop_name'],
            'stop_lat': row['stop_lat'],
            'stop_lon': row['stop_lon'],
            'routes': set() 
        }

with open(trips_csv, mode='r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        trip_id = row['trip_id']
        route_id = row['route_id']
        if route_id not in routes:
            routes[route_id] = []
        routes[route_id].append(trip_id)

edges = []
with open(stop_times_csv, mode='r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    last_stop_id = None
    for row in reader:
        trip_id = row['trip_id']
        stop_id = row['stop_id']
        for route_id, trips in routes.items():
            if trip_id in trips:
                stops[stop_id]['routes'].add(route_id)
                break
        if last_stop_id and last_stop_id[0] == trip_id:
            edge = {'source': last_stop_id[1], 'target': stop_id}
            if edge not in edges: 
                edges.append(edge)
        last_stop_id = (trip_id, stop_id)

for stop in stops.values():
    stop['routes'] = list(stop['routes'])

graph_data = {
    'nodes': list(stops.values()),
    'links': edges
}

with open('transit_network_graph.json', 'w', encoding='utf-8') as f:
    json.dump(graph_data, f, ensure_ascii=False, indent=4)

print("JSON file created successfully!")
