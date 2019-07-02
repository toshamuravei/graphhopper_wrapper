import settings
import requests
from functools import wraps
from typing import Dict, List
from flask import abort, request


def extract_points_from_str(points_text: str) -> List:
    """
    Function transforms text like '52.123,39.454|51.321,38.778'
    to nested list like [[52.123, 39.454], [51.321, 38.778]]
    """
    p = [list(map(lambda x: float(x), x.split(","))) for x in points_text.split("|")]
    return p


def get_graphhopper_route(points: List) -> List:
    """
    Function transforms points into specific string format,
    send request to GrassHopper Server and returns 'paths'
    list from its response:
    [{
        "distance": float,
        "weight": float,
        "time": int,
        "transfers": int,
        "points_encoded": bool,
        "bbox": [float, ],
        "points": {
            "type": str,
            "coordinates": [[float, float], ]
        },
        "legs": [],
        "details": {},
        "ascend": int,
        "descend": int,
        "snapped_waypoints": {
            "type": str,
            "coordinates": [[float, float], ]
        }
    }, ]
    """
    payload = []

    for point in points:
        payload.append(("point", "{},{}".format(*point)))

    payload += settings.gh_server.default_params
    address = "{}:{}/route".format(settings.gh_server.host, settings.gh_server.port)

    r = requests.get(address, params=payload)

    response = r.json()
    return response["paths"]


def calculate_matrices(origins:List, destinations: List) -> Dict:
    """
    Function gets lists of origin & destination points
    and calculates length/duration for every combination
    of origin-destination
    """
    matrices = []
    for o in origins:
        for d in destinations:
            row = {
                "duration": {"value":0},
                "status": "FAIL",
                "distance": {"value":0}
            }

            paths = get_graphhopper_route([o, d])
            if paths:
                row["distance"]["value"] = sum(item["distance"] for item in paths)
                row["duration"]["value"] = sum(item["time"] for item in paths)
                row["status"] = "OK"

            element = [row]
            matrices.append({"elements": element})

    return {"rows": matrices}


def create_route_response(points: List) -> Dict:
    """
    Get 'points' from every 'path'-dict and
    transform them into apropriate response
    """
    paths = get_graphhopper_route(points)
    resp = render_route_response_data(paths)

    return resp


def render_route_response_data(paths: List) -> Dict:
    """
    Transform GrassHopper data to suitable for client format
    """
    resp = {"route":
            {"legs":[
                {
                    "status": "OK",
                    "steps":[]
                }
            ]
        }
    }

    if not paths:
        resp["route"]["legs"][0]["status"] = "FAIL"
        return resp

    steps = []
    for path in paths:
        step = {
            "duration": path["time"],
            "length": path["distance"],
            "polyline":{
                "points": path["points"]["coordinates"]
            }
        }
        steps.append(step)

    resp["route"]["legs"][0]["steps"] = steps
    return resp


def ask_for_key(func):
    @wraps(func)
    def apikey_wrapper(*args, **kwargs):
        if settings.API_KEY != request.headers.get("x-api-key"):
            abort(401)
        return func(*args, **kwargs)
    return apikey_wrapper
