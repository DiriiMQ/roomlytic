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