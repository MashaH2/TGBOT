import os
import json


def save_to_group_data(group_data, filename="group_data.json"):
    """Save the provided group data to a JSON file."""

    abs_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), filename
        )

    # Read the current data from the file
    if os.path.exists(abs_path):
        with open(abs_path, 'r') as file:
            current_data = json.load(file)
    else:
        current_data = {}

    # Use the telegram_user_id as the unique key
    telegram_user_id = str(group_data['Telegram UserID'])

    # If the user already exists, update their data, else create a new entry
    if telegram_user_id in current_data:
        current_data[telegram_user_id].update(group_data)
    else:
        current_data[telegram_user_id] = group_data

    # Write the updated data to the file
    with open(abs_path, 'w') as file:
        json.dump(current_data, file)
# Enable logging
