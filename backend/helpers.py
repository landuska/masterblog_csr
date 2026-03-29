from flask import request
import json_helpers
import os

project_root = os.path.dirname(os.path.abspath(__file__))
users_path = os.path.join(project_root, "data", "users.json")


def create_id(lst):
    """
    Generates a new unique ID based on the highest existing ID in the list.

    Args:
       lst: The current list

    Returns:
        int: The next available unique integer ID.
    """
    if not lst:
        return 1
    return max(int(item["id"]) for item in lst) + 1


def authenticate():
    """
    Authenticates a user by checking the token provided in the Authorization header.

    Returns:
        dict: The user dictionary if the token is valid.
        None: If the token is missing or invalid.
    """
    users = json_helpers.load_file(users_path)
    token = request.headers.get("Authorization")

    if not token:
        return None

    for user in users:
        if user.get("token") == token:
            return user
    return None
