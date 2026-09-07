from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(scope="session")
def initial_activities():
    return deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def isolate_activities(initial_activities):
    app_module.activities = deepcopy(initial_activities)
    yield
    app_module.activities = deepcopy(initial_activities)


@pytest.fixture
def client():
    return TestClient(app_module.app)