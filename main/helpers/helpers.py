import requests
import json

def route_request(origin_lat, origin_lng, destination_lat, destination_lng,travel_mode,api_key):
    # API endpoint URL
    url = "https://routes.googleapis.com/directions/v2:computeRoutes"

    # Request payload
    payload = {
        "origin": {
            "location": {
                "latLng": {
                    "latitude": origin_lat,
                    "longitude": origin_lng
                }
            }
        },
        "destination": {
            "location": {
                "latLng": {
                    "latitude": destination_lat,
                    "longitude": destination_lng
                }
            }
        },
        "travelMode": travel_mode,
        # "routingPreference": "TRAFFIC_AWARE",
        # "departureTime": "2023-10-15T15:01:23.045123456Z",
        # "computeAlternativeRoutes": False,
        # "routeModifiers": {
        #     "avoidTolls": False,
        #     "avoidHighways": False,
        #     "avoidFerries": False
        # },
        "languageCode": "en-US",
        "units": "METRIC"
    }

    # HTTP headers
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "routes.duration,routes.distanceMeters,routes.polyline.encodedPolyline"
    }

    # Make the POST request
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    # Return the response
    return response.json()



def response_parser(response):
    routes_distanceMeters = []
    routes_duration = []
    routes_encodedPolyline = []

    try:
        routes_info = response.get("routes")
        if routes_info:
            for route in routes_info:
                routes_distanceMeters.append(route.get("distanceMeters"))
                routes_duration.append(route.get("duration"))
                routes_encodedPolyline.append(route.get("polyline", {}).get("encodedPolyline"))
    except KeyError:
        # Trate aqui o caso em que a chave 'routes' não está presente
        return {"DistanceMeters": [], "Duration": [], "EncodedRoutes": []}

    return {"DistanceMeters": routes_distanceMeters, "Duration": routes_duration, "EncodedRoutes": routes_encodedPolyline}


