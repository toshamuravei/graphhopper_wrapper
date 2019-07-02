from flask import Flask, request, jsonify, abort
from utils import extract_points_from_str, create_route_response, calculate_matrices, ask_for_key


app = Flask(__name__)


@app.route("/route", methods=["GET"])
@ask_for_key
def get_route():
    """
    Incoming argument is 'waypoints'. It is represented as
    string where at least 2 points are delimited with '|':
    'waypoints=57.152936,65.52547|57.158705,65.560656'
    """
    raw_wps = request.args.get("waypoints")
    if not raw_wps:
        abort(400)

    waypoints = extract_points_from_str(raw_wps)

    resp = create_route_response(waypoints)
    return jsonify(resp)


@app.route("/distancematrix", methods=["GET"])
@ask_for_key
def get_matrix():
    """
    Incoming arguments are 'origins' and 'destinations'.
    Both of them are represented in this format:
    'origins=57.152936,65.52547|57.158705,65.560656'
    """
    raw_origins = request.args.get("origins")
    raw_destinations = request.args.get("destinations")

    if not raw_origins or not raw_destinations:
        abort(400)

    origins = extract_points_from_str(raw_origins)
    destinations = extract_points_from_str(raw_destinations)
    resp = calculate_matrices(origins, destinations)

    return jsonify(resp)
