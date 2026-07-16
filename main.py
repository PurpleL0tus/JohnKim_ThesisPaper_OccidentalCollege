import random
from tools import Tokens, is_valid_regex
from math_stuff import normal_distribution
from keywords import process_keywords


def generate_regex(token_count, keywords):
    token_instance = Tokens()
    pattern = ''
    for _ in range(token_count):
        token = token_instance.get_random_token()
        if '%' in token:
            for _ in range(token.count('%')):
                token = token.replace('%', str(random.randint(0, 9)), 1)
        if '~' in token:
            for _ in range(token.count('~')):
                token = token.replace('~', random.choice(keywords), 1)
        pattern += token
    return pattern


if __name__ == '__main__':
    MAX_ATTEMPTS = 50000

    keywords = process_keywords(['guppies', 'guppy', 'guppitonia'])
    print(f'keywords: {keywords}')

    for attempt in range(1, MAX_ATTEMPTS + 1):
        if attempt < 10000:
            token_count = normal_distribution(3, 1, 0, 10)
        elif attempt < 20000:
            token_count = normal_distribution(3, 2, 0, 10)
        else:
            token_count = random.randint(0, 10)

        pattern = generate_regex(token_count, keywords)
        print(pattern)

        # swap this check out for whatever you're actually searching for
        if is_valid_regex(pattern):
            print(f'found after {attempt} attempts: {pattern}')
            break
    else:
        print('no suitable pattern found.')
