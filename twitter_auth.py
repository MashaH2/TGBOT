""" Simplified Flask Bot for Twitter OAut"""
import json
import os
import requests
import logging
from flask import Flask, session, redirect, request
from requests_oauthlib import OAuth1Session
from dotenv import load_dotenv


load_dotenv("keys.env")

client_key = os.environ.get("client_key")
client_secret = os.environ.get("client_secret")
secret_app = os.environ.get("secret_app")
token = os.environ.get("token")

app = Flask(__name__)
app.secret_key = secret_app  # This should be a random secret key for session encryption
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

Telegram_token = token
# Your Twitter API credentials
#client_key = client_key
#client_secret = client_secret
REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
AUTHORIZATION_BASE_URL = 'https://api.twitter.com/oauth/authorize'
ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'


def save_to_json(user_data, filename="user_data.json"):
    """Save the provided user data to a JSON file in a custom format."""

    abs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

    # Read the current data from the file
    if os.path.exists(abs_path):
        with open(abs_path, 'r', encoding='utf-8') as file:
            current_data = json.load(file)
    else:
        current_data = {}

    # Use the telegram_user_id as the unique key
    telegram_user_id = str(user_data['Telegram UserID'])

    # Update or add the user's data
    if telegram_user_id in current_data:
        current_data[telegram_user_id].update(user_data)
    else:
        current_data[telegram_user_id] = user_data

    # Write the updated data to the file
    with open(abs_path, 'w', encoding='utf-8') as file:
        json.dump(current_data, file)


def send_telegram_message(chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    requests.post(url, data=payload)


@app.route('/verify')
def verify():
    """Start the Twitter OAuth process."""
    twitter = OAuth1Session(client_key, client_secret=client_secret)
    request_token = twitter.fetch_request_token(REQUEST_TOKEN_URL)
    session['request_token'] = request_token
    authorization_url = twitter.authorization_url(AUTHORIZATION_BASE_URL)

    telegram_user_id = request.args.get('telegram_user_id', None)
    if telegram_user_id:
        session['telegram_user_id'] = telegram_user_id

    telegram_username = request.args.get('telegram_username', None)
    if telegram_username:
        session['telegram_username'] = telegram_username

    # Redirect the user to the Twitter authorization URL directly
    return redirect(authorization_url)


@app.route('/callback')
def callback():
    """Handle the OAuth callback from Twitter, fetch user details, and print in the terminal."""
    oauth_verifier = request.args.get('oauth_verifier')
    if not oauth_verifier or 'request_token' not in session:
        logging.warning("Session expired or invalid. Redirecting to Twitter homepage.")
        return redirect("https://www.twitter.com")

    twitter = OAuth1Session(client_key,
                            client_secret=client_secret,
                            resource_owner_key=session['request_token']['oauth_token'],
                            resource_owner_secret=session['request_token']['oauth_token_secret'],
                            verifier=oauth_verifier)

    access_tokens = twitter.fetch_access_token(ACCESS_TOKEN_URL)
    logging.info("Received access tokens: %s", access_tokens)

    # Fetch user's username using the Access Tokens
    twitter = OAuth1Session(client_key,
                            client_secret=client_secret,
                            resource_owner_key=access_tokens['oauth_token'],
                            resource_owner_secret=access_tokens['oauth_token_secret'])

    response = twitter.get('https://api.twitter.com/1.1/account/verify_credentials.json')
    if response.status_code != 200:
        logging.error("Error fetching user details: %s ", response.text)
        return "Error fetching user details"

    telegram_user_id = session.get('telegram_user_id', None)
    if not telegram_user_id:
        return "Error: Telegram user ID missing."

    telegram_username = session.get('telegram_username', None)
    if not telegram_username:
        return "Error: Telegram username missing."

    user_info = response.json()
    username = user_info['screen_name']
    user_id = user_info['id_str']
    user_data = {
        "Telegram UserID": telegram_user_id,
        "Telegram Username": telegram_username,
        "Twitter Username": username
    }
    telegram_user_id = session.get('telegram_user_id', None)
    if telegram_user_id:
        send_telegram_message(telegram_user_id, f"Thank you for authorizing {username}!\n" "Please use /setup to continue.")

    # Log the authenticated username
    logging.info(f"Authenticated user: {username}, User ID: {user_id}")
    # Save the authenticated Twitter username to a dictionary and then to a JSON file
    user_data = {"Twitter Username": username,
                 "Twitter_ID": user_id,
                 "Telegram UserID": telegram_user_id,
                 "Telegram Username": telegram_username}
    logging.info("Data to save: %s ", user_data)
    save_to_json(user_data)

    # Return the authenticated username
    return (f"Thank you for authorizing the application {username}."
            f"Currently in BETA, so please close the window and continue with"
            f"the FT_Trackr Bot on Telegram.{telegram_username}"
            f" and {telegram_user_id}"
            )

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(port=8080)
