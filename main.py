from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import uvicorn
import os
@app.get("/")
def home():
    return {"status": "System Online", "message": "Reddit Checker is ready!"}
app = FastAPI()

# تفعيل CORS للسماح لصفحة GitHub بالاتصال بالـ API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/check/{username}")
async def check_reddit_user(username: str):
    clean_name = username.replace("u/", "").strip()
    # رابط JSON العام (لا يحتاج مفاتيح)
    url = f"https://www.reddit.com/user/{clean_name}/about.json"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json().get('data', {})
            karma = data.get('total_karma', 0)
            created_utc = data.get('created_utc', 0)
            
            return {
                "valid": True,
                "total_karma": karma,
                "created_utc": created_utc
            }
        elif response.status_code == 404:
            return {"valid": False, "error": "User not found"}
        else:
            return {"valid": False, "error": "Reddit blocked the request (429/403)"}
    except Exception as e:
        return {"valid": False, "error": str(e)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
