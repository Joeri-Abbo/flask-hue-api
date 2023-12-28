from Clients import FlaskClient
from flask import jsonify
from hue_client import HueClient

flask_client = FlaskClient()
app = flask_client.get_client()
client = HueClient()


@app.route('/', methods=['GET'])
def route_get_lamps():
    try:
        client.get_lamps()
    except:
        return jsonify(
            {
                "message": "Lamps not found"
            }
        ), 404

    return jsonify(
        {
            "message": "Lamps cleaned up"
        }
    )


@app.route('/<key>', methods=['GET'])
def route_get_lamp(key):
    try:
        lamp = client.get_lamp(key)
    except:
        return jsonify(
            {
                "message": "Lamp not found"
            }
        ), 404
    return jsonify(
        lamp
    )


@app.route('/set-color/<key>/<color>', methods=['PUT'])
def route_set_lamp_color(key, color):
    try:
        client.set_color_by_number(key, color)
    except:
        return jsonify(
            {
                "message": "Lamp not found"
            }
        ), 404
    return jsonify(
        {
            "message": "Color changed"
        }
    )


@app.route('/set-color/<key>/<brightness>', methods=['PUT'])
def route_set_lamp_brightness(key, brightness):
    try:
        client.set_brightness(key, brightness)
    except:
        return jsonify(
            {
                "message": "Lamp not found"
            }
        ), 404
    return jsonify(
        {
            "message": "Brightness changed"
        }
    )


@app.route('/turn-on/<key>', methods=['PUT'])
def route_set_lamp_turn_on(key):
    try:
        client.turn_on(key)
    except:
        return jsonify(
            {
                "message": "Lamp not found"
            }
        ), 404
    return jsonify(
        {
            "message": "Turn lamp on"
        }
    )


@app.route('/turn-off/<key>', methods=['PUT'])
def route_set_lamp_turn_off(key):
    try:
        client.turn_off(key)
    except:
        return jsonify(
            {
                "message": "Lamp not found"
            }
        ), 404
    return jsonify(
        {
            "message": "Turn lamp off"
        }
    )


if __name__ == '__main__':
    app.run(
        port=flask_client.get_port(),
        debug=flask_client.get_debug(),
        host=flask_client.get_host()
    )
