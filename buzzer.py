import time
import threading
import paho.mqtt.client as mqtt

C4, D4, E4, F4, G4, A4, B4, C5 = 262, 294, 330, 349, 392, 440, 494, 523
Q, HN = 0.45, 0.90
MELODY = [
    (E4, Q), (E4, Q), (F4, Q), (G4, Q), (G4, Q), (F4, Q), (E4, Q), (D4, Q),
    (C4, Q), (C4, Q), (D4, Q), (E4, Q), (E4, Q), (D4, Q), (D4, HN),
    (E4, Q), (E4, Q), (F4, Q), (G4, Q), (G4, Q), (F4, Q), (E4, Q), (D4, Q),
    (C4, Q), (C4, Q), (D4, Q), (E4, Q), (D4, Q), (C4, Q), (C4, HN),
]
GAP = 0.06

playing = False
armed = True
client = None

def play_note(freq_hz, dur_s):
    client.publish("/devices/buzzer/controls/frequency/on", str(int(freq_hz)), qos=1)
    client.publish("/devices/buzzer/controls/enabled/on", "1", qos=1)
    time.sleep(dur_s)
    client.publish("/devices/buzzer/controls/enabled/on", "0", qos=1)
    time.sleep(GAP)

def play_melody():
    global playing
    playing = True
    try:
        for f, d in MELODY:
            play_note(f, d)
    finally:
        playing = False

def on_connect(c, u, flags, rc, props=None):
    print(f"Connected rc={rc}")
    c.subscribe("/devices/wb-msw-v3_64/controls/Sound Level", qos=1)

def on_message(c, u, msg):
    global armed
    try:
        level = float(msg.payload.decode(errors="replace"))
    except ValueError:
        return
    if armed and (level > 60.0) and not playing:
        threading.Thread(target=play_melody, daemon=True).start()
        armed = False
    elif level < 55.0:
        armed = True

def main():
    global client
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("192.168.1.90", 1883, 60)
    client.loop_start()
    try:
        while True:
            time.sleep(1)
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()
