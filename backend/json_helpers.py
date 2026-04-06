import json


def load_file(path):
    """
    Loads the list from the JSON file.

    Args:
        path (str): The path to the JSON file.

    Returns:
        list: A list of dictionaries.
              Returns an empty list if the file is missing or corrupted.
    """
    try:
        with open(path, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []
    except OSError:
        return []


def write_file(lst, path):
    """
    Writes the updated list of blog posts back to the JSON file.

    Args:
        path (str): The path to the JSON file.
        lst (list): The list of dictionaries to be saved.
    Returns:
        Returns an empty list if errors are encountered.
    """
    try:
        with open(path, "w") as file:
            json.dump(lst, file, indent=4)
    except TypeError:
        return []
    except OSError:
        return []
