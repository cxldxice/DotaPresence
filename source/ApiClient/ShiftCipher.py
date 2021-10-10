from itertools import cycle


def form_dict() -> dict:
    return dict([(i, chr(i)) for i in range(128)])


def comparator(value: str, key: str) -> dict:
    return dict([(idx, [ch[0], ch[1]])
                 for idx, ch in enumerate(zip(value, cycle(key)))])


def full_encode(value: str, key: str) -> str:
    d = comparator(value, key)
    length = len(form_dict())
    return "".join(
        [chr(ord(value_for_encode) + ord(key_value) % length) for (value_for_encode, key_value) in d.values()])


def full_decode(value: str, key: str) -> str:
    d = comparator(value, key)
    length = len(form_dict())
    return "".join(
        [chr(ord(value_for_encode) - ord(key_value) % length) for (value_for_encode, key_value) in d.values()])
