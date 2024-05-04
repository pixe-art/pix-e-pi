import requests
import json
import random

FIREBASE = 'https://pix-e-b9fab-default-rtdb.europe-west1.firebasedatabase.app'
STORAGE = 'https://firebasestorage.googleapis.com/v0/b/pix-e-b9fab.appspot.com/o/images'

# TODO: support for multiple images

def get_screen_details(device_id):
    r"""
    get details for a device given device_id
    returns dict with activeImage and owner
    """
    r = requests.get(f'{FIREBASE}/pixeModel/screens/{device_id}.json')
    return r.json()

def get_screen_template():
    with open('screenTemplate.json', 'r') as f:
        screen_template = json.load(f)
    return screen_template

def validate_screen(device_id):
    screen_template = get_screen_template()
    r = requests.get(f'{FIREBASE}/pixeModel/screens/{device_id}.json')
    for screen_template_item in screen_template:
        try:
            if not screen_template_item in r.json():
                return False #invalid
        except: return False
    
    return True # valid

def setup_screen(device_id):
    screen_template = get_screen_template()
    r = requests.put(f'{FIREBASE}/pixeModel/screens/{device_id}.json', json=screen_template)
    # print(r.status_code)
    # print(r.text)

def get_image_data(image_id):
    r"""
    gets image metadata given image_id
    returns dict with lastEdited, owner, description and title
    """
    r = requests.get(f'{FIREBASE}/pixeModel/images/{image_id}.json')
    return r.json()
    # print(type(r.json()))
    # print(r.json()['url'])

def get_image(image_id):
    url = f'{STORAGE}%2F{image_id}.png?alt=media'
    r = requests.get(url)
    if r.status_code == 200:
        print(f'Downloading image {image_id}')
        return r.content
    else:
        print(f'Failed to download {image_id}: {r.status_code} {r.reason} {r.url}')
        return None

def get_pairing_code(device_id):
    r = requests.get(f'{FIREBASE}/pixeModel/screens/{device_id}/pairingCode.json')
    return r.json()

def get_pairing_code_details(pairing_code):
    r = requests.get(f'{FIREBASE}/pixeModel/pairingCodes/{pairing_code}.json')
    return r.json()

def set_pairing_code(pairing_code, device_id):
    r = requests.put(f'{FIREBASE}/pixeModel/pairingCodes/{str(pairing_code)}.json', json=device_id)
    if r.status_code == 200:
        r = requests.put(f'{FIREBASE}/pixeModel/screens/{device_id}/pairingCode.json', json=str(pairing_code))

def validate_ownership(device_id):
    r = requests.get(f'{FIREBASE}/pixeModel/screens/{device_id}.json')
    owner = r.json()['owner']
    pairing_code = r.json()['pairingCode']

    if owner == 0: # device does not have owner
        return False

    r = requests.get(f'{FIREBASE}/pixeModel/users/{owner}/device.json')
    device = r.json()

    if device != device_id: # device has owner but owner does not device or owner has another device
        return False

    return True

def generate_pairing_code(device_id):
    r = requests.get(f'{FIREBASE}/pixeModel/pairingCodes.json')
    codes = r.json()
    print(codes)

    code = f'{random.randint(1,9999):04}'
    while code in codes:
        print(f'Code taken: {code}')
        code = f'{random.randint(1,9999):04}' 
    print(f'Picked code: {code}')

    if device_id in codes.values(): # delete any previous active pairing code
        for c in codes.items():
            if c[1] == device_id:
                d = requests.delete(f'{FIREBASE}/pixeModel/pairingCodes/{c[0]}.json')
                
    # set new paring code
    print(f'code: {code} device_id: {device_id}')
    r = requests.put(f'{FIREBASE}/pixeModel/pairingCodes/{code}.json', json=device_id)

if __name__ == "__main__":
    generate_pairing_code('pixedemodevice')
    # needs_pairing('pixedemodevice')

    # set_pairing_code(0000, 'pixedemodevice')

    # print(get_pairing_code('pixedemodevice'))
    # print(get_pairing_code_details('1234'))
    
    # get_image('https://knark.club/pix-e/rgb.png')
    # get_image_url('userid', 'imageid')
    # print(validate_screen('randomid'))
    # setup_screen('test')
    # print(get_active_image_url('randomid'))

