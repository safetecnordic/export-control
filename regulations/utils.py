def get_formated_string(value: str, delimiter: str) -> str:
    query = f" {delimiter} ".join([f"'{word}'" for word in value.split()])
    return f"({query})"
