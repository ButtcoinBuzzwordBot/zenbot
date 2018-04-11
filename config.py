# Zen Bot configuration file.

import os

# When DEBUG is True the bot uses /r/testingground4bots.

DEBUG = True
AUTHOR = "BarcaloungerJockey"
BOTNAME = "python:zenmaster.bot:v1.1 (by /u/" + AUTHOR +")"
SUBREDDIT = "buttcoin"

DATABASE = None
VISITED_STORE = "visited"

KOAN_STORE = "koans"
KOAN_ODDS = 1000000000 # (ex: 1 in 10000000 chance)
HAIKU_STORE = "haiku"
HAIKU_ODDS = 1000000000
#SNAPPY_STORE = "snappy"
SNAPPY_ODDS = 11
RANT_STORE = "rants"
REPLY_STORE = "replies"
REPLY_ODDS = 30

MAX_VISITED = 1000

# If HOSTED is True the script continues looping. Set appropriate storage type and
# info based on your hosting options. Both SQLite and MySQL default to UTF-8 for
# text but if not you can set a default encoding for input files below.
HOSTED = False
ENCODING = "utf-8"
#STORE_TYPE = "sqlite"
STORE_TYPE = "mysql"
MYSQL_USER = "zenbot"
MYSQL_PW = os.environ['MYSQL_PW']
MYSQL_HOST = "127.0.0.1"

# Start rate limit at 600 (10 minutes) per reply for a bot account w/no karma.
# Drops quickly as karma increases, can go down to 10 seconds minimum.
RATELIMIT = 10

# Triggers which active the bot to reply to a comment.
TRIGGER = "!ZenBot"
CMD_KOAN = TRIGGER + " koan"
CMD_HAIKU = TRIGGER + " haiku"
CMD_SNAPPY = TRIGGER + " snappy"
CMD_RANT = TRIGGER + " rant"

# Reply for Snapshillbot quote.
snap_reply = "  \n&nbsp;  \n^^by ^^Zen ^^Master ^^/u/Snapshillbot\n"

# Signature for all replies.
sig = (
    "\n_____\n\n^(Hi! I\'m a hand-run bot, *bleep* *bloop* "
    "| Send praise, rage or arcade game tokens to /u/" + AUTHOR + ", *beep*)"
)

already_visited = []
snappy_quotes = []
