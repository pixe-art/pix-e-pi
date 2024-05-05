import subprocess
import time
import database_helper
import connectivity_check
import image_helper
import screen_helper
import atexit

with open('device_id.txt', 'r') as f:
    global DEVICE_ID
    DEVICE_ID = f.read()
    print(f'DEVICE_ID: {DEVICE_ID}')

# network_setup_process = subprocess.Popen(['/home/pi/.local/share/virtualenvs/pix-e-HnRFVe-M/bin/python', 'network_setup_main.py'])

previous_image_0 = False
code_showing = False
paired = False
def loop():
    global screen_process
    global previous_image_0
    global code_showing

    while not connectivity_check.is_connected():
        print('screen_watchdog waiting for network')
        time.sleep(60)

    if not database_helper.validate_screen(DEVICE_ID):
        print("screen invalid, updating database")
        database_helper.setup_screen(DEVICE_ID)
    else: print("screen in database and ok")


    first_loop = True
    while not database_helper.validate_ownership(DEVICE_ID):
        if first_loop:
            first_loop = False
            code = database_helper.generate_pairing_code(DEVICE_ID)
            screen_helper.generate_pairing_image(code)
            try: screen_process.terminate() 
            except: pass
            code_showing = True
            screen_process = screen_helper.display_image('pairing_image.png')


    active_image_id, updated = image_helper.update_local_image(DEVICE_ID)
    print(f'active_image_id: {active_image_id}\nupdated: {updated}')
    if active_image_id != 0:
        print('has valid image_id')
        if updated or previous_image_0 or code_showing:
            previous_image_0 = False
            image_helper.update_local_image(DEVICE_ID)
            try: screen_process.terminate() 
            except: pass
            screen_process = screen_helper.display_image(f'images/{active_image_id}')
    else:
        previous_image_0 = True
        try: screen_process.terminate() 
        except: pass        

def cleanup():
    print("screen_watchdog cleanup")
    try: screen_process.terminate()
    except: pass
    try: network_setup_process.terminate()
    except: pass

atexit.register(cleanup)

while True:
    loop()
    time.sleep(10)