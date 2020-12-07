import random 

def Genrate_random_id(N):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N));