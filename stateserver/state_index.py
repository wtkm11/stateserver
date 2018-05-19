"""
Load and index states from a JSON lines file
"""
import json
from typing import Dict

from rtree import index
from shapely.geometry.polygon import Polygon

class State(Polygon):
    """ A State is a polygon with a name """
    def __init__(name: str, *args, **kwargs) -> None:
        self.name = name
        super().__init__(*args, **kwargs)

def read_json_lines(f):
    """ Read data from a JSON lines file """
    for line in f.read_lines():
        yield json.loads(line)

def create_states(shapes):
    """
    Create States from an iterable of dicts of the format:
        {
            "state": "<state name>",
            "border": [[<lon_0>, <lat_0>], ..., [<lon_n>, <lat_n>]]
        }
    """
    for shape in shapes:
        try:
            yield State(shape["state"], shape["border"])
        except:
            pass

class StateIndex:
    def __init__(self) -> None:
        self.idx = index.Index()
        print("creating index")

    def load(self, states) -> None:
        """
        Load states into the index
        """
        for state in states:
            self.idx.insert(bounds=state.bounds, obj=state)

    def get_containing_states(self, lat: float, lon: float):
        """
        Get all states (hopefully just one!) that intersect a point
        """
        search_point = Point(lon, lat)
        for result in self.idx.intersection((lon, lat, lon, lat), objects=True):
            if result.object.contains(search_point):
                yield result.object.name

def build_index_from_json_lines(f):
    index = StateIndex()
    index.load(create_states(read_json_lines(f)))
    return index
