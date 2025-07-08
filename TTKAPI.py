import os
import requests
from systemfunctions import *

init_url = "https://open.tiktokapis.com/v2/video/upload/init/"
headers = {
    "Authorization": "Bearer act.KHobYcnZzrSMsrtx4w4WwJaS9U8QhuNtIvFyxdSbvt4HTSwyvCX84kD3JGSi!6383.u1"
}
params = {
    "fields": "username"
}

response = requests.get("https://open.tiktokapis.com/v2/user/info/", headers=headers,params=params)
print(response.json())

class TTKCLIENT:
    def __init__(self,token):
        self.token = token
        self.path="C:/Users/flori/Brainbrot"
        url = "https://open.tiktokapis.com/v2/post/publish/creator_info/query/"
        headers = {
            "Authorization": "Bearer YOUR_ACCESS_TOKEN",
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers)
        print(response.json())

    def post(self,amount,id=None,delay=0):
        if id:
            if os.path.exists(os.path.normpath(self.path+f"/media/stories/story{id}")):
                infos=readfile(os.path.normpath(self.path+f"/media/stories/story{id}"))
                url=infos["redditurl"]
                title=infos["title"]
                ttkposted=infos["ttkposted"]
   
                for file in os.listdir(self.path+"/media/topost"):
                    if file.find(str(id)):
                        parts=file.replace(f"{id}part","").replace(".mp4","").split("_")
                        part,total=parts[0],parts[1]
                        
                        print(f"filename:{file} | part:{part}/{total}")
                        
                        init_payload = {
                            "upload_type": "video",  # always "video" for Direct Post
                            "video_type": "mp4"      # or mov
                        }

                        res = requests.post(init_url, json=init_payload, headers=headers)
                        upload_info = res.json()
                        print("Step 1:", upload_info)

                        # Extract URL and video_id
                        upload_url = upload_info['data']['upload_url']
                        video_id = upload_info['data']['video_id']

                        # Step 2: Upload video via PUT to the presigned URL
                        with open(self.path+f"/media/topost/{file}", "rb") as f:
                            video_data = f.read()

                        put_headers = {
                            "Content-Type": "application/octet-stream"
                        }
                        upload_res = requests.put(upload_url, data=video_data, headers=put_headers)
                        print("Step 2:", upload_res.status_code)

                        # Step 3: Publish the video
                        publish_url = "https://open.tiktokapis.com/v2/video/publish/"
                        publish_payload = {
                            "video_id": video_id,
                            "title": title,
                            "visibility": "public",
                            "disable_download": True
                        }

                        publish_res = requests.post(publish_url, json=publish_payload, headers=headers)
                        print("Step 3:", publish_res.json())

            else: print(f"TTKPOST Error : unable to locate story with id {id}")
        else:
            for file in os.listdir(self.path+"/media/topost"):
                fname=os.path.basename(file)
                