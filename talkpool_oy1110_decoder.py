from datetime import datetime, timedelta
import base64


def decode_single_measurement_from_bytes(bytes):
    if not len(bytes) == 3:
        return "false len"
    t = (((bytes[0] << 4) + (bytes[2] >> 4)) / 10) - 80
    h = (((bytes[1] << 4) + (bytes[2] & 0x0F)) / 10) - 25
    return [
        {"field": "TEMPERATURE", "value": t},
        {"field": "HUMIDITY", "value": h}
    ]


def decode_multi_measurement_from_bytes(bytes):
    is_hour = bytes[0] >> 7 & 1
    dt = bytes[0] & 0x0F
    payload = bytes[1:len(bytes)]
    number_of_reports = int(len(bytes) / 3)
    reports = []
    time_now = datetime.utcnow()
    for i in range(0, number_of_reports):
        chunk = payload[0+(i*3):3+(i*3)]
        t = (((chunk[0] << 4) + (chunk[2] >> 4)) / 10) - 80
        h = (((chunk[1] << 4) + (chunk[2] & 0x0F)) / 10) - 25
        timestamp = time_now - timedelta(hours=(dt * i)) if is_hour else time_now - timedelta(minutes=(dt * i))
        timestamp = int(timestamp.timestamp())
        reports.append({"field": "TEMPERATURE", "value": t, "timestamp": timestamp})
        reports.append({"field": "HUMIDITY", "value": h, "timestamp": timestamp})
    return reports


def decode_measurement_interval(payload):
    measurement_interval = (payload[2] << 8) + payload[3]
    return {"field": "MEASUREMENT_INTERVAL", "value": measurement_interval}


def decode(port, bytes):
    decoded_payload = None
    if port == 1:
        index = bytes[1]
        if index == 0x23:
            decoded_payload = decode_measurement_interval(bytes)
    if port == 2:
        decoded_payload = decode_single_measurement_from_bytes(bytes)
    if port == 3:
        decoded_payload = decode_multi_measurement_from_bytes(bytes)
    return decoded_payload


# Wenn von TTN TTI kommt: Dann Base64 decode
# Wenn als Bytes kommt (Wanesy) dann bytes.fromhex()

payload = base64.b64decode("PkQd")
d = decode(2, payload)
print(d)

# minutes
payload = base64.b64decode("Dy48zTM40jkx9Q==")
d = decode(3, payload)
print(d)

# hours
payload = base64.b64decode("jy48zTM40jkx9Q==")
d = decode(3, payload)
print(d)

# measurement interval set
payload = base64.b64decode("ASMADw==")
d = decode(1, payload)
print(d)


