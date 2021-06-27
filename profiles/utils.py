import uuid 

def get_random_token():
    token =  str(uuid.uuid4())[:8].replace('-', '').lower()
    return token

#uudi part is implemented in (PART-2) 22:10, this is to create a unique slug for the users with similar first and last name 
#using uuid 5 throws a error