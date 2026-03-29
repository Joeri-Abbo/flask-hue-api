import json
import sys
import pytest
from unittest.mock import MagicMock, patch


def _make_env(key, default=None):
    """Return env values suitable for testing (no real bridge or Sentry)."""
    mapping = {
        "HUE_BRIDGE_IP": "192.168.1.1",
        "SENTRY_DSN": None,
        "DEBUG": "False",
        "PORT": "5000",
        "HOST": "0.0.0.0",
    }
    return mapping.get(key, default)


@pytest.fixture(scope="module")
def flask_app():
    # Remove cached app module so we can reload with mocks active
    for mod in list(sys.modules.keys()):
        if mod in ("app", "hue_client"):
            del sys.modules[mod]

    with patch("phue.Bridge") as mock_bridge_cls, \
         patch("os.getenv", side_effect=_make_env):
        mock_bridge = MagicMock()
        mock_bridge_cls.return_value = mock_bridge

        import app as app_module

        flask_app = app_module.app
        flask_app.config["TESTING"] = True
        yield flask_app, app_module.client, mock_bridge


@pytest.fixture
def client(flask_app):
    app, hue_client, mock_bridge = flask_app
    return app.test_client(), hue_client, mock_bridge


def test_get_lamps_success(client):
    test_client, hue_client, _ = client
    with patch.object(hue_client, "get_lamps", return_value=[MagicMock()]):
        response = test_client.get("/")
    assert response.status_code == 200
    assert json.loads(response.data)["message"] == "Lamps cleaned up"


def test_get_lamps_failure(client):
    test_client, hue_client, _ = client
    with patch.object(hue_client, "get_lamps", side_effect=Exception("No bridge")):
        response = test_client.get("/")
    assert response.status_code == 404
    assert json.loads(response.data)["message"] == "Lamps not found"


def test_get_lamp_success(client):
    test_client, hue_client, _ = client
    with patch.object(hue_client, "get_lamp", return_value={"state": {"on": True}}):
        response = test_client.get("/1")
    assert response.status_code == 200


def test_get_lamp_not_found(client):
    test_client, hue_client, _ = client
    with patch.object(hue_client, "get_lamp", side_effect=Exception("Not found")):
        response = test_client.get("/999")
    assert response.status_code == 404
    assert json.loads(response.data)["message"] == "Lamp not found"


def test_turn_on_success(client):
    test_client, hue_client, _ = client
    with patch.object(hue_client, "turn_on"):
        response = test_client.put("/turn-on/1")
    assert response.status_code == 200
    assert json.loads(response.data)["message"] == "Turn lamp on"


def test_turn_on_failure(client):
    test_client, hue_client, _ = client
    with patch.object(hue_client, "turn_on", side_effect=Exception("Not found")):
        response = test_client.put("/turn-on/999")
    assert response.status_code == 404


def test_turn_off_success(client):
    test_client, hue_client, _ = client
    with patch.object(hue_client, "turn_off"):
        response = test_client.put("/turn-off/1")
    assert response.status_code == 200
    assert json.loads(response.data)["message"] == "Turn lamp off"


def test_turn_off_failure(client):
    test_client, hue_client, _ = client
    with patch.object(hue_client, "turn_off", side_effect=Exception("Not found")):
        response = test_client.put("/turn-off/999")
    assert response.status_code == 404


def test_set_color_success(client):
    test_client, hue_client, _ = client
    with patch.object(hue_client, "set_color_by_number"):
        response = test_client.put("/set-color/1/32000")
    assert response.status_code == 200
    assert json.loads(response.data)["message"] == "Color changed"


def test_set_color_failure(client):
    test_client, hue_client, _ = client
    with patch.object(hue_client, "set_color_by_number", side_effect=Exception("Not found")):
        response = test_client.put("/set-color/999/32000")
    assert response.status_code == 404
