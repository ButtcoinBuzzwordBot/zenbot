import os

# When DEBUG is True the bot uses /r/testingground4bots.

DEBUG = False
AUTHOR = "BarcaloungerJockey"
BOTNAME = "python:zenmaster.bot:v1.0 (by /u/" + AUTHOR +")"
#REDDIT = "https://redd.it/"
SUBREDDIT = "buttcoin"
# Max. new messages in bot inbox before script quits.
MAX_MSGS = 12

DATABASE = None
VISITED_STORE = "visited"
KOAN_STORE = "koans"
HAIKU_STORE = "haiku"
SNAPPY_STORE = "snappy"
HAIKU_ODDS = 1000 # (ex: 1 in 1000 chance)
KOAN_ODDS = 20
SNAPPY_ODDS = 10

MAX_VISITED = 1000

# If HOSTED is True the script continues looping. Set appropriate storage type and
# info based on your hosting options.
HOSTED = False
STORE_TYPE = "sqlite"
#STORE_TYPE = "mysql"
#MYSQL_USER = "user"
#MYSQL_PW = "password"
#MYSQL_HOST = "127.0.0.1"

# Start rate limit at 600 (10 minutes) per reply for a bot account w/no karma.
# Drops quickly as karma increases, can go down to 10 seconds minimum.
RATELIMIT = 20

# Triggers which active the bot to reply to a comment.
TRIGGER = "!ZenBot"
CMD_KOAN = TRIGGER + " koan"
CMD_HAIKU = TRIGGER + " haiku"
CMD_SNAPPY = TRIGGER + "snappy"

# Reply for Snapshillbot quote.
snap_reply = "The Zen Master /u/Snapshillbot whispered into my ear:\n\n"

# Signature for all replies.
sig = (
    "\n_____\n\n^(Hi! I\'m a hand-run bot, *bleep* *bloop* "
    "| Send praise, rage or arcade game tokens to /u/" + AUTHOR + ", *beep*)"
)

already_visited = []
snappy_quotes = []
