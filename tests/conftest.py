import pytest
import os
from datetime import datetime
from pathlib import Path
from neows_client import NeoWsClient

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_name = f"reports/report_{timestamp}.html"
    Path("reports").mkdir(exist_ok=True)
    config.option.htmlpath = report_name  # Overrides --html from pyproject.toml


@pytest.fixture(scope="session")
def client():
    return NeoWsClient()
