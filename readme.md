# Hue Lamp Control API
The Hue Lamp Control API is a Flask-based web service that allows you to control Philips Hue smart lamps connected to your local network. This project provides a simple RESTful API to interact with your Hue lamps, enabling you to perform various actions such as turning them on or off, adjusting brightness, and changing colors. The API can be easily integrated into your home automation or smart lighting projects.

## Getting Started
To set up and run the Hue Lamp Control API, follow these steps:

### Prerequisites
- Python 3.x
- Flask
- Phue (Python library for controlling Philips Hue)
- FlaskClient (Custom Flask client for configuring the API)
You also need to have a Philips Hue bridge connected to your local network. Make sure you know the IP address of your Hue bridge, or you can use the automatic discovery feature provided by the API.

### Installation
Clone this repository to your local machine:

```bash
git clone git@github.com:Joeri-Abbo/flask-hue-api.git
```
Navigate to the project directory:

```bash
cd flask-hue-api
```
Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```
Create a .env file in the project directory and add your Hue bridge IP address:

```bash
HUE_BRIDGE_IP=your_bridge_ip
```
If you don't know your bridge's IP address, you can leave this field empty, and the API will attempt to discover it automatically.

### Usage
Start the API by running the app.py script:

```bash
python app.py
```
The API will run on the specified host and port (default is localhost:5000).

You can now use HTTP requests to interact with your Hue lamps. Here are some example API endpoints:

- GET /: Get a list of all available lamps.

- GET /<lamp_id>: Get details about a specific lamp by its ID.

- PUT /set-color/<lamp_id>/<color>: Set the color of a lamp (provide color as a numeric value between 0 and 65535).

- PUT /set-brightness/<lamp_id>/<brightness>: Set the brightness of a lamp (provide brightness as a numeric value between 0 and 100).

- PUT /turn-on/<lamp_id>: Turn on a lamp.

- PUT /turn-off/<lamp_id>: Turn off a lamp.

### Error Handling
The API provides basic error handling for scenarios where a requested action cannot be performed. If a lamp is not found or an operation fails, the API will return a JSON response with an appropriate error message and a status code of 404.
