import requests

with open('device_id.txt', 'r') as f:
    device_id = f.read()

with open('screenTemplate.json', 'r') as f:
    screen_template = f.read()

r = requests.get(f'https://pix-e-b9fab-default-rtdb.europe-west1.firebasedatabase.app/screens/{device_id}.json')

if r.json() is Null:
    put = requests.put(f'https://pix-e-b9fab-default-rtdb.europe-west1.firebasedatabase.app/screens/{device_id}.json', )    


print(r.json())