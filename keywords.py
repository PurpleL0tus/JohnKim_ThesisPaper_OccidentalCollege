import re


def _remove_duplicates(lst):
    return list({item for item in lst if item is not None})


def _alphabetize(lst):
    return sorted(lst, key=str)


def _pair_merge(a, b):
    """Merge two plain strings into a regex alternation on their common prefix."""
    for i in range(len(max(a, b))):
        try:
            if a[i] != b[i]:
                return f'{a[:i]}({a[i:]}|{b[i:]})'
        except IndexError:
            suffix = f'{a[i:]}{b[i:]}'
            if len(suffix) == 1:
                return f'{a[:i]}{suffix}?'
            return f'{a[:i]}({suffix})?'
    return None


def _classify(pattern):
    """Returns (has_optional_group, has_group, has_single_optional) for a pattern."""
    opt  = bool(re.search(r'.*\(.*\)\?$', pattern))
    grp  = bool(re.search(r'.*\(.*|.*\)$', pattern))
    sing = bool(re.search(r'.*[^/\\/]\?$', pattern))
    return opt, grp, sing


def _extract_parts(pattern, has_opt, has_grp, has_sing):
    """Pull the alternatives out of a pattern's terminal group."""
    parts = []
    if has_opt or has_grp:
        m = re.search(r'\(.*\)\?$' if has_opt else r'\(.*\)$', pattern)
        s = m.group()
        flag = 0
        for i in range(len(s)):
            if s[i] in ('(', ')', '|') and i != 0 and s[i - 1] != '\\':
                parts.append(s[flag + 1:i])
                flag = i
    elif has_sing:
        parts.append(pattern[-2])
    return parts


def pair_matcher_util(a, b):
    return _pair_merge(a, b)


def find_prefix(a, b):
    last = 0
    for i in range(len(max(a, b))):
        if re.search(r'\(.*\)', a) and i == re.search(r'\(.*\)', a).span()[0]:
            break
        if re.search(r'\(.*\)', b) and i == re.search(r'\(.*\)', b).span()[0]:
            break
        try:
            if a[i] != b[i]:
                break
        except IndexError:
            break
        last = i
    return last


def find_parts(a, b):
    a_opt, a_grp, a_sing = _classify(a)
    b_opt, b_grp, b_sing = _classify(b)

    if not any([a_opt, a_grp, a_sing, b_opt, b_grp, b_sing]):
        return _pair_merge(a, b)

    if not any([a_opt, a_grp, a_sing]):
        if any([b_opt, b_grp]) or not b_sing:
            a, b = b, a
            a_opt, a_grp, a_sing = _classify(a)
            b_opt, b_grp, b_sing = _classify(b)

    parts = _extract_parts(a, a_opt, a_grp, a_sing) + _extract_parts(b, b_opt, b_grp, b_sing)
    return _alphabetize(_remove_duplicates(parts))


def pair_matcher(a, b):
    if a is None or b is None:
        return None
    if a[0].lower() != b[0].lower() or a[1] != b[1] or a[2] != b[2]:
        return None

    a_opt, a_grp, a_sing = _classify(a)
    b_opt, b_grp, b_sing = _classify(b)

    if not any([a_opt, a_grp, a_sing, b_opt, b_grp, b_sing]):
        return _pair_merge(a, b)

    if not any([a_opt, a_grp, a_sing]):
        if any([b_opt, b_grp]) or not b_sing:
            a, b = b, a
            a_opt, a_grp, a_sing = _classify(a)
            b_opt, b_grp, b_sing = _classify(b)

    # scan forward to find where the common prefix ends
    prefix = ''
    i_remember = 0
    for i in range(len(max(a, b))):
        prefix = a[:i]
        if re.search(r'\(.*\)', a) and i == re.search(r'\(.*\)', a).span()[0]:
            break
        if re.search(r'\(.*\)', b) and i == re.search(r'\(.*\)', b).span()[0]:
            break
        try:
            if a[i] != b[i]:
                break
        except IndexError:
            break
        i_remember = i

    if a_opt or a_grp or a_sing:
        if b_opt or b_grp or not b_sing:
            parts = _extract_parts(a, a_opt, a_grp, a_sing) + _extract_parts(b, b_opt, b_grp, b_sing)
            parts = _alphabetize(_remove_duplicates(parts))

            if re.search(r'\(.*\)$', a):
                j = re.search(r'\(.*\)$', a).span()[0] - 1
            elif re.search(r'\(.*\)?$', a):
                j = re.search(r'\(.*\)?$', a).span()[0] - 1
            else:
                j = i_remember

            if j != i_remember:
                parts.append(a[i_remember:j])

            if re.search(r'\(.*\)$', b):
                j = re.search(r'\(.*\)$', b).span()[0] - 1
            elif re.search(r'\(.*\)?$', b):
                j = re.search(r'\(.*\)?$', b).span()[0] - 1
            else:
                j = i_remember

            if j != i_remember:
                parts.append(b[i_remember:j])

            result = prefix + '(' + '|'.join(parts) + ')'
            if a[-1] == '?' or b[-1] == '?':
                result += '?'
            return result

    if a_opt:
        return a[:-2] + f'|{b[i_remember:]})?'
    elif a_grp:
        return a[:-1] + f'|{b[i_remember:]})'
    elif a_sing:
        stem = a[:-1]
        last_char = stem[-1]
        stem = stem[:-1]
        return stem + f'({last_char}|{b[i_remember:]})?'

    return None


def first_4_match(a, b):
    if len(a) <= 4 or len(b) <= 4:
        return False
    return all(a[i] == b[i] for i in range(4))


def pair_capitalizator(a, b):
    if a is None or b is None:
        return None
    if (a[0].lower() == b[0] or a[0] == b[0].lower()) and a[1:] == b[1:]:
        return f'[{a[0].upper()}{a[0].lower()}]{a[1:]}'
    return None


def process_keywords(keyword_list):
    kw = keyword_list.copy()
    orig_len = len(keyword_list)

    # null out consumed entries in-place so appended merges end up in the result
    for i in range(orig_len):
        for j in range(orig_len):
            if i == j or kw[i] is None or kw[j] is None:
                continue
            if len(kw[i]) < 3 or len(kw[j]) < 3:
                continue
            if (kw[i][0].lower() == kw[j][0].lower()
                    and kw[i][1] == kw[j][1]
                    and kw[i][2] == kw[j][2]):
                paired = pair_matcher(kw[i], kw[j])
                if paired is not None:
                    kw[i] = None
                    kw[j] = None
                    kw.append(paired)

    intermediate = _remove_duplicates(kw)

    final = intermediate.copy()
    for i in range(len(intermediate)):
        for j in range(len(intermediate)):
            if i == j:
                continue
            capped = pair_capitalizator(intermediate[i], intermediate[j])
            if capped is not None:
                final[i] = None
                final[j] = None
                final.append(capped)

    return _remove_duplicates(final)


if __name__ == '__main__':
    test_keywords = ['gupp(ies|happy)', 'gupp(itonia)', 'gupp(piop)']
    result = process_keywords(test_keywords)
    print(f'processed keywords: {result}')
