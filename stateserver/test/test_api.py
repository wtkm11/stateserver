"""
Tests of API
"""
from unittest import TestCase
from stateserver.app import app, state_point_intersection

client = app.test_client()

def test_no_query_string():
    """
    Test that an empty results list is returned if the query string is omitted
    """
    resp = client.get("/")
    assert resp.data == b"[]"

def test_out_of_bounds():
    """
    Test that an empty results list is returned for out of bounds queries
    """
    resp = client.get("/?latitude=9001&longitude=9001")
    assert resp.data == b"[]"

def test_in_pa():
    """
    Test that a point in Philadelphia is inside Pennsylvania
    """
    resp = client.get("/?latitude=39.9493182&longitude=-75.1653888")
    assert resp.data == b'["Pennsylvania"]'
