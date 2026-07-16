import random
import time


regex_tokens = [
    ".",
    "^",
    "$",
    "*",
    "+",
    "?",
    "{n}",
    "{n,}",
    "{n,m}",
    "[]",
    "|",
    "\\",
    "\\d", "\\D",
    "\\w", "\\W",
    "\\s", "\\S",
    "\\b",
]

TARGET = r"\b[Gg]upp(ies|y)(?:\s+\w+)*\s*"
KEYWORD = "[Gg]upp(ies|y)"
MAX_HITS = 10


if __name__ == '__main__':
    start = time.time()
    attempts = 0
    hits = 0
    hit_times = []
    hit_attempts = []

    while True:
        attempts += 1
        token_count = random.randint(1, 10)
        insert_at = random.randint(0, token_count - 1)

        pattern = ''
        for i in range(token_count):
            pattern += random.choice(regex_tokens)
            if i == insert_at:
                pattern += KEYWORD

        if pattern == TARGET:
            elapsed = time.time() - start
            print(f"Found: {pattern}")
            print(f"  time: {elapsed:.4f}s, attempts: {attempts}")

            hit_times.append(elapsed)
            hit_attempts.append(attempts)
            attempts = 0
            hits += 1
            start = time.time()

            if hits == MAX_HITS:
                print(f"\nAverage time: {sum(hit_times) / len(hit_times):.4f}s")
                print(f"Average attempts: {sum(hit_attempts) / len(hit_attempts):.1f}")
                break
