from time import sleep

from hue_client import HueClient

client = HueClient()
lamps = client.get_lamps()

while True:
    # lamps = [1]
    lamps = [16, 17, 18]

    for i in range(100, 0, -1):
        for lamp in lamps:
            client.set_brightness(lamp, i)
        # sleep(0.1)
        print(i)
    for i in range(0, 100, 1):
        for lamp in lamps:
            client.set_brightness(lamp, i)
        # sleep(0.1)
        print(i)



#
# for lamp in lamps:
#     l = client.get_lamp(lamp.light_id)
#     # print(l)
#     print(
#         lamp.light_id,
#         lamp.name,
#         lamp.on,
#         # lamp.brightness,
#         # lamp.colormode
#     )
#
# print(lamps)
# exit()
# client.set_brightness(1, 50)
# client.turn_on(1)
# # 0-65535
# while True:
#     for i in range(0, 65535, 1):
#         client.set_color_by_number(1, i)
#         print(i)
#         # sleep(0.1)
# # client.set_color_by_number(1, 65535)
# print(client.get_lamp(1))
