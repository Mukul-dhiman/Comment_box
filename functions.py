import random 
import string
from datetime import datetime



def Generate_random_id(N):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))


def current_time_string():
    now = datetime.now()
    return now.strftime("%H:%M:%S")