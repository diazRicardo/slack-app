import logging
import os
import requests

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

logging.basicConfig(level=logging.INFO)
load_dotenv()

# read slack credentials
SLACK_BOT_TOKEN = os.environ["ACA_App_Bot_User"]
SLACK_APP_TOKEN = os.environ["ACA_App_Socket_Mode_Token"]

slackApp = App(token=SLACK_BOT_TOKEN)

# -------------- Weather and temperature of cities -------------- 
def get_weather(city, say):
    # correct the name of city input before calling weather API
    if city == "sf":
        city = "San Francisco"
    else:
        city = city.capitalize()

    api_key = "0178954784dd5a66127b9429e5563cdf"
    api_link = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial"

    response = requests.get(api_link)
    if response.status_code == 200:
        data = response.json()
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        say(f"Weather: {weather}. Temperature: {temp} °F")

# -------------- YouTube videos of cities --------------
def videos(city, say):
    vid = [""]
    vid_list= [
        "https://www.youtube.com/watch?v=h_ayZ-xcMd4",
        "https://www.youtube.com/watch?v=6DQxRQb9dCE",
        "https://www.youtube.com/watch?v=ZHHbpy91O2E",
        "https://www.youtube.com/watch?v=OoqNoNQeoPo",
        "https://www.youtube.com/watch?v=oSexfR0Ubzw",
        "https://www.youtube.com/watch?v=r3oYIZe0FEk",
        "https://www.youtube.com/watch?v=dqQO3h9B_wg"
    ]

    if city == "sf":
        vid = vid_list[0]
    elif city == "tokyo":
        vid = vid_list[1]
    elif city == "berlin":
        vid = vid_list[2]
    elif city == "cancun":
        vid = vid_list[3]
    elif city =="rome":
        vid = vid_list[4]
    elif city == "milan":
        vid = vid_list[5]
    else:
        vid = vid_list[6]
    say(vid)

# -------------- Displays info of cities --------------
def display_info(city, say):
    videos(city, say)
    get_weather(city, say)

# -------------- Commands that travelbot will respond to ------------
@slackApp.event("app_mention")
def mention_handler(payload, say, logger):
    request = payload['blocks'][0]['elements'][0]['elements'][1]['text']
    ip = request.lstrip().split(' ', 1)
    logger.info(ip)
    city = request[0].strip().lower()

    if city in ('sf', 'tokyo', 'berlin', 'cancun', 'rome', 'milan', 'paris'):
        display_info(city, say)
    elif city == "help":
        say("Welcome! I'm travelbot, your travel guide for a selection of 8 beautiful cities around the world: \n San Franciso (type '@chatbot sf') \n Berlin (type '@chatbot berlin') \n Mexico City (type '@chatbot mc')  \n Tokyo (type '@chatbot tokyo') \n Paris (type '@chatbot paris') \n Rome (type '@chatbot rome') \n Milan (type '@chatbot milan')")
    else:
        say("Looks like you asked me about something I don't yet know! Type @chatbot followed by one of my commands. \nType '@chatbot help' to see a list my commands. ")

if __name__ == "__main__":
    handler = SocketModeHandler(slackApp, SLACK_APP_TOKEN)
    handler.start()

