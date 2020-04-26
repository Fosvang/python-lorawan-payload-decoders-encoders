import base64

def decode(port, data):
    lat = (data[0] << 24 | data[1] << 16 | data[2] << 8 | data[3]) / 1000000
    lon = (data[4] << 24 | data[5] << 16 | data[6] << 8 | data[7]) / 1000000
    location = f"({lat},{lon})"
    alarm = (data[8] & 0x40) > 0
    battery = ((data[8] & 0x3f)<<8 | data[9]) / 1000
    motion = { 0: "Disable", 1: "Move", 2: "Collide", 3: "Custom" }[data[10]>>6]
    firmware = 150+(data[10] & 0x1f)
    led = "ON" if (data[10] & 0x20) else "OFF"
    roll = 0
    pitch = 0
    if (len(data) >= 14):
        roll = (data[11]<<24>>16 | data[12]) / 100
        pitch = (data[13]<<24>>16 | data[14]) / 100
    return [
        {"field": "LOCATION", "value": location},
        {"field": "ALARM", "value": alarm},
        {"field": "BATTERY", "value": battery},
        {"field": "MOTION", "value": motion},
        {"field": "FIRMWARE", "value": firmware, "meta": True},
    ]

# b = bytes.fromhex("0319E8AC0067F52B0F7A63")
# b = base64.b64encode(b)

# Wenn von TTN kommt dann:
payload = base64.b64decode("AxnorABn9SsPemM=")
r = decode(1, payload)
for field in r:
    print(field)


# Wenn nicht von TTN TTI als Bytes kommt dann:
payload = bytes.fromhex("0319E8AC0067F52B0F7A63")
r = decode(1, payload)
for field in r:
    print(field)