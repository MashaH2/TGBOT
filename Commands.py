from telegram import Update
from telegram.ext import ContextTypes
from Check_User_Auth import is_user_authorized

async def commands(
        update: Update, context: ContextTypes.DEFAULT_TYPE
        ) -> None:
    user_id = str(update.effective_user.id)
    if not is_user_authorized(user_id):
        await update.message.reply_text(
            "You're not authorized! Use /auth to authorize."
            )
        return
    if update.message.text == '/commands':
        await update.message.reply_text(
            " You can use the following commands\n"
            "/contact -> To contact my creator\n"
            "/update -> To crosscheck all Holders and "
            "kick users who do not hold keys anymore\n"
            "/stats -> To check how many Groups and "
            "Users have been registered"
            )
