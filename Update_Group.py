from telegram import Update
from telegram.ext import ContextTypes
import json
import requests


async def update_group(
        update: Update, context: ContextTypes.DEFAULT_TYPE
        ) -> None:

    # Ensure the command is called in a group setting
    if update.effective_chat.type not in ["group", "supergroup"]:

        await update.message.reply_text(
            "This command can only be used in a group."
            )
        return

    # Fetch the list of group members
    group_members = await context.bot.get_chat_members(
        update.effective_chat.id
        )

    for member in group_members:
        telegram_id = str(member.user.id)

        # Fetch the TwitterUsername using the Telegram ID from user_data.json
        with open("user_data.json", 'r') as file:
            user_data = json.load(file)
            twitter_username = user_data.get(
                telegram_id, {}).get('Twitter Username')

        if not twitter_username:
            continue  # Skip if the member has not authenticated

        # Fetch data from the API using the TwitterUsername
        api_response = requests.get(f"https://prod-api.kosetto.com/"
                                    "users/{twitter_username}/token/holders")
        api_data = api_response.json()

        # Check if the TwitterUsername exists in the API data
        if not any(user['twitterUsername'] ==
                   twitter_username for user in api_data['holders']):
            # Kick the user from the group
            await context.bot.kick_chat_member(
                update.effective_chat.id, telegram_id
                )
            # Unban the user to allow them to rejoin in the future
            await context.bot.unban_chat_member(
                update.effective_chat.id, telegram_id
                )
