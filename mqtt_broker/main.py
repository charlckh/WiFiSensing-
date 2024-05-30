import paho.mqtt.client as mqtt
import json

payloads = {}

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("rssi/data")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    ssid, mac, rssi = [item.split(": ")[1] for item in payload.split(", ")]
    blacklist = ["CSL", "Y5ZONE", "Wi-Fi.HK", "eduroam"]
    if any(keyword in ssid for keyword in blacklist):
        # If it does, skip the rest of the function and do not save the payload
        return
    print(msg.topic+" "+str(msg.payload))
    # Check if the (SSID, MAC) tuple is already in the dictionary
    key = f"{ssid}-{mac}"
    if key in payloads:
        # If it is, append the RSSI to the existing list
        payloads[key].append(rssi)
    else:
        # If it's not, create a new list with the RSSI as the first element
        payloads[key] = [rssi]
    with open('payloads.txt', 'w') as f:
        # Convert the payloads dictionary to a JSON string and write it to the file
        f.write(json.dumps(payloads) + '\n')


mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="3035685677")
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("localhost", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
mqttc.loop_forever()




