from textacy import preprocessing
import re, json

CAMEL_WORD_WHITE_LIST = [
    "wifi"
]

def save_to_file(data: list[dict], file_path: str):
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving data to file: {e}")

def add_spaces_to_camel_case(text):
    # Add a space before any uppercase letter that is not at the start of the string
    return re.sub(r'(?<!^)(?=[A-Z])', ' ', text)

def standardize_text_with_textacy(text: str) -> str:
    # Remove extra whitespace and normalize spacing
    if text is None:
        return None
    text = preprocessing.normalize.whitespace(text)
    return text

def get_longer_str(str1: str, str2: str) -> str: # if one of both is None, return the other
    if str1 is None and str2 is None:
        return None
    if str1 is None:
        return str2
    if str2 is None:
        return str1
    return str1 if len(str1) > len(str2) else str2

def filter_more_general_term(terms: list[str]) -> list[str]:
    # Filter out terms that are substrings of other terms 
    # Such as "pool" and "indoor pool" and "outdoor pool" -> keep the shorter one as it's more general

    filtered_terms = []
    for term in terms:
        flag = False
        for term1 in terms:
            if term != term1 and term1 in term:
                flag = True
                break
        if not flag:
            filtered_terms.append(term)

    return filtered_terms

def jaro_distance(s1, s2):
    # Step 1: Calculate matching characters
    len1, len2 = len(s1), len(s2)
    if len1 == 0:
        return 0.0
    match_window = max(len1, len2) // 2 - 1

    # Create a boolean array to mark matched characters
    matched1 = [False] * len1
    matched2 = [False] * len2
    matches = 0

    for i in range(len1):
        start = max(0, i - match_window)
        end = min(len2, i + match_window + 1)
        for j in range(start, end):
            if s1[i] == s2[j] and not matched2[j]:
                matched1[i] = True
                matched2[j] = True
                matches += 1
                break

    # If no matches, return 0
    if matches == 0:
        return 0.0

    # Step 2: Calculate transpositions
    t = 0
    k = 0
    for i in range(len1):
        if matched1[i]:
            while not matched2[k]:
                k += 1
            if s1[i] != s2[k]:
                t += 1
            k += 1
    t /= 2

    # Step 3: Calculate Jaro distance
    jaro_dist = (matches / len1 + matches / len2 + (matches - t) / matches) / 3
    return jaro_dist

def jaro_winkler_distance(s1, s2, p=0.1, l=4):
    # Step 1: Calculate Jaro distance
    jaro_dist = jaro_distance(s1, s2)
    
    # Step 2: Apply the Winkler adjustment
    # Count common prefix (max 4 characters)
    prefix_len = 0
    for i in range(min(len(s1), len(s2), l)):
        if s1[i] == s2[i]:
            prefix_len += 1
        else:
            break
    
    # Adjust the Jaro distance with the Winkler correction
    jaro_winkler_dist = jaro_dist + (p * prefix_len * (1 - jaro_dist))
    
    return jaro_winkler_dist
