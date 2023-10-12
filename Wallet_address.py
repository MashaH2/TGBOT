from telegram import Update
from telegram.ext import ContextTypes
from Check_User_Auth import is_user_authorized
from Variables import ft_addresses, pattern
import json
import requests
from Save_Group_Data import save_to_group_data
import re
from datetime import datetime
from Config import logger

async def wallet_address(
        update: Update, context: ContextTypes.DEFAULT_TYPE
        ) -> None:

    user_id = str(update.effective_user.id)
    username = update.effective_user.username
    message = update.effective_message
    first_name = update.effective_user.first_name
    last_name = update.effective_user.last_name
    full_name = (first_name or '') + ' ' + (last_name or '')

    if not is_user_authorized(user_id):
        await update.message.reply_text(
            "You're not authorized! Use /auth to authorize."
            )
        return

    # Check if the message is a direct reply to the bot's prompt
    if not message.reply_to_message or message.reply_to_message.text != (
        "Lets get on with it and set everything up.\n"
        "First Step: Use /wallet <Friend.Tech Wallet Address>. "
        "Please reply to this message."
            ):

        await update.message.reply_text("Please reply to the message.")
        return

    address = message.text.split()[1] if len(
        message.text.split()) > 1 else None
    if not address:
        await update.message.reply_text("Please provide an Ethereum address "
                                        "using the format /wallet <address>\n"
                                        "Please Reply to this message.")
        return

    if address in ft_addresses.values():
        await update.message.reply_text(
            "Address has already been registered."
            )
        return

    if re.match(pattern, address):
        # Fetching the Twitter Username and Twitter ID
        # using the Telegram UserID from user_data.json
        with open("user_data.json", 'r') as file:
            user_data = json.load(file)
            twitter_username = user_data[user_id]['Twitter Username']
            twitter_id = user_data[user_id]['Twitter_ID']

        # Fetching data from the API using the provided address
        api_response = requests.get(
            f"https://prod-api.kosetto.com/users/{address}"
            )
        api_data = api_response.json()

        # Comparing the data from the API with the data from user_data.json
        if api_data['twitterUsername'] != (twitter_username or
                                           api_data['twitterUserId'] !=
                                           twitter_id):

            await update.message.reply_text(
                "Please try again, Twitter username "
                "does not match the Address"
                )
            return

        # Store the FT address associated with the user's Telegram ID
        ft_addresses[user_id] = address
        # Save to group_data.json
        group_data = {
            'Telegram UserID': str(user_id),
            'Ethereum Address': address
        }
        save_to_group_data(group_data, "group_data.json")

        await update.message.reply_text("Address has been registered.\n"
                                        "Please provide me with "
                                        "the invite to your group using "
                                        "/invite <link> by replying "
                                        "to this message"
                                        "\n" "Example: /invite +Zj...M0")
        # Log user interaction
        logger.info(f"User ID: {user_id}, Username: {username}, "
                    "Full Name: {full_name}, "
                    "Time: {datetime.now()}, "
                    "Message: {message.text}")
    else:
        await update.message.reply_text("Invalid Ethereum address.")
