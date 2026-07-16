import random
from tools import Tokens, is_valid_regex


def regex_generator(keywords):
    token_instance = Tokens()

    for _ in range(10000):
        pattern = ''
        for _ in range(random.randint(2, 4)):
            token = token_instance.get_random_token()
            if '%' in token:
                for _ in range(token.count('%')):
                    token = token.replace('%', str(random.randint(0, 9)), 1)
            if '~' in token:
                for _ in range(token.count('~')):
                    token = token.replace('~', random.choice(keywords), 1)
            pattern += token

        if is_valid_regex(pattern):
            return pattern

    return None
