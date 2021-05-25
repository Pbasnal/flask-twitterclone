import string
import random

LETTERS = string.ascii_letters
NUMBERS = string.digits  
PUNCTUATION = string.punctuation    

# create alphanumerical from string constants
printable = f'{LETTERS}{NUMBERS}{PUNCTUATION}'

# convert printable from string to list and shuffle
printable = list(printable)
random.shuffle(printable)

def password_generator(length=50) -> str:
    '''
    Generates a random password having the specified length
    :length -> length of password to be generated. Defaults to 8
        if nothing is specified.
    :returns string <class 'str'>
    '''

    # generate random password and convert to string
    random_password = random.choices(printable, k=length)
    random_password = ''.join(random_password)
    
    return random_password