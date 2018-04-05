# I'm the Zen Bot. Bleep bloop!
# TODO: mysql, memcache, log support
# TODO: randomize types of replies
# TODO: raise/lower frequency based on up/downvotes?
# FIX: reply to parent? Getting wrong author w/nested replies.

import sys, traceback, random, time
import db, comments, config as cfg, cmdline, oauth

def main(r):
    """ Initialize and recurse through posts. """

    dbase = db.DB(cfg.STORE_TYPE)
    cfg.snappy_quotes = dbase.readSnappy(r)

    if len(sys.argv) > 1:
        cmdline.processOpts(dbase, sys.argv)

    # Check bot inbox for messages.
    msgs = list(r.inbox.unread(limit=None))
    if len(msgs) > 0 and not cfg.HOSTED:
        print(str(len(msgs)) +" message(s) in /u/"+ cfg.ZENBOT_USERNAME +"\'s inbox.")
        print("Please read before running bot.")
        if len(msgs) > cfg.MAX_MSGS: exit()

    try:
        while True:
            sub = r.subreddit(cfg.SUBREDDIT).new(limit=40)
            for submission in sub:
                post = r.submission(submission)
                c = comments.Comments(dbase, r, post)

                if cfg.DEBUG: print("submission: " + format(post.id))
                # TODO: Figure out how to randomize order for variety.
                # TODO: Put Snappy quotes in DB to pull random.
                if not c.alreadyVisited(post.id):
                    cfg.already_visited.append(str(post.id))
                    if random.randrange(0, cfg.HAIKU_ODDS) < 1:
                        c.postReply(dbase.readRandom(cfg.HAIKU_STORE))
                    elif random.randrange(0, cfg.SNAPPY_ODDS) < 1:
                        c.postReply(random.choice(cfg.snappy_quotes) + cfg.snap_reply)
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

    except:
        if cfg.DEBUG: traceback.print_exc()
        time.sleep(30)
        if cfg.DEBUG: print("ERROR: Reddit timeout, resuming.")

if __name__ == '__main__':
    main(oauth.auth())
