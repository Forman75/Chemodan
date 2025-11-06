import paho.mqtt.publish as publish

cmd = input("on/off/rgb? ").strip().lower()
if cmd == "on":
    publish.single(f"/devices/wb-led_39/controls/RGB Strip/on", payload="1", hostname="192.168.1.90")
elif cmd == "off":
    publish.single(f"/devices/wb-led_39/controls/RGB Strip/on", payload="0", hostname="192.168.1.90")
elif cmd == "rgb":
    r,g,b = input("R G B: ").split()
    publish.single(f"/devices/wb-led_39/controls/RGB Palette/on", payload=f"{int(r)};{int(g)};{int(b)}", hostname="192.168.1.90")
else:
    print("Неизвестная команда")