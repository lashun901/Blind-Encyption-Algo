from random import randint
from time import time

key_encryption_constant: int = 333

def random_key_generator(seed: int = randint(1, 999_999_999)):
    a: int = seed + 233 if seed % 2 == 0 else seed + 45762
    b: int = round(a / seed) + seed ** (1 / seed)
    c: int = 33334
    d: int = (87451 % b) + a
    e: int = round((b + a) / (a - c)) - 3283
    return round((a * c + seed) * round(d / b) + e)

class Key:
    def __init__(k) -> None:
        k.value: int = 0
        k.encrypted: bool = False

    def get_value(k) -> int:
        return k.value
    
    def set_value(k, key_value: int) -> bool:
        if key_value != 0 and k.value == 0:
            k.value: int = key_value
        else: 
            return ValueError

class KeyGenerator:
    def __init__(kg, seed: int = randint(1, 999_999_999)) -> None:
        kg.key: Key =  kg._generate_key(seed=seed)
    
    def get_key(kg) -> Key:
        return kg.key

    def _generate_key(kg, seed: int) -> Key:
        new_key: Key = Key()
        new_key.set_value(random_key_generator(seed=seed))
        return new_key

