from fastapi import FastAPI
import praw
import os

app = FastAPI()

# استخدام متغيرات البيئة التي ضبطناها في Render
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent="checker_v1"
)

@app.get("/check/{username}")
def check_user(username: str):
    try:
        user = reddit.redditor(username)
        return {
            "karma": user.comment_karma + user.link_karma,
            "created_utc": user.created_utc,
            "valid": True
        }
    except Exception as e:
        return {"valid": False, "error": str(e)}
