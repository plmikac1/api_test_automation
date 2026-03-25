import pytest
import sys
import os
sys.path.insert(0, os.path.abspath('../src'))
from neows_client import NeoWsClient

@pytest.fixture(scope="session")
def client():
    return NeoWsClient()
