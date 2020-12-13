import random
import string
import os
from datetime import datetime



def Generate_random_id(N):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))


def current_time_string():
    return datetime.now().strftime("%H-%M-%S")


def store_image(file,id):
    # os.getcwd() for local path
    # os.path.splitext(file.filename)[1] for extention
    path = os.getcwd() + "/static/images/" + str(id) + ".jpg"
    if os.path.isfile(path):
        os.remove(path)
    file.save(path)
    return