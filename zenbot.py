# Bleep bloop! I am a Zen Bot. Om.

import sys, random, time

import prawcore

import config as cfg
import db
import comments
import cmdline, oauth

def checkInbox(r, dbase):
    """ Check inbox and reply randomly to new messages from regular users. """

    try:
        msgs = list(r.inbox.unread(limit=None))
        if cfg.DEBUG or (len(msgs) > 0 and not cfg.HOSTED):
            print(str(len(msgs))
                  + " message(s) in /u/"+ cfg.ZENBOT_USERNAME +"\'s inbox.")
    except prawcore.exceptions.ServerError as err:
        print("ERROR: Cannot connect to server, skipping...")
        return
    except:
        print("ERROR: Error connecting...")
        return
        
    for msg in msgs:
        msg.mark_read()
        if msg.author not in cfg.IGNORE:
            try:
                msg.reply(cfg.botReply(dbase.readRandom(cfg.REPLY_STORE)) + cfg.sig)
            except:
                pass

def main(r):
    """ Initialize and recurse through posts. """

    dbase = db.DB(cfg.STORE_TYPE)
    if len(sys.argv) > 1:
        cmdline.processOpts(dbase, sys.argv)
    dbase.checkDB()
    if cfg.DEBUG and not cfg.HOSTED:
        print ("Type CTRL-C to exit.")

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
                    if random.randrange(0, cfg.KOAN_ODDS) < 1:
                        c.postReply(dbase.readRandom(cfg.KOAN_STORE))
                    elif random.randrange(0, cfg.HAIKU_ODDS) < 1:
                        c.postReply(dbase.readRandom(cfg.HAIKU_STORE))
                    elif random.randrange(0, cfg.REPLY_ODDS) < 1:
                        c.postReply(dbase.readRandom(cfg.REPLY_STORE))

                dbase.writeVisited()

            if not cfg.HOSTED:
                print("\nBleep! All done.")
                break
            else:
                if cfg.DEBUG: print("Sleeping. Zzzz...")
                time.sleep(cfg.SLEEP_LOOP)

        except cfg.ExitException as err:
            print(err)
            exit()
        except Exception as err:
            if cfg.DEBUG: print(format(err) + "\nERROR: Reddit timeout, will resume.")
            time.sleep(cfg.SLEEP_TIMEOUT)

    dbase.closeDB()

if __name__ == '__main__':
    main(oauth.auth())
