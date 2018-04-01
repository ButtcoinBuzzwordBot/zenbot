# I'm the Zen Bot. Bleep bloop!
# TODO: mysql, memcache, log4 support

import sys
import praw
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

    # Check for command line options.
    if len(sys.argv) > 1:
        cmdline.processOpts(store, sys.argv)

    # Check bot inbox for messages.
    msgs = list(r.inbox.unread(limit=None))
    if len(msgs) > 0 and not cfg.HOSTED:
        print(str(len(msgs)) + " message(s) in /u/" + cfg.USERNAME + "\'s inbox.")
        print("Please read before running bot.")
        if len(msgs) > cfg.MAX_MSGS: exit()

    while True:
        sub = r.subreddit(cfg.SUBREDDIT).new()
        for submission in sub:
            post = r.submission(submission)
            if cfg.DEBUG: print("submission: " + format(post.id))
            for comment in post.comments:
                cmt.checkComment(store, r, comment)
        if not cfg.HOSTED:
            print("\nBleep! All done.")
            break

    if store != "file": store.close()

if __name__ == '__main__':
    main(r)
