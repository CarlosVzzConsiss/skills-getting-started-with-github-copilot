import copy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module


@pytest.fixture
def client():
    original_activities = copy.deepcopy(app_module.activities)
    client = TestClient(app_module.app)

    try:
        yield client
    finally:
        app_module.activities = original_activities
