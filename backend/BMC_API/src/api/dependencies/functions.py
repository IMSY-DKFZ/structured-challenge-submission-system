import random
import string


def get_random_digits(length):
    # choose from all lowercase letter
    letters = string.digits
    result_str = "".join(random.choice(letters) for i in range(length))
    return result_str
