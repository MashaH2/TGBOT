from telegram import Update
from telegram.ext import ContextTypes
from Check_User_Auth import is_user_authorized
import json
import requests


async def user_access(
        update: Update, context: ContextTypes.DEFAULT_TYPE
        ) -> None:

    user_id = str(update.effective_user.id)
    if not is_user_authorized(user_id):
        await update.message.reply_text(
            "You're not authorized! Use /auth to authorize."
            )
        return
    # Load user's Twitter username from User_data.json
    with open("User_data.json", 'r') as file:
        user_data = json.load(file)
        twitter_username = user_data.get(
            str(user_id), {}).get("Twitter Username")

    # If the user hasn't provided their Twitter username, inform them
    if not twitter_username:
        await update.message.reply_text(
            "You haven't provided your Twitter username. "
            "Please do so with /auth."
            )
        return

    # Load all group data from Group_data.json
    with open("Group_data.json", 'r') as file:
        all_group_data = json.load(file)

    access_links = []  # To collect all invite links the user has access to

    # Iterate over each group's data
    for group_user_id, group_info in all_group_data.items():
        ethereum_address = group_info.get("Ethereum Address")
        invite_link = group_info.get("Invite Link")

# If the group hasn't provided their Ethereum address or invite link, skip
        if not ethereum_address or not invite_link:
            continue

        # Fetch data from the API and handle pagination
        base_url = (f"https://prod-api.kosetto.com/users"
                    "/{ethereum_address}/token/holders"
                    )

        page_start = ""
        user_found = False

        while True:
            response = requests.get(base_url + page_start)
            data = response.json()

            users_data = data.get("users", [])
            for entry in users_data:
                if entry.get("twitterUsername") == (twitter_username and
                                                    entry.get(
                                                        "balance", "0"
                                                        ) >= "1"):

                    access_links.append(invite_link)
                    user_found = True
                    break

# If the user is found or there's no next page, break out of the loop
            if user_found or "nextPage" not in data:
                break

            # Set up the next page query parameter
            page_start = f"?pageStart={data['nextPage']}"

    # Reply to the user based on whether they have access
    if access_links:
        links_str = "\n".join(access_links)
        await update.message.reply_text(
            f"You have access to the following groups:\n{links_str}"
            )
    else:
        await update.message.reply_text(
            "Sorry, you don't have access to any groups."
            )
