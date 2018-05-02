# Zen Bot configuration file. Bleep bloop.

import os

# When DEBUG is True the bot uses /r/testingground4bots, set in oauth.py.

DEBUG = False
AUTHOR = "BarcaloungerJockey"
BOTNAME = "python:zenmaster.bot:v1.2 (by /u/" + AUTHOR +")"
SUBREDDIT = "buttcoin"
ZENBOT_USERNAME = os.environ['ZENBOT_USERNAME']

# Reddit accounts to ignore in bot inbox.
IGNORE = [ZENBOT_USERNAME, AUTHOR, "reddit"]

# If HOSTED is True the script runs indefinitely. Set appropriate storage type and
# info based on your hosting options. Both SQLite and MySQL default to UTF-8 for
# text but if not you can set a default encoding for input files below. SQLite is
# preferred as database needs are minimal and it's fast and lightweight compared to
# others.
#
# Memcache and Couchbase support on hold until Python 3.7 supported.

HOSTED = True
ENCODING = "utf-8"
STORE_TYPE = "sqlite"
#STORE_TYPE = "mysql"
###STORE_TYPE = "memcache"
#MYSQL_USER = "zenbot"
#MYSQL_PW = os.environ['MYSQL_PW']
#MYSQL_HOST = "127.0.0.1"
DATABASE = "zenbot"

# Example: odds set at 1000 are approx. 1-in-1000 chance to post.
KOAN_STORE = "koans"
KOAN_ODDS = 15
HAIKU_STORE = "haiku"
HAIKU_ODDS = 15
REPLY_STORE = "replies"
REPLY_ODDS = 21
RANT_STORE = "rants"
RANT_TABLE = "lex_insult"
TEMPLATE_STORE = "templates"

VISITED_STORE = "visited"
if DEBUG: VISITED_STORE += "_debug"
MAX_VISITED = 5000

# Start rate limit at 600 (10 minutes) per reply for a bot account w/no karma.
# Drops quickly as karma increases, can go down to 10 seconds minimum.
RATELIMIT = 10
SUBLIMIT = 25
SLEEP_LOOP = 5 * 60
SLEEP_TIMEOUT = 30

# Triggers which active the bot to reply to a comment.
TRIGGER = "!ZenBot"
CMD_KOAN = TRIGGER + " koan"
CMD_HAIKU = TRIGGER + " haiku"
CMD_RANT = TRIGGER + " rant"
CMD_REPLY = TRIGGER + " quip"

# Signatures for replies.
sig = (
    "\n_____\n^(Hi! I\'m a bot, *bleep* *bloop* | Send praise or rage to "
    "/u/" + AUTHOR +
    ". Submit rants, koans, etc. on /r/" + ZENBOT_USERNAME + ", *beep*)"
)

def botReply(reply):
    return("^(*beep*)\n" + reply)

# END OF SETTINGS.

already_visited = []
class ExitException(Exception):
    pass
