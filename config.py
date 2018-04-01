import os

# When DEBUG is True the bot uses /r/testingground4bots.

DEBUG = False
AUTHOR = "BarcaloungerJockey"
BOTNAME = "python:zenmaster.bot:v0.1 (by /u/" + AUTHOR +")"
#REDDIT = "https://redd.it/"
SUBREDDIT = "buttcoin"
# Max. new messages in bot inbox before script quits.
MAX_MSGS = 12

DATABASE = None
VISITED_STORE = "visited"
KOAN_STORE = "koans"
HAIKU_STORE = "haiku"

MAX_VISITED = 1000

# If HOSTED is True the script continues looping. Set appropriate storage type and
# info based on your hosting options.
HOSTED = False
STORE_TYPE = "sqlite"
#STORE_TYPE = "mysql"
#MYSQL_USER = "user"
#MYSQL_PW = "password"
#MYSQL_HOST = "127.0.0.1"

# Reddit account and API OAuth information. You can hardcode values here but
# it creates a security risk if your code is public (on Github, etc.)
# Otherwise, set the environment variables on your host as below.
USERNAME = os.environ['ZENBOT_USERNAME']
PASSWORD = os.environ['ZENBOT_PASSWORD']
CLIENT_ID = os.environ['ZENBOT_ID']
CLIENT_SECRET = os.environ['ZENBOT_SECRET']

# Start rate limit at 600 (10 minutes) per reply for a bot account w/no karma.
# Drops quickly as karma increases, can go down to 10 seconds minimum.
RATELIMIT = 600

# Triggers which active the bot to reply to a comment.
TRIGGER = "!ZenMaster"
CMD_KOAN = TRIGGER + " koan"
CMD_HAIKU = TRIGGER + " haiku"

# Signature for all replies.
sig = (
    "\n_____\n\n^(I\'m a hand-run bot, *bleep* *bloop* "
    "| Send praise, rage or arcade game tokens to /u/" + AUTHOR + ", *beep*)"
)

already_visited = []
