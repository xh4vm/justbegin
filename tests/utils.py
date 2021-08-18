import random
from string import ascii_lowercase


def random_string(length: int = 8) -> str:
    return ''.join(random.choice(ascii_lowercase) for _ in range(length))
