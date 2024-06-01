def write_avoid_xml_conflicts(text: str):
    if text == "<":
        return "&lt;"
    elif text == ">":
        return "&gt;"
    elif text == '"':
        return "&quot;"
    elif text == "&":
        return "&amp;"

    return text


def is_valid_file(file: str, end_with: str = ".jack", raise_error=False):
    if not raise_error:
        return file[0].upper() == file[0] and file.endswith(end_with)

    if file[0].upper() != file[0]:
        raise ValueError("the file name must start with an uppercase letter")
    if not file.endswith(end_with):
        raise ValueError(f"the file extension must be {end_with}")
