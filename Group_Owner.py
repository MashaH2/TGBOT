from telegram import Update
from telegram.ext import ContextTypes
from Check_User_Auth import is_user_authorized

async def group_owner(
        update: Update, context: ContextTypes.DEFAULT_TYPE
        ) -> None:

    user_id = str(update.effective_user.id)
    if not is_user_authorized(user_id):
        await update.message.reply_text(
            "You're not authorized! Use /auth to authorize."
            )
        return

    if update.message.text == '/groupowner':
        await update.message.reply_text(
            "Lets get on with it and set everything up.\n"
            "First Step: Use /wallet <Friend.Tech Wallet Address>. "
            "Please reply to this message."
        )
