from CRAWLER import CRAWLER
from AWSGEN import AWSCLI
from systemfunctions import *
import random
import json
import math
import os

class GENERATOR:
    def __init__(self,outformat="mp3",VoiceId="Matthew",maxTTSinputlen=3000):
        self.AWSCLIENT=AWSCLI(OutputFormat=outformat,VoiceId=VoiceId)
        self.CRAWLIENT=CRAWLER()
        self.maxTTSIL=maxTTSinputlen
        self.projectpath="C:/Users/flori/Brainbrot"

    def crawlSUBr(self,amount):
        self.CRAWLIENT.appendposts("AITAH",amount)

    def generatestories(self,subs=True,postamount=1,maxuseamount=1,defaultinpfile="posts.json"):
        sourcefile=os.path.join("media/redditposts",defaultinpfile)
        postcount=0

        with open(sourcefile, "r", encoding="utf-8") as JSONcontent:
            posts=json.load(JSONcontent)
            for post in posts:
                if int(post["postcount"]) <= maxuseamount and postcount<postamount:
                    title=post["title"]
                    content=post["content"]
                    postc=post["postcount"]

                    id=GenIDfTitle(title=title)
                    newfolderpath=None
                    if not os.path.exists(f"{self.projectpath}/media/stories/story{id}"):
                        print("creating")
                        newfolderpath=os.path.normpath(f"{self.projectpath}/media/stories/story{id}")
                        os.makedirs(newfolderpath, exist_ok=True)

                        self.AWSCLIENT.generate(title,newfolderpath+"\stitle")

                        if len(content) > self.maxTTSIL:
                            middle = len(content) // 2
                            while middle < len(content) and content[middle] != " ":
                                middle += 1
                            p1,p2 = content[:middle], content[middle:].strip()

                            self.AWSCLIENT.multigenerate(saveloc=newfolderpath,sub=subs,Voice="Matthew",part1=p1,part2=p2)
                        else:
                            self.AWSCLIENT.generate(content,newfolderpath+"\speech",sub=subs)

                        postc=postc+1
                        postcount=postcount+1
                    else : newfolderpath=os.path.normpath(f"{self.projectpath}/media/stories/story{id}")

                    writetojson(sourcefile,posts)

                    postdata={
                        "title":title,
                        "id":id,
                        "ttkposted":0,
                        "redditurl":post["url"]
                    }

                    writetojson(newfolderpath+"\infos.json",postdata)

                    backgroundv=choserandomfile(self.projectpath+"/media/finalvideos")
                    titleduration=getduration(newfolderpath+"\stitle.mp3")
                    backgroundvduration=getduration(backgroundv)
                    audioduration=getduration(newfolderpath+"\speech.mp3")
                    
                    parts=audioduration/61
                    if parts > 1 :
                        totalparts = math.ceil(parts)
                        starttime=random.randint(0,int(backgroundvduration-(audioduration+titleduration*totalparts)))   #only for background  
                        partlength = audioduration / totalparts + titleduration if (audioduration - (totalparts-1) * 61) >= 40 else audioduration / (totalparts-1) + titleduration

                        for part in range(1,totalparts):
                            endtime=starttime+partlength*part

                            cutvideo(backgroundv,self.projectpath + "/temp/temppart.mp4",starttime + partlength * (part-1),1 + endtime,burntext=f"Part {part}/{totalparts-1}")
                            print(f"start:{(partlength - titleduration)*(part-1)} end:{(partlength - titleduration)*part}")
                            startsub=cutsubfile(newfolderpath + "/speech.mp3.vtt", 0 + (partlength - titleduration)*(part-1),0 + (partlength - titleduration)*part , self.projectpath + "/temp/temp.vtt")
                            mergesubfile(newfolderpath + "/stitle.mp3.vtt", self.projectpath + "/temp/temp.vtt", self.projectpath + "/temp/merged.vtt")
                            print(f"STARTTTTTTT {startsub}")
                            
                            cutaudio(newfolderpath + "/speech.mp3", self.projectpath + "/temp/tempaud.mp3", startsub,1 + (partlength - titleduration)*part)
                            mergeaudio(newfolderpath + "/stitle.mp3", self.projectpath + "/temp/tempaud.mp3", self.projectpath + "/temp/merged_audio.mp3")

                            split_subtitles(self.projectpath + "/temp/merged.vtt",self.projectpath + "/temp/smerged.vtt")

                            mergeVAS(self.projectpath + "/temp/temppart.mp4", self.projectpath + "/temp/merged_audio.mp3", self.projectpath + "/temp/smerged.vtt", self.projectpath + f"/media/topost/{id}part{part}_{totalparts-1}.mp4")
                            cleartemp()
gen = GENERATOR()
gen.generatestories(subs=True,postamount=1,maxuseamount=1)