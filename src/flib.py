from flask import  request

import vk_api
import random
import os
import sqlite3
import time

from multiprocessing import Process
from vk_api.longpoll import VkLongPoll , VkEventType
from config.config   import access_key , groups , service_key
from src.exceptions  import NonAttachments , NonPhoto , NonPhotoDownloaded
from src.logger      import log

# need to get photo cause vk does not support gettings wall with group auth
def __auth_as_service():
    try:
        vk = vk_api.VkApi(token=service_key)
        return vk
    except vk_api.AuthError:
        return False

# need to send messages
def __auth_as_group():
    try:
        vk = vk_api.VkApi(token=access_key)
        return vk
    except vk_api.AuthError:
        return False

# return string with format 
# photo<owner_id>_<media_id>_<access_ke>
# she use random numbers to get a photo
def get_new_photos():
    cur_group = random.randint(0 , len(groups)-1)
    session = __auth_as_service()
    _req = session.method('wall.get' , {'owner_id':groups[cur_group] , 'count': 40})
    cur_group_photo = random.randint(0 , len(_req['items']) - 1)
    photo_obj = _req['items'][cur_group_photo]
    
    if not 'attachments' in photo_obj:
        raise NonAttachments
    if not 'photo' in photo_obj['attachments'][0]:
        raise NonPhoto
    
    photo_attachment = photo_obj['attachments'][0]
    photo_attachment_access_key = photo_attachment['photo']['access_key']
    photo_attachment_owner_id   = photo_attachment['photo']['owner_id']
    photo_attachment_media_id   = photo_attachment['photo']['id']

    photo_struct = 'photo' +  str(photo_attachment_owner_id) + '_' + str(photo_attachment_media_id) + '_' + str(photo_attachment_access_key)
    
    return photo_struct


# now vk require a random id to send message
# diapazon 0 - int32MAX
def set_random_id():
    rand = random.randint(0 , 2147483647)
    return rand

def send_message_to_user(user_id):
    vk = __auth_as_group()
    vk.method('messages.send' , {'user_id': user_id , 'random_id': set_random_id() , 'attachment': get_new_photos()})
    log('Messages were sended to user with id {0}'.format(user_id))

def validate_password():
    if request.args.get('pass') == '12345':
        return True
    else:
        return False

    
def sender():
    send_message_to_user(263838377)
    log('Sended message to me')