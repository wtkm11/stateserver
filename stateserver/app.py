import json

import falcon

from stateserver.config import Config
from stateserver.resources import PointInStateResource
from stateserver.state_index import StateIndex

api = falcon.API()

# Load state boundary data into the state index
with open(Config.STATE_DATA_PATH) as f:
    states = StateIndex.build_from_json_lines(f)

api.add_route("/", PointInStateResource(states))
