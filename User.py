from telegram import Update
from telegram.ext import ContextTypes
from Check_User_Auth import is_user_authorized

async def user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)
    if not is_user_authorized(user_id):
        await update.message.reply_text(
            "You're not authorized! Use /auth to authorize."
            )
        return

    if update.message.text == '/user':
        await update.message.reply_text("Hiya there, before you can "
                                        "see which groups you can enter, "
                                        "please authorize your Twitter "
                                        "account by using /auth command")
