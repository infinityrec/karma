from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import praw
import os
from datetime import datetime, timedelta

app = FastAPI()

# 1. إعدادات CORS: تسمح لصفحة GitHub بالوصول إلى الـ API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # يمكنك استبداله برابط GitHub Pages الخاص بك لزيادة الأمان
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. إعداد الاتصال بـ Reddit باستخدام متغيرات البيئة (Environment Variables)
# تأكد من إضافة هذه المفاتيح في لوحة تحكم Render كما شرحنا سابقاً
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    password=os.getenv("REDDIT_PASSWORD"),
    user_agent=os.getenv("REDDIT_USER_AGENT", "checker_v1"),
    username=os.getenv("REDDIT_USERNAME"),
)

@app.get("/")
def read_root():
    return {"message": "Reddit Checker API is Running!"}

@app.get("/check/{username}")
async def check_user(username: str):
    try:
        # تنظيف اسم المستخدم من أي إضافات مثل u/
        clean_username = username.replace("u/", "").strip()
        user = reddit.redditor(clean_username)
        
        # جلب البيانات الأساسية
        # ملاحظة: بعض البيانات قد تتطلب عمل "load" للملف الشخصي
        karma = user.comment_karma + user.link_karma
        created_utc = user.created_utc
        
        return {
            "valid": True,
            "username": clean_username,
            "total_karma": karma,
            "created_utc": created_utc
        }
    except Exception as e:
        # في حال لم يتم العثور على المستخدم أو حدث خطأ في الاتصال
        return {
            "valid": False, 
            "error": "User not found or Reddit API error"
        }

if __name__ == "__main__":
    import uvicorn
    # Render يستخدم المنفذ 10000 افتراضياً
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
