import database_helper

local_image = {}

def update_local_image(device_id):

    updated = False

    screen_details = database_helper.get_screen_details(device_id)

    print(screen_details)

    try: active_image_id = screen_details['activeImage']
    except:
        print("except: active_image_id") 
        return 0, updated
    try: screen_owner = screen_details['owner']
    except: 
        print("except: screen_owner") 
        return 0, updated

    print(f'get_image_data params: {active_image_id}')
    image_data = database_helper.get_image_data(active_image_id)
    print(f'image_data: {image_data}')

    try: active_image_last_edited = image_data['lastEdited']
    except: 
        print("except: active_image_last_edited") 
        return 0, updated

    if active_image_id != 0: # screen has an active image
        print('active_image_id is not 0')
        if active_image_id in local_image: #if actve image in local array
            print(f'active_image_id {active_image_id} is in local_image')
            if local_image[active_image_id] < active_image_last_edited: # update image if a newer version is avalible
                local_image[active_image_id] = active_image_last_edited
                get_image(active_image_id) #image exists localy but is outdated
                updated = True
        else:
            get_image(active_image_id) #image does not exist localy
            local_image[active_image_id] = active_image_last_edited
            updated = True
    else:
        return 0, updated
    
    return active_image_id, updated


def get_image(image_id):
    with open(f'images/{image_id}', 'wb') as f: #download new image
        f.write(database_helper.get_image(image_id))

