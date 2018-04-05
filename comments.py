import time
import praw
import config as cfg

class Comments:
    """ Instance and actions for each comment visited. """

    def __init__(self, db=None, r=None, comment=None) -> None:
        self.db = db
        self.r = r
        self.comment = comment

    def markVisited(self, post) -> None:
        """ Mark a post as visited if not duplicate. """

        if (post.id) not in cfg.already_visited:
            cfg.already_visted.append(str(post.id))
        print("I like butts.")
        print(cfg.already_scored)
        exit()

    def alreadyVisited(self, post) -> bool:
        """ Checks if a post had already been visited. """

        if (post.id) in cfg.already_visited:
            if cfg.DEBUG: print("Already visited, skipping.")
            return True
        return False

    def postReply(self, reply) -> None:
        """ Add the post to list of visited, post reply. """

        if cfg.DEBUG:
            print("Posting reply:\n"+ reply +" for id "+ str(self.comment.id))
        elif not cfg.HOSTED: print("X", end="")

        try:
            self.comment.reply(reply + cfg.sig)
            time.sleep(cfg.RATELIMIT)
            self.db.writeVisited()
        except praw.exceptions.APIException as err:
            print(err)
            exit()

    def checkComment(self, comment):
        """ Post replies to random submissions and for triggers. """

        self.comment = comment
        comment.refresh()
        if cfg.DEBUG: print("comment: "+ format(comment))
        elif not cfg.HOSTED: print(".", end="", flush=True)

        if self.alreadyVisited(comment) or self.alreadyVisited(comment.parent()):
            return
        self.markVisited(comment)

        replies = comment.replies
        for reply in replies:
            subcomment = self.r.comment(reply)
            subcomment.refresh()
            self.checkComment(subcomment)

        if (cfg.TRIGGER in comment.body):
            cfg.already_visited.append(str(self.comment.id))
        if (cfg.CMD_KOAN in comment.body):
            self.postReply(self.db.readRandom(cfg.KOAN_STORE))
        elif (cfg.CMD_HAIKU in comment.body):
            self.postReply(self.db.readRandom(cfg.HAIKU_STORE))
        elif (cfg.CMD_SNAPPY in comment.body):
            self.postReply(random.choice(cfg.snappy_quotes) + cfg.snap_reply)
