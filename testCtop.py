import requests
import json

url = "https://ctop.iiit.ac.in/api/nodes/create-cin/388"
data = {
 "lux": 87.7,
  "humidity": 39.7,
  "temperature": 14.72,
  "ipv6_address": "example",
  "rpl": 46,
  "availability": "example",
  "connectivity": "example",
  "disconnectivity": "example",
  "rsl_in": 55,
  "rsl_out": 9,
  "current": 9.43,
  "power": 26.44,
  "energy": 83.86,
  "relay_status": "example",
  "lamp_status": "example"}

headers = {"Content-Type": "application/json", "Authorization": "Bearer 380cc181d46ebc2b963d11a1e71ae6d7"}

response = requests.post(url, data=json.dumps(data), headers=headers)

if response.status_code == 200:
    print("Success:", response.text)
else:
    print("Error:", response.status_code, response.text)
