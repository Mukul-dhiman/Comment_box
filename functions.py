import random 
import string
from datetime import datetime

now = datetime.now()

def Generate_random_id(N):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))


def current_time_string():
    return now.strftime("%H:%M:%S")