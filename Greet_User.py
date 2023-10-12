from telegram import Update
from telegram.ext import ContextTypes

async def greet_user(
        update: Update, context: ContextTypes.DEFAULT_TYPE
        ) -> None:
    if update.message:
        if update.message.text == '/start':
            await update.message.reply_text(
                "Thank you for using FT Holder Manager, "
                "use /auth to get started"
            )
