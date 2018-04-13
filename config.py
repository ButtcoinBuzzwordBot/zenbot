# Zen Bot configuration file. Bleep bloop.
#
# TODO v1.2: Add Couchbase memcache/error logging for remote hosting.
# TODO: post reply to parent although complicated re: praw models.
# TODO: rewrite template system to find replace vars.
# FIX: never reply to self.
# FIX: don't allow random replies to same thread as where invoked.

import os

# When DEBUG is True the bot uses /r/testingground4bots, set in oauth.py.

DEBUG = True
AUTHOR = "BarcaloungerJockey"
BOTNAME = "python:zenmaster.bot:v1.1 (by /u/" + AUTHOR +")"
SUBREDDIT = "buttcoin"

# If HOSTED is True the script runs indefinitely. Set appropriate storage type and
# info based on your hosting options. Both SQLite and MySQL default to UTF-8 for
# text but if not you can set a default encoding for input files below. SQLite is
# preferred as database needs are minimal and it's fast and lightweight compared to
# others.

HOSTED = False
ENCODING = "utf-8"
#STORE_TYPE = "memcache"
STORE_TYPE = "sqlite"
#STORE_TYPE = "mysql"
#MYSQL_USER = "zenbot"
#MYSQL_PW = os.environ['MYSQL_PW']
#MYSQL_HOST = "127.0.0.1"
DATABASE = "zenbot"

# Example: odds set at 1000 are approx. 1-in-1000 chance to post.
KOAN_STORE = "koans"
KOAN_ODDS = 15
HAIKU_STORE = "haiku"
HAIKU_ODDS = 15
SNAPPY_STORE = "snappy"
SNAPPY_ODDS = 999999999999
RANT_STORE = "rants"
RANT_TABLE = "lex_insult"
REPLY_STORE = "replies"
REPLY_ODDS = 30

VISITED_STORE = "visited"
if DEBUG: VISITED_STORE += "_debug"
MAX_VISITED = 5000

# Start rate limit at 600 (10 minutes) per reply for a bot account w/no karma.
# Drops quickly as karma increases, can go down to 10 seconds minimum.
RATELIMIT = 10
SUBLIMIT = 25
SLEEP_LOOP = 10 * 60
SLEEP_TIMEOUT = 30

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

shortsig = (
    "\n_____\n^Send praise, rage or arcade game tokens to /u/" + AUTHOR
)

already_visited = []
snappy_quotes = []
