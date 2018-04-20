# Bleep bloop! I am a Zen Bot. Om.

import sys, traceback, random, time

import config as cfg
import db
import comments
import cmdline, oauth

def checkInbox(r, dbase):
    """ Check inbox and reply randomly to new messages from regular users. """

    msgs = list(r.inbox.unread(limit=None))
    if cfg.DEBUG or (len(msgs) > 0 and not cfg.HOSTED):
        print(str(len(msgs)) +" message(s) in /u/"+ cfg.ZENBOT_USERNAME +"\'s inbox.")

    for msg in msgs:
        msg.mark_read()
        if msg.author not in cfg.IGNORE:
            msg.reply(cfg.botReply(dbase.readRandom(cfg.REPLY_STORE)) + cfg.sig)

def main(r):
    """ Initialize and recurse through posts. """

    dbase = db.DB(cfg.STORE_TYPE)
    if len(sys.argv) > 1:
        cmdline.processOpts(dbase, sys.argv)
    dbase.checkDB()
    if cfg.DEBUG:
        print ("Type CRTL-C CTRL-C to exit.")

    while True:
        checkInbox(r, dbase)

        try:
            sub = r.subreddit(cfg.SUBREDDIT).new(limit=cfg.SUBLIMIT)
            for submission in sub:
                post = r.submission(submission)
                c = comments.Comments(dbase, r, post)

                # VERY IMPORTANT: since the bot marks posts visited, the submission
                # (top) must be processed last, so traverse comment trees depth-first.
                if cfg.DEBUG: print("submission: " + format(post.id))
                for comment in post.comments:
                    newc = comments.Comments(dbase, r, comment)
                    newc.checkComment()

                if not c.alreadyVisited():
                    c.markVisited()
                    if random.randrange(0, cfg.HAIKU_ODDS) < 1:
                        c.postReply(dbase.readRandom(cfg.HAIKU_STORE))
                    elif random.randrange(0, cfg.KOAN_ODDS) < 1:
                        c.postReply(dbase.readRandom(cfg.KOAN_STORE))
                    elif random.randrange(0, cfg.REPLY_ODDS) < 1:
                        c.postReply(dbase.readRandom(cfg.REPLY_STORE))

                dbase.writeVisited()

            if not cfg.HOSTED:
                print("\nBleep! All done.")
                break
            else: time.sleep(cfg.SLEEP_LOOP)

        except cfg.ExitException as err:
            print(err)
            exit()
        except ReadTimeout as err:
            time.sleep(60)
            if cfg.DEBUG: print(err + "\nERROR: Reddit timeout, resuming.")
        except Exception as err:
            time.sleep(60)
            if cfg.DEBUG: print(err + "\nERROR: Reddit error, resuming.")
        finally:
            dstore.closeDB()

if __name__ == '__main__':
    main(oauth.auth())
