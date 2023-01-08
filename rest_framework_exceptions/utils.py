import re


def _underscore_to_camel(match: re.Match) -> str:
    group = match.group()
    if len(group) == 3:
        return group[0] + group[2].upper()
    else:
        return group[1].upper()


def camelize(field: str) -> str:
    camelize_re = re.compile(r"[a-z0-9]?_[a-z0-9]")
    return re.sub(camelize_re, _underscore_to_camel, field)
