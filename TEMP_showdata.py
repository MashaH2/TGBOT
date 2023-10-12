import os
import json
from Check_User_Auth import is_user_authorized


async def show_data(update, context):
    user_id = str(update.message.from_user.id)
    if not is_user_authorized(user_id):

        await update.message.reply_text(
            "You're not authorized! Use /auth to authorize."
            )
        return

    abs_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "group_data.json")

    # Check if the file exists
    if not os.path.exists(abs_path):

        await update.message.reply_text("No data found.")
        return

    # Read the data from the JSON file
    with open(abs_path, 'r') as file:
        data = json.load(file)

    # Construct the response
    response = "Current data:\n"
    for user_id, user_data in data.items():

        ethereum_address = user_data.get("Ethereum Address", "N/A")
        invite_link = user_data.get("Invite Link", "N/A")
        response += f"User ID: {user_id}\n"
        "Ethereum Address: {ethereum_address}\n"
        "Invite Link: {invite_link}\n\n"

    await update.message.reply_text(response)
