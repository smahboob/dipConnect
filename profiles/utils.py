import uuid 

def get_random_token():
    token =  str(uuid.uuid4())[:8].replace('-', '').lower()
    return token