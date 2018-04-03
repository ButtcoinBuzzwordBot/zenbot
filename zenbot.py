# I'm the Zen Bot. Bleep bloop!
# TODO: mysql, memcache, log4 support
# TODO: randomize types of replies
# FIX: visited submissions and comments not sticking?

import sys
import random
import praw

import db
import comments
import config as cfg
import cmdline

# Initialize PRAW with custom User-Agent.
if cfg.DEBUG:
    cfg.SUBREDDIT = "testingground4bots"
    print("Username/pass: " + cfg.ZENBOT_USERNAME, cfg.ZENBOT_PASSWORD)
    print("Client ID/pass: " + cfg.ZENBOT_ID, cfg.ZENBOT_SECRET)
    print("Authenticating...")
r = praw.Reddit(
    client_id=cfg.ZENBOT_ID,
    client_secret=cfg.ZENBOT_SECRET,
    password=cfg.ZENBOT_PASSWORD,
    user_agent=cfg.BOTNAME,
    username=cfg.ZENBOT_USERNAME
)
if cfg.DEBUG: print("Authenticated as: " + format(r.user.me()))

def main(r):
    """ Initialize and recurse through posts. """

    dbase = db.DB(cfg.STORE_TYPE)
    cfg.snappy_quotes = dbase.readSnappy(r)

    if len(sys.argv) > 1:
        cmdline.processOpts(dbase, sys.argv)

    # Check bot inbox for messages.
    msgs = list(r.inbox.unread(limit=None))
    if len(msgs) > 0 and not cfg.HOSTED:
        print(str(len(msgs)) + " message(s) in /u/" + cfg.USERNAME + "\'s inbox.")
        print("Please read before running bot.")
        if len(msgs) > cfg.MAX_MSGS: exit()

    while True:
        sub = r.subreddit(cfg.SUBREDDIT).new(limit=30)
        for submission in sub:
            post = r.submission(submission)
            c = comments.Comments(dbase, r, post)

            if cfg.DEBUG: print("submission: " + format(post.id))
            # Figure out how to randomize order for variety.
            # Put Snappy quotes in DB to pull random.
            if not c.alreadyVisited(post.id):
                cfg.already_visited.append(str(post.id))
                if random.randrange(0, cfg.HAIKU_ODDS) < 1:
                    c.postReply(dbase.readRandom(cfg.HAIKU_STORE))
                elif random.randrange(0, cfg.SNAPPY_ODDS) < 1:
                    i = random.randrange(0, len(cfg.snappy_quotes) -1)
                    c.postReply(cfg.snap_reply +"\""+ cfg.snappy_quotes[i] +"\"")
                elif random.randrange(0, cfg.KOAN_ODDS) < 1:
                    c.postReply(dbase.readRandom(cfg.KOAN_STORE))

            dbase.writeVisited()
            for comment in post.comments:
                c.checkComment(comment)

        if not cfg.HOSTED:
            print("\nBleep! All done.")
            break
        else: time.sleep(60 * 10)

    dbase.closeDB()

if __name__ == '__main__':
    main(r)
