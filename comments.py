import time
import praw
import config as cfg, rants

class Comments:
    """ Instance and actions for each comment visited. """

    def __init__(self, db=None, r=None, post=None) -> None:
        self.db = db
        self.r = r
        if type(post) is not praw.models.Submission:
            post.refresh()
        self.post = post

    def getParent(self) -> str:
        """ Returns the parent of post. """

        if type(self.post) is praw.models.Submission:
            return(self.post)
        elif type(self.post) is praw.models.Comment:
            return(self.post.parent())

    def markVisited(self) -> None:
        """ Mark a post as visited if not duplicate. """

        id = str(self.post.id)
        if type(self.post) is praw.models.Submission:
            id = "sub " + id

        if id not in cfg.already_visited:
            cfg.already_visited.append(id)

    def alreadyVisited(self) -> bool:
        """ Checks if a post had already been visited. """

        id = str(self.post.id)
        if type(self.post) is praw.models.Submission:
            id = "sub " + id

        if id in cfg.already_visited:
            if cfg.DEBUG: print("Already visited, skipping.")
            return True
        return False

    def postReply(self, reply) -> None:
        """ Add the post to list of visited, post reply. """

        if cfg.DEBUG:
            print("Posting reply to "+ str(self.post.id) +":\n"+ reply)
        elif not cfg.HOSTED: print("X", end="")

        parent = self.getParent()    
        if parent.author is None or parent.author == "[deleted]":
            if cfg.DEBUG: print("Post was deleted, skipping.")
            return None
        elif parent.author == cfg.ZENBOT_USERNAME:
            if cfg.DEBUG: print("Reply is to bot, skipping.")
            return None
        elif parent.author == cfg.AUTHOR:
            if cfg.DEBUG: print("Replying to poster instead.")
            parent = self.post
            
        try:
            parent.reply(reply + cfg.sig)
            time.sleep(cfg.RATELIMIT)
            self.db.writeVisited()
        except praw.exceptions.APIException as err:
            raise cfg.ExitException(err)
        except:
            raise cfg.ExitException("ERROR: Post reply error.")

    def checkComment(self) -> None:
        """ Post replies to random submissions and trigger replies. """

        if cfg.DEBUG: print("comment: "+ format(self.post))
        elif not cfg.HOSTED: print(".", end="", flush=True)

        replies = self.post.replies
        for reply in replies:
            newc = Comments(self.db, self.r, reply)
            newc.checkComment()

        if self.alreadyVisited():
            return
        self.markVisited()

        if (cfg.TRIGGER in self.post.body):
            if (cfg.CMD_KOAN in self.post.body):
                self.postReply(self.db.readRandom(cfg.KOAN_STORE))
            elif (cfg.CMD_RANT in self.post.body):
                self.postReply(rants.Rants(self.db).getTemplate())
            elif (cfg.CMD_HAIKU in self.post.body):
                self.postReply(self.db.readRandom(cfg.HAIKU_STORE))
            elif (cfg.CMD_REPLY in self.post.body):
                self.postReply(cfg.botReply(self.db.readRandom(cfg.REPLY_STORE)))
            cfg.already_visited.append(str(self.post.id))
