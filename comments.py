class Comments:
    """ Instance and actions for each comment visited. """

    def __init(self):
        
    def postReply(reply):
        """ Add the post to list of scored, post reply. h"""

        if cfg.DEBUG: print("Posting reply:\n" + reply)
        else: print("X", end="")
        try:
            post.reply(reply + cfg.sig)
            time.sleep(cfg.RATELIMIT)
        except praw.exceptions.APIException as err:
            print(err)
            exit()


def checkComment (*args):
    """ Check a comment or post for the invocation keyword. """

    store = args[0]
    r = args[1]
    comment = args[2]

    if cfg.DEBUG: print("comment: " + format(comment))
    elif not cfg.HOSTED: print(".", end="", flush=True)
    comment.refresh()
    replies = comment.replies

    # Traverse comment forest (trees.)
    for reply in replies:
        subcomment = r.comment(reply)
        subcomment.refresh()
        checkComment(store, r, subcomment)

    # Process various triggers if found in comment.
    scoredFlag = False
    if scr.alreadyScored(r, comment): return
    if (cfg.CMD_HS in comment.body):
        scoredFlag = postReply(comment, cfg.highscoresReply(cfg.highscores))
    elif (cfg.CMD_KOAN in comment.body):
        scoredFlag = postReply(comment, ds.readRandom(store, cfg.KOAN_STORE))
    elif (cfg.CMD_HAIKU in comment.body):
        scoredFlag = postReply(comment, ds.readRandom(store, cfg.HAIKU_STORE))
    elif (cfg.TRIGGER in comment.body):
        if cfg.CMD_SCORE in comment.body:
            regex = re.compile(cfg.CMD_SCORE + "\s+([0-9]+)\s*")
            tempscore = regex.search(comment.body).group(1)
            if tempscore is not None:
                needed = int(tempscore)

        parent = comment.parent()
        print("parent: " + format(parent))
        if not cfg.DEBUG:
            if scr.alreadyScored(r, parent): return
            elif comment.author == parent.author.name: return
            #elif comment.author.name != cfg.AUTHOR: return
        else:
            scr.markScored(parent)
            scoredFlag = scr.playBingo(comment, getText(parent))
    if scoredFlag:
        ds.writeScored(store, cfg.SCORED_STORE)
