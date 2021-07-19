from random import choice
import string


def randomword(length=8):
   letters = string.ascii_lowercase
   return ''.join(choice(letters) for i in range(length))

