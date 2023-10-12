from telegram import Update
from telegram.ext import ContextTypes
import requests
import pyshorteners
from Config import logger


async def authorize(update: Update, context: ContextTypes.DEFAULT_TYPE)-> None:
    user_id = update.effective_user.id
    username = update.effective_user.username
    # Construct the URL to get the verification URL from the Flask app
    verification_url_endpoint = (
        f"https://7d5b-84-52-5-102.ngrok-free.app/verify"
        f"?telegram_user_id={user_id}&telegram_username={username}"
        )

    try:
        # Make a request to the Flask app to get the verification URL
        response = requests.get(verification_url_endpoint)
        verification_url = response.text

        # Shorten the verification URL
        s = pyshorteners.Shortener()
        short_url = s.tinyurl.short(verification_url_endpoint)

        # Send the shortened verification URL to the user
        await update.message.reply_text(
            f"Please click on the following link"
            f"to authenticate your Twitter account: {short_url}"
            )
    except Exception as e:
        logger.error(f"Error fetching verification URL: {e}")
        await update.message.reply_text(
            "An error occurred while trying to fetch"
            "the verification URL. Please try again later."
            )
