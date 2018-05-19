"""
Load and index states from a JSON lines file
"""
from collections import namedtuple
import json
from typing import Dict

from rtree import index
from shapely.geometry.polygon import Polygon
from shapely.geometry import Point

# A state consists of a name and a polygon
State = namedtuple('State', 'name polygon')

def read_json_lines(f):
    """
    Read data from a JSON lines file

    Parameters
    ----------
    f : File
       A file object from which to read data

    Yields
    ------
    dict
        Parsed data from lines in the file
    """
    for line in f:
        yield json.loads(line)

def create_states(shapes):
    """
    Create States

    Parameters
    ----------
    shapes : iterable of dicts
        Data in the format:
            {
                "state": "<state name>",
                "border": [[<lon_0>, <lat_0>], ..., [<lon_n>, <lat_n>]]
            }

    Yields
    ------
    State
        a State representing the data
    """
    for shape in shapes:
        yield State(name=shape["state"], polygon=Polygon(shell=shape["border"]))

class StateIndex:
    """
    An r-tree index for fast State lookups
    """
    def __init__(self) -> None:
        self.idx = index.Index()

    @classmethod
    def build_from_json_lines(cls, f):
        """
        Build a StateIndex from a JSON lines file

        Parameters
        ----------
        f : File
            A file object from which to read state data
        """
        index = cls()
        index.load(create_states(read_json_lines(f)))
        return index

    def load(self, states) -> None:
        """
        Load states into the index

        Parameters
        ----------
        states : iterable of State
            States to add to the index
        """
        for i, state in enumerate(states):
            self.idx.insert(i, state.polygon.bounds, obj=state)

    def get_containing_states(self, lon: float, lat: float):
        """
        Get all states (hopefully just one!) that intersect a point

        Yields
        ------
        str
            The name of the state containing the point
        """
        search_point = Point(lon, lat)

        # Iterate through intersections between this point and States' bounding
        # boxes
        for result in self.idx.intersection((lon, lat, lon + 1, lat + 1), objects=True):
            # Yield the state's name if it contains the search point
            if result.object.polygon.contains(search_point):
                yield result.object.name
