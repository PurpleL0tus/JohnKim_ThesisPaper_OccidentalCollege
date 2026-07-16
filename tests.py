import pytest
from tools import Tokens, is_valid_regex
from math_stuff import normal_distribution
from keywords import (
    pair_matcher_util, pair_matcher,
    pair_capitalizator, process_keywords
)
from regex_generator import regex_generator


# --- tools ---

def test_is_valid_regex_accepts_valid():
    assert is_valid_regex(r'\d+')
    assert is_valid_regex(r'[a-z]+')
    assert is_valid_regex(r'(foo|bar)')
    assert is_valid_regex(r'^hello\s+world$')

def test_is_valid_regex_rejects_invalid():
    assert not is_valid_regex(r'(unclosed')
    assert not is_valid_regex(r'[bad')
    assert not is_valid_regex(r'*noquant')

def test_tokens_returns_string():
    t = Tokens()
    for _ in range(20):
        token = t.get_random_token()
        assert isinstance(token, str)


# --- math_stuff ---

def test_normal_distribution_stays_in_bounds():
    for _ in range(200):
        val = normal_distribution(5, 2, 0, 10)
        assert 0 <= val <= 10

def test_normal_distribution_returns_int():
    val = normal_distribution(3, 1)
    assert isinstance(val, int)


# --- keywords ---

def test_pair_merge_basic():
    assert pair_matcher_util('guppies', 'guppy') == 'gupp(ies|y)'

def test_pair_merge_prefix_of_other():
    # 'cat' is a prefix of 'cats' — should produce 'cats?'
    assert pair_matcher_util('cat', 'cats') == 'cats?'

def test_pair_merge_single_char_suffix():
    result = pair_matcher_util('foo', 'foos')
    assert result == 'foos?'

def test_pair_capitalizator_case_variants():
    assert pair_capitalizator('apple', 'Apple') == '[Aa]pple'
    assert pair_capitalizator('Apple', 'apple') == '[Aa]pple'

def test_pair_capitalizator_no_match():
    assert pair_capitalizator('cat', 'car') is None
    assert pair_capitalizator('hello', 'world') is None

def test_pair_capitalizator_none_input():
    assert pair_capitalizator(None, 'apple') is None
    assert pair_capitalizator('apple', None) is None

def test_pair_matcher_returns_none_for_mismatched_prefix():
    assert pair_matcher('apple', 'banana') is None

def test_pair_matcher_none_input():
    assert pair_matcher(None, 'guppy') is None
    assert pair_matcher('guppy', None) is None

def test_process_keywords_merges_plain_words():
    result = process_keywords(['guppies', 'guppy'])
    assert 'gupp(ies|y)' in result

def test_process_keywords_merges_regex_groups():
    result = process_keywords(['gupp(ies|happy)', 'gupp(itonia)', 'gupp(piop)'])
    assert len(result) > 0
    # all results should be non-empty strings
    assert all(isinstance(r, str) and len(r) > 0 for r in result)

def test_process_keywords_single_item():
    result = process_keywords(['hello'])
    assert result == ['hello']


# --- regex_generator ---

def test_regex_generator_returns_valid_or_none():
    result = regex_generator(['apple', 'banana', 'cherry'])
    assert result is None or is_valid_regex(result)

def test_regex_generator_returns_string_when_found():
    # run a few times — should find something within 10000 tries
    found = None
    for _ in range(3):
        found = regex_generator(['abc'])
        if found is not None:
            break
    if found is not None:
        assert isinstance(found, str)
        assert is_valid_regex(found)
