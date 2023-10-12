import os
import json


def is_user_authorized(
        telegram_user_id: str, filename="user_data.json"
        ) -> bool:
    """
    Check if the provided telegram_user_id is authorized
    (exists in user_data.json).

    Args:
    - telegram_user_id (str): The Telegram UserID to check.
    - filename (str, optional):
    The name of the file containing user data. Defaults to "user_data.json".

    Returns:
    - bool: True if the user is authorized, False otherwise.
    """
    abs_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), filename
        )
    # Check if file exists
    if not os.path.exists(abs_path):
        return False

    # Read the current data from the file
    with open(abs_path, 'r') as file:
        current_data = json.load(file)
    return telegram_user_id in current_data
