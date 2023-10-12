from telegram import Update
from telegram.ext import ContextTypes
from Check_User_Auth import is_user_authorized


async def setup(
        update: Update, context: ContextTypes.DEFAULT_TYPE
        ) -> None:

    user_id = str(update.effective_user.id)
    if not is_user_authorized(user_id):

        await update.message.reply_text(
            "You're not authorized! Use /auth to authorize."
            )
        return
    if update.message.text == '/setup':
        await update.message.reply_text(
            "/groupowner -> Use If you're a group owner\n"
            "/user -> Use if you're looking to join a group"
        )
