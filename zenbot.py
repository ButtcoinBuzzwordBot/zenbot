# Bleep bloop! I am a Zen Bot. Om.
# TODO: mysql, memcache
# TODO: post reply to parent? complicated re: praw models.
# FIX: never reply to self
# FIX: Snappy posts going to comments not submission

import sys, traceback, random, time
import config as cfg, db, comments, cmdline, oauth

def checkInbox(r, dbase):
    """ Check inbox and reply randomly to new messages from regular users. """

    IGNORE = [cfg.ZENBOT_USERNAME, "reddit"] # TODO: cfg.AUTHOR
    msgs = list(r.inbox.unread(limit=None))

    if len(msgs) > 0 and not cfg.HOSTED:
        print(str(len(msgs)) +" message(s) in /u/"+ cfg.ZENBOT_USERNAME +"\'s inbox.")

    for msg in msgs:
        msg.mark_read()
        if msg.author not in IGNORE:
            reply = "*bleep bloop* "+ dbase.readRandom(cfg.REPLY_STORE) +" *beep*"
            msg.reply(reply)

def main(r):
    """ Initialize and recurse through posts. """

    dbase = db.DB(cfg.STORE_TYPE)
    if len(sys.argv) > 1:
        cmdline.processOpts(dbase, sys.argv)

    checkInbox(r, dbase)
    cfg.snappy_quotes = dbase.readSnappy(r)

    while True:
        try:
            sub = r.subreddit(cfg.SUBREDDIT).new(limit=40)
            for submission in sub:
                post = r.submission(submission)
                c = comments.Comments(dbase, r, post)

                # VERY IMPORTANT: since the bot marks posts visited, the submission
                # (top) must be processed last, so traverse comment trees depth-first.
                if cfg.DEBUG: print("submission: " + format(post.id))
                for comment in post.comments:
                    c.checkComment(comment)

                # TODO: differentiate post vs. comment in class?
                c.comment = post
                if not c.alreadyVisited(post):
                    c.markVisited(post)
                    if random.randrange(0, cfg.HAIKU_ODDS) < 1:
                        c.postReply(dbase.readRandom(cfg.HAIKU_STORE))
                    elif random.randrange(0, cfg.SNAPPY_ODDS) < 1:
                        c.postReply(random.choice(cfg.snappy_quotes) + cfg.snap_reply)
                    elif random.randrange(0, cfg.KOAN_ODDS) < 1:
                        c.postReply(dbase.readRandom(cfg.KOAN_STORE))

                dbase.writeVisited()

            if not cfg.HOSTED:
                print("\nBleep! All done.")
                break
            else: time.sleep(60 * 10)

        except:
            if cfg.DEBUG: traceback.print_exc()
            time.sleep(30)
            if cfg.DEBUG: print("ERROR: Reddit timeout, resuming.")

    dbase.closeDB()

if __name__ == '__main__':
    main(oauth.auth())
