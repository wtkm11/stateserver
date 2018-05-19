import json

from flask import Flask, request, g

from stateserver.state_index import convert_shape_data, read_json_lines, StateIndex
from stateserver.config import Config

app = Flask(__name__)
app.config.from_object(Config)

def get_state_index():
    states = getattr(g, 'states', None)
    if not states:
        with open(app.config.STATE_DATA_PATH) as f:
            states = build_index_from_json_lines(f)
    return states

@app.route("/")
def state_point_intersection() -> str:
    """ Find states that intersect a point """
    empty = "[]"  # The response to return when no states are found

    # Get the latitude and longitude from the request
    try:
        lat = float(request.args["latitude"])
        lon = float(request.args["longitude"])
    except KeyError:
        app.logger.debug(
            "The latitude or longitude was omitted from the query string."
        )
        return empty

    # If the latitude or longitude is out of bounds, skip the query
    if lat > 90 or lat < -90 or lon > 180 or lon < -180:
        return empty

    return json.dumps(["Pennsylvania"])

def main() -> None:
    g.states = get_state_index()
    app.run(host="0.0.0.0", port=9001)
