import config as cfg

class Comments:
    """ Instance and actions for each comment visited. """

    def __init(self, r, store, comment) -> None:
        self.r = r
        self.store = store
        self.comment = comment
        
    def postReply(self, reply) -> None:
        """ Add the post to list of scored, post reply. """

        if cfg.DEBUG: print("Posting reply:\n"+ reply)
        else: print("X", end="")
        try:
            self.comment.reply(reply + cfg.sig)
            time.sleep(cfg.RATELIMIT)
        except praw.exceptions.APIException as err:
            print(err)
            exit()

    def checkComment(self, comment):
        """ Check a comment or post for the invocation keyword. """

        self.comment = comment
        if type(self.comment) is praw.models.Submission:
            if random.randrange(0, cfg.KOAN_ODDS) < 1:
                print("Post koan")
                exit()
            elif random.randrange(0, cfg.HAIKU_ODDS) < 1:
                print("Post haiku")
                exit()

        else:
            if cfg.DEBUG: print("comment: "+ format(self.comment))
            elif not cfg.HOSTED: print(".", end="", flush=True)
            self.comment.refresh()
            replies = self.comment.replies

            # Traverse comment forest (trees.)
            for reply in replies:
                subcomment = self.r.comment(reply)
                subcomment.refresh()
                checkComment(self, subcomment)

            # Process various triggers if found in comment.
            if alreadyVisited(self, comment): return
            visitedFlag = False
            if (cfg.CMD_KOAN in comment.body):
                visitedFlag = postReply(self, db.readRandom(cfg.KOAN_STORE))
            elif (cfg.CMD_HAIKU in comment.body):
                visitedFlag = postReply(self, db.readRandom(cfg.HAIKU_STORE))

            if visitedFlag:
                db.writeVisited()
