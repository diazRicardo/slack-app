import logging
import os

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

logging.basicConfig(level=logging.INFO)
load_dotenv()

SLACK_BOT_TOKEN = os.environ["ACA_App_Bot_User"]
SLACK_APP_TOKEN = os.environ["ACA_App_Socket_Mode_Token"]

chatbot_app = App(token=SLACK_BOT_TOKEN)

@chatbot_app.event("app_mention")
def mention_handler(body, context, payload, options, say, event):
    say("Hello World!")

@chatbot_app.event("message")
def message_handler(body, context, payload, options, say, event):
    pass

if __name__ == "__main__":
    handler = SocketModeHandler(chatbot_app, SLACK_APP_TOKEN)
    handler.start()