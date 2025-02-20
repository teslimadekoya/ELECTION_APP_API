import random

def generate_voter_id(length=20):
    pool = '1234567890'
    return ''.join(random.choices(pool, k=length))