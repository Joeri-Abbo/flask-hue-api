import pytest
from unittest.mock import MagicMock, patch, call


@pytest.fixture
def hue_client():
    with patch("hue_client.Bridge") as mock_bridge_cls, \
         patch("hue_client.os.getenv", return_value="192.168.1.1"):
        mock_bridge = MagicMock()
        mock_bridge_cls.return_value = mock_bridge

        from hue_client import HueClient
        client = HueClient()
        client.bridge = mock_bridge
        return client, mock_bridge


def test_turn_on(hue_client):
    client, mock_bridge = hue_client
    client.turn_on(1)
    mock_bridge.set_light.assert_called_with(1, "on", True)


def test_turn_off(hue_client):
    client, mock_bridge = hue_client
    client.turn_off(1)
    mock_bridge.set_light.assert_called_with(1, "on", False)


def test_set_brightness_normal(hue_client):
    client, mock_bridge = hue_client
    client.set_brightness(1, 50)
    # 50 * 2.54 = 127
    mock_bridge.set_light.assert_called_with(1, "bri", 127)


def test_set_brightness_clamps_low(hue_client):
    client, mock_bridge = hue_client
    client.set_brightness(1, -10)
    # clamped to 0 * 2.54 = 0
    mock_bridge.set_light.assert_called_with(1, "bri", 0)


def test_set_brightness_clamps_high(hue_client):
    client, mock_bridge = hue_client
    client.set_brightness(1, 200)
    # clamped to 100 * 2.54 = 254
    mock_bridge.set_light.assert_called_with(1, "bri", 254)


def test_set_color_by_number_normal(hue_client):
    client, mock_bridge = hue_client
    client.set_color_by_number(1, 32000)
    mock_bridge.set_light.assert_called_with(1, "hue", 32000)


def test_set_color_by_number_clamps_low(hue_client):
    client, mock_bridge = hue_client
    client.set_color_by_number(1, -100)
    mock_bridge.set_light.assert_called_with(1, "hue", 0)


def test_set_color_by_number_clamps_high(hue_client):
    client, mock_bridge = hue_client
    client.set_color_by_number(1, 99999)
    mock_bridge.set_light.assert_called_with(1, "hue", 65535)


def test_get_lamps(hue_client):
    client, mock_bridge = hue_client
    mock_bridge.lights = [MagicMock(), MagicMock()]
    result = client.get_lamps()
    assert result == mock_bridge.lights


def test_get_lamp(hue_client):
    client, mock_bridge = hue_client
    mock_bridge.get_light.return_value = {"state": {"on": True}}
    result = client.get_lamp(1)
    mock_bridge.get_light.assert_called_with(1)
    assert result == {"state": {"on": True}}
