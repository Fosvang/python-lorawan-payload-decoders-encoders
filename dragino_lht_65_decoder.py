import base64


def decode_report(payload):
    batV = ((payload[0] << 8 | payload[1]) & 0x3FFF) / 1000
    temp_SHT = payload[2] << 8 | payload[3]
    if payload[2] & 0x80:
        temp_SHT |= 0xFFFF0000
    temp_SHT = (temp_SHT / 100)
    hum_SHT = ((payload[4] << 8 | payload[5]) / 10)
    temp_ds = payload[7] << 8 | payload[8]
    if payload[7] & 0x80:
        temp_ds |= 0xFFFF0000
    temp_ds = (temp_ds / 100)
    return [
        {"field": "BATTERY", "value": batV},
        {"field": "TEMPERATURE_PROBE", "value": temp_ds},
        {"field": "TEMPERATURE", "value": temp_SHT},
        {"field": "HUMIDITY", "value": hum_SHT},
    ]


def decode(port, payload):
    if port == 2:
        return decode_report(payload)


# Wenn Bytes kommen (Wanesy), dann:
payload = bytes.fromhex("CBD5050501BE017FFF7FFF")
p = decode(2, payload)
print(p)


# Wenn TTN / TTI kommt:
payload = base64.b64decode("y9UFBQG+AX//f/8=")
p = decode(2, payload)
print(p)