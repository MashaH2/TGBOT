from telegram import Update
from telegram.ext import ContextTypes
from Check_User_Auth import is_user_authorized
from Save_Group_Data import save_to_group_data
import re
from Config import logger
from Variables import invite_links
from datetime import datetime


async def invite_user(
        update: Update, context: ContextTypes.DEFAULT_TYPE
        ) -> None:

    user_id = str(update.effective_user.id)
    username = update.effective_user.username
    message = update.effective_message
    first_name = update.effective_user.first_name
    last_name = update.effective_user.last_name

    if not is_user_authorized(user_id):
        await update.message.reply_text("You're not authorized! "
                                        "Use /auth to authorize."
                                        )
        return
    # Check if the message is a direct reply to the bot's prompt
    if not message.reply_to_message or message.reply_to_message.text != (
        "Address has been registered.\n"
        "Please provide me with the invite to your group using "
        "/invite <link> by replying to this message"
        "\n"
        "Example: /invite +Zj...M0"
            ):
        await update.message.reply_text("Please reply to the message.")
        return

    link = message.text.split()[1] if len(message.text.split()) > 1 else None
    if not link:
        await update.message.reply_text(
            "Please reply to the previous message and provide a Telegram "
            "group invite link using the format /invite <invite_link>\n"
            "\n" "Example: /invite +Zj...M0")
        return

    # Extract the unique string from the message
    unique_string_parts = message.text.strip().split()
    unique_string = unique_string_parts[-1] if unique_string_parts else ""
    # Check if the provided link fits the pattern of a Telegram group inv url
    telegram_link_pattern = r"\+[A-Za-z0-9]+"
    if re.match(telegram_link_pattern, unique_string):
        # Store the unique string associated with the user's Telegram ID
        invite_links[user_id] = f"https://t.me/{unique_string}"
        # Save to group_data.json
        group_data = {
            "Telegram UserID": str(user_id),
            "Invite Link": f"https://t.me/{unique_string}"
        }
        save_to_group_data(group_data, "group_data.json")

        await update.message.reply_text(
            f"Invite link registered as https://t.me/{unique_string}\n"
            "\n"
            "Thank you for setting up, Please provide the "
            "following invite link to your users: https://t.me/Tracr_Bot\n"
            "\n"
            "Once your FT Key Holders authorize through twitter and the bot "
            "crosschecks their Holdings, they will gain access to your "
            "Group Invite Link"
            "\n"
            "Do not forget to add FT_Tracr / @Tracr_Bot to your group and "
            "give Admin Priviledges"
            "\n"
            "\n"
            "From now on, you can use /access if you wish to look for other "
            "groups that have been registered via the bot"
                                        )
        # Log successful registration
        logger.info(f"Invite link registered: https://t.me/{unique_string} "
                    "for User ID: {user_id}, "
                    "Username: {username}, "
                    "Full Name: {first_name + ' ' + (last_name or '')}, "
                    "Time: {datetime.now()}")
    else:
        await update.message.reply_text(
            "Invalid Telegram invite unique string."
            )
# Shows the data currently stored in the bots memory.
