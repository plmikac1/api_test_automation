from datetime import datetime, timedelta

import pytest
import requests


# Testy specyficzne NeoWs
def test_browse_endpoint_returns_data(client):
    data = client.get_browse()
    client.save_json_to_file(data, "responses/browse_page_0.json")
    assert data["page"]["total_elements"] > 0
    assert len(data["near_earth_objects"]) > 0


def test_feed_endpoint_for_today_returns_data(client):
    today = datetime.now().strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    data = client.get_feed(start_date=today, end_date=tomorrow)
    assert "near_earth_objects" in data


def test_neo_lookup_returns_data(client):
    neo_id = 2001620
    data = client.get_neo(neo_id=neo_id)
    print(data)
    assert int(data["id"]) == neo_id
    assert "name" in data


@pytest.mark.negative
def test_invalid_neo_id_returns_404(client):
    with pytest.raises(requests.exceptions.HTTPError):
        client.get_neo(neo_id=999999999)


# Testy uniwersalne HTTP
def test_generic_get_browse(client):
    data = client.get("neo/browse", params={"page": 0})
    assert data["page"]["total_elements"] > 0


def test_generic_get_feed(client):
    data = client.get("feed", params={"start_date": "2026-03-19"})
    assert "element_count" in data


@pytest.mark.negative
def test_put_returns_405_method_not_allowed(client):
    """NASA NeoWs read-only, PUT zwraca 405."""
    with pytest.raises(requests.exceptions.HTTPError, match="401"):
        client.put("neo/browse", json_data={"test": True})


@pytest.mark.negative
def test_patch_returns_405_method_not_allowed(client):
    with pytest.raises(requests.exceptions.HTTPError, match="405"):
        client.patch("neo/browse")
