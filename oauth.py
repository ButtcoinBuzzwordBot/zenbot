import os
import praw
import config as cfg

def auth():

    # Reddit account and API OAuth information. You can hardcode values here but
    # it creates a security risk if your code is public (on Github, etc.)
    # Otherwise, set the environment variables on your host as below.
    cfg.ZENBOT_USERNAME = os.environ['ZENBOT_USERNAME']
    cfg.ZENBOT_PASSWORD = os.environ['ZENBOT_PASSWORD']
    cfg.ZENBOT_ID = os.environ['ZENBOT_ID']
    cfg.ZENBOT_SECRET = os.environ['ZENBOT_SECRET']

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
    return(r)
