def get_longer_str(str1: str, str2: str) -> str: # if one of both is None, return the other
    if str1 is None and str2 is None:
        return None
    if str1 is None:
        return str2
    if str2 is None:
        return str1
    return str1 if len(str1) > len(str2) else str2