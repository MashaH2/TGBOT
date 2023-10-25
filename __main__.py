import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
)
from dotenv import load_dotenv
from auth_user import authorize
from commands import commands
from greet_user import greet_user
from group_owner import group_owner
from setup import setup
from user import user
from wallet_address import wallet_address
from invite_user import invite_user
from user_access import user_access
from update_group import update_group

load_dotenv("keys.env")

token = os.environ.get("token")


def main() -> None:
    """Start the Bot"""
# Create the Application and pass it your bot's token.
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler('start', greet_user))
    application.add_handler(CommandHandler('setup', setup))
    application.add_handler(CommandHandler('groupowner', group_owner))
    application.add_handler(CommandHandler('user', user))
    application.add_handler(CommandHandler("auth", authorize))
    application.add_handler(CommandHandler('wallet', wallet_address))
    application.add_handler(CommandHandler('invite', invite_user))
    application.add_handler(CommandHandler('access', user_access))
    application.add_handler(CommandHandler('commands', commands))
    application.add_handler(CommandHandler("update", update_group))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
