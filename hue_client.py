import os
from time import sleep

import requests
from dotenv import load_dotenv
from phue import Bridge

load_dotenv()


class HueClient:
    def __init__(self):
        self.bridge_ip = os.getenv("HUE_BRIDGE_IP", None)
        if self.bridge_ip is None:
            self.bridge_ip = self._get_by_ip_discover()
        self.bridge = Bridge(self.bridge_ip)

    def _connect(self):
        counter = 0
        while True:
            try:
                self.bridge.connect()
            except:
                raise Exception(
                    "Could not connect to bridge. Please press the button on the bridge and try again. I will wait 30 seconds.")
            sleep(30)
            counter += 1
            if counter > 5:
                print("Tried 5 times to connect to bridge. Giving up.")
                exit()

    def _get_by_ip_discover(self):
        try:
            data = requests.get("https://discovery.meethue.com/")
            if data.status_code != 200:
                return None
            data = data.json()
            return data[0]['internalipaddress']
        except:
            raise Exception("Could not find bridge. Please use ip address instead of discovery.")

    def get_lamps(self):
        return self.bridge.lights

    def get_lamp(self, lamp_id):
        return self.bridge.get_light(lamp_id)

    def set_brightness(self, lamp_id, brightness):
        # validate that number is between 0 and 100
        if brightness < 0:
            brightness = 0
        elif brightness > 100:
            brightness = 100
        # convert to 0-254
        brightness = int(brightness * 2.54)
        self.bridge.set_light(lamp_id, 'bri', brightness)

    def turn_on(self, lamp_id):
        self.bridge.set_light(lamp_id, 'on', True)

    def turn_off(self, lamp_id):
        self.bridge.set_light(lamp_id, 'on', False)

    def set_color_by_number(self, lamp_id, number):
        # check if number is between 0 and 65535
        number = max(0, min(number, 65535))

        self.bridge.set_light(lamp_id, 'hue', number)
