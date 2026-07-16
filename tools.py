import random
import re


class Tokens:
    def __init__(self):
        self.regex_commands = [
            "~", "%", ".", "^", "$", "\\",
            "[~]", "[^~]", "[a-z]", "[A-Z]", "[0-9]",
            r"\d", r"\D", r"\w", r"\W", r"\s", r"\S",
            "*", "+", "?",
            "{%}", "{%,}", "{%,%}",
            "(~)", "(?:~)", "(?<~>~)",
            r"(?=~)", r"(?!~)", r"(?<=~)", r"(?<!~)",
            r"\b", r"\B",
            "i", "m", "s", "x",
            r"^\d{3}-\d{2}-\d{4}$",
            "(~|~)",
        ]

    def get_random_token(self):
        all_tokens = [
            item
            for attr in dir(self)
            if isinstance(getattr(self, attr), list)
            for item in getattr(self, attr)
        ]
        return random.choice(all_tokens) if all_tokens else None


def is_valid_regex(pattern):
    try:
        re.compile(pattern)
        return True
    except re.error:
        return False
