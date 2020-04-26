import base64

def decode_data_from_hex(payload):
    if not len(payload) == 10:
        return "false len"
    temperature = (int(payload[0:2] + payload[4:5], 16) / 10.0) - 80
    humidity = (int(payload[2:4] + payload[5:6], 16) / 10.0) - 25
    co2 = int(payload[6:10], 16)
    return temperature,humidity,co2


def decode_data_from_bytes(bytes):
    if not len(bytes) == 5:
        return "false len"
    t = (((bytes[0] << 4) + (bytes[2] >> 4)) / 10) - 80
    h = (((bytes[1] << 4) + (bytes[2] & 0x0F)) / 10) - 25
    co2 = (bytes[3] << 8) + bytes[4]
    return t,h,co2


def decode(port, bytes):
    decoded_payload = None
    if port == 2:
        decoded_payload= decode_data_from_hex(bytes)
    return decoded_payload


print(decode(2, "3e441d021b"))


# TTN schickt -> PibEAAYABwAI
# Daher erst base64 decodieren
payload = base64.b64decode("PkQdAhs=")
# und dann hex() raus machen -> einfacher zu dekodieren
payload = payload.hex()
r = decode_data_from_hex(payload)
print(r)

# oder:
# TTN schickt -> PibEAAYABwAI
# Base64 decodieren und dann nur mit bytes arbeiten
payload = base64.b64decode("PkQdAhs=")
r = decode_data_from_bytes(payload)
print(r)


