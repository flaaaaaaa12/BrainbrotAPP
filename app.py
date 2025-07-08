
import secrets
state = secrets.token_urlsafe(16)
print(state)
from flask import Flask,request

app = Flask(__name__)


@app.route("/callback/")

def tiktok_callback():
    code = request.args.get("code")
    state = request.args.get("state")
    
    if not code:
        return "No code received from TikTok.", 400

    return f"Received code: {code}, state: {state}"

link="""https://www.tiktok.com/v2/auth/authorize/
  ?client_key=sbaw6ioomyoljaig8m
  &response_type=code
  &scope=user.info.basic
  &redirect_uri=https://flaaaaaaa12.github.io/BrainbrotAPP/callback.html
  &state=fQBifn-mvB3JDXn___JmLw
"""

Bss9OFU_nOurqWT306Yulw
#import requests

url = "https://open.tiktokapis.com/v2/oauth/token/"
payload = {
    "client_key": "sbaw6ioomyoljaig8m",
    "client_secret": "baQjwqZIoh9RmNIjVUTaaekjgxCYEmwr",
    "code": "CEFiu7Pac0qtCaBhhVtI08Zx3hJ2DFJehsSOHLyFk2lHa7F7HU8FMY3-G2fiCy-SUYniLj0P1-c2_MvC7Zs9pLGEnnPIYPpXNxIzAlEIiN9HxTRbxbKxobotYbtyKAI5ofaMUdikKdB2yiqRytCnWlEzsoew3LMDsvOd2k1u8HfmkYt4ciCetKdbwTi9zf0jTKXQHN0FXdlvveQd12WYow*1!6406.u1",
    "grant_type": "authorization_code",
    "redirect_uri": "https://3282-82-124-130-233.ngrok-free.app/callback/"
}

#response = requests.post(url, data=payload)
#tokens = response.json()
#print(tokens)
