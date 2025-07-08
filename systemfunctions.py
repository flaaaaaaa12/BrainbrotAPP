import ffmpeg
import os
import subprocess
from moviepy import *
import ffmpeg
import random
import os
import ffmpeg
import hashlib
import json
import re

def GenIDfTitle(title, max_length=12):
    title = title.lower().encode("utf-8")
    hash_value = hashlib.sha256(title).hexdigest()
    numeric_id = "".join(str(ord(char)) for char in hash_value[:max_length])
    return numeric_id[:max_length]

def time_to_seconds(time_str):
    """ Convertit un timestamp hh:mm:ss.sss en secondes """
    parts = time_str.split(":")
    if len(parts) != 3:
        raise ValueError(f"Format invalide du timestamp : {time_str}")

    hours, minutes = map(int, parts[:2])
    seconds = float(parts[2])
    return hours * 3600 + minutes * 60 + seconds

def format_time(seconds):
    """ Formate un temps en hh:mm:ss.sss avec des zéros correctement placés """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02}:{minutes:02}:{secs:06.3f}"  # Assure trois chiffres après le point et deux avant

def split_subtitles(input_vtt, output_vtt):
    with open(input_vtt, "r", encoding="utf-8-sig") as f:
        lines = f.readlines()

    new_subtitles = []
    timestamp = None
    last_end_time = 0.0

    for line in lines:
        if "-->" in line:
            line = line.replace(",",".")
            line = line.replace("�"," ")
            timestamp = line.strip()
        elif timestamp and line.strip():
            line = line.replace(",",".")
            line = line.replace("�"," ")
            words = line.strip().split()
            start_time, end_time = timestamp.split(" --> ")
            
            try:
                start_seconds = time_to_seconds(start_time)
                end_seconds = time_to_seconds(end_time)
            except ValueError as e:
                print(f"Erreur de timestamp : {e}")
                continue

            total_chars = sum(len(word) for word in words)
            duration_per_char = (end_seconds - start_seconds) / total_chars
            
            for word in words:
                word_duration = len(word) * duration_per_char

                new_start = max(start_seconds, last_end_time)
                new_end = new_start + word_duration

                formatted_start = format_time(new_start)
                formatted_end = format_time(new_end)

                new_subtitles.append(f"{formatted_start} --> {formatted_end}\n{word}\n\n")

                last_end_time = new_end
                start_seconds = new_end

            timestamp = None

    with open(output_vtt, "w", encoding="utf-8") as f:
        f.writelines(new_subtitles)

def cleartemp():
    tempdir=os.path.normpath("C:/Users/flori/Brainbrot/temp")
    for file in os.listdir(tempdir):
        print(f"Deleted : {file}")
        os.remove(os.path.join(tempdir,file))

def mergeVAS(videofile, audiofile, subtitlefile, outputfile):
    videofile=os.path.normpath(videofile)
    audiofile=os.path.normpath(audiofile)
    subtitlefile=os.path.abspath(subtitlefile)
    outputfile=os.path.normpath(outputfile)
    subtitlefile = os.path.relpath(subtitlefile).replace("\\", "/")

    video=ffmpeg.input(videofile)
    audio=ffmpeg.input(audiofile)
    
    stream=ffmpeg.output(audio, video, outputfile, vcodec="libx264",vf=f"subtitles={subtitlefile}", acodec="aac",preset="fast")
    ffmpeg.run(stream)
    cleartemp()

def cutvideo(inputfile, outputfile, start, end,keepsound=False,burntext=None):
    inputfile=os.path.normpath(inputfile)
    outputfile=os.path.normpath(outputfile)
    print(f"cutvideo / [inp]:{inputfile}, [out]:{outputfile}, [sta]:{start}, [end]:{end}")
    stream = ffmpeg.input(inputfile, ss=start, to=end)

    if burntext:
        font = "C:/Windows/Fonts/arial.ttf"
        font_size = 90
        font_color = "white"
        x_position = "(w-text_w)/2"
        y_position = "160"

        stream = stream.filter(
            "drawtext",
            text=burntext,
            fontfile=font,
            fontsize=font_size,
            fontcolor=font_color,
            x=x_position,
            y=y_position
        )
    if keepsound: 
        stream = ffmpeg.output(stream, outputfile, vcodec="libx264",force_key_frames=f"expr:gte(t,{start})", acodec="aac", audio_bitrate="192k", map="0:a")
    else:
        stream = ffmpeg.output(stream, outputfile, vcodec="libx264", acodec="copy",an=None,force_key_frames=f"expr:gte(t,{start})")
    ffmpeg.run(stream)
    print('finished')

def cutaudio(inputfile, outputfile, start, end):
    inputfile=os.path.normpath(inputfile)
    outputfile=os.path.normpath(outputfile)
    print(f"cutaudio / [inp]:{inputfile}, [out]:{outputfile}, [sta]:{start}, [end]:{end}")
    stream = ffmpeg.input(inputfile, ss=start, to=end)
    stream = stream.output(outputfile)
    ffmpeg.run(stream)

def choserandomfile(directory):
    directory = os.path.normpath(directory)
    print(f"Checking directory: {directory}")
    if not os.path.isdir(directory):
        raise ValueError(f"Invalid directory: {directory}")

    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    if not files:
        return None

    return os.path.join(directory, random.choice(files))

def getduration(file):
    file=os.path.normpath(file)
    metadata = ffmpeg.probe(file)
    return float(metadata['format']['duration'])

def countfolders(folderpath):
    if not os.path.exists(folderpath):
        print("Le dossier spécifié n'existe pas.")
        return 0
    folders = [nom for nom in os.listdir(folderpath) if os.path.isdir(os.path.join(folderpath, nom))]
    return len(folders)

def readfile(file):
    with open(file, "r", encoding="utf-8") as f:
        return f.readlines()

def writefile(file,data):
    with open(file, "w", encoding="utf-8") as f:
        f.writelines(data)

def writetojson(file,data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def reversetimeformat(time):
    if not isinstance(time,float):
        parts = time.split(":")
        if len(parts) != 3:
            raise ValueError(f"Format invalide du timestamp : {time}")
        hours, minutes = map(int, parts[:2])
        seconds = float(parts[2])
        return hours * 3600 + minutes * 60 + seconds
    else:
        hours = int(time // 3600)
        minutes = int((time % 3600) // 60)
        secs = time % 60
        return f"{hours:02}:{minutes:02}:{secs:06.3f}"
    
def mergesubfile(file1,file2,outputfile):
    file1 = os.path.normpath(file1)
    file2 = os.path.normpath(file2)
    outputfile = os.path.normpath(outputfile)

    file1lines = readfile(file1)
    file2lines = readfile(file2)

    lasttimestamp=None
    for f1line in file1lines:
        if "-->" in f1line:
            starttimestamp,endtimestamp = f1line.split(" --> ")
            print(starttimestamp,endtimestamp)
            lasttimestamp=reversetimeformat(endtimestamp)
        
    print(f"finished {lasttimestamp}" )
    updatedtimestamps=[]

    previousstamp=lasttimestamp
    for f2line in file2lines:
        newline=None
        if " --> " in f2line:
            starttimestamp,endtimestamp = f2line.split(" --> ")

            starttimestamp=reversetimeformat(starttimestamp)
            endtimestamp=reversetimeformat(endtimestamp)
            duration=endtimestamp-starttimestamp

            newstarttime=reversetimeformat(previousstamp)
            newendtime=reversetimeformat((previousstamp+duration))
            
            previousstamp=previousstamp+duration
            newline=f"{newstarttime} --> {newendtime} \n"
        else:
            newline=f2line
        updatedtimestamps.append(newline)

    mergedlines = ["WEBVTT\n\n"] + file1lines[1:] + ["\n"] + updatedtimestamps
    writefile(outputfile,mergedlines)
    print("Success : merged vtt files")

def cutsubfile(inputfile, start, end, outputfile):
    print(f"cutsub:[start]:{start}_[end]:{end}")
    inputfile = os.path.normpath(inputfile)
    outputfile = os.path.normpath(outputfile)
    retstart=None
    with open(inputfile, "r", encoding="utf-8") as f:
        lines = f.readlines()
    keep_lines=False
    updated_vtt = []
    for line in lines:
        print(line)
        
        timestamp_match = re.search(r"(\d+):(\d+):(\d+\.\d+)", line)
        if timestamp_match:
            timestamp = reversetimeformat(timestamp_match.group(0))
            if (retstart==None) and (start <= timestamp <= end) :
                retstart=timestamp
            keep_lines = start <= timestamp <= end
        if keep_lines:
            updated_vtt.append(line)

    writefile(outputfile, updated_vtt)
    return retstart

def mergeaudio(file1,file2,outputfile):
    file1 = os.path.normpath(file1)
    file2 = os.path.normpath(file2)
    outputfile = os.path.normpath(outputfile)

    input1 = ffmpeg.input(file1)
    input2 = ffmpeg.input(file2)
    stream = ffmpeg.concat(input1.audio, input2.audio, n=2, v=0, a=1)
    stream = stream.output(outputfile)
    ffmpeg.run(stream)

def VTTtoASS(inputfile, outputfile):
    inputfile = os.path.normpath(inputfile)
    outputfile = os.path.normpath(outputfile)

    lines = readfile(inputfile)
    
    ass_header = """[Script Info]
Title: Converted Subtitles
ScriptType: v4.00+
PlayResY: 720

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, ShadowColour, Alignment, MarginL, MarginR, MarginV
Style: Default,Arial,30,&H00FFFFFF,&H00000000,&H00000000,6,10,10,300

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"""

    ass_events = []
    time_pattern = re.compile(r'(\d{2}):(\d{2}):(\d{2})\.(\d{3})')

    for line in lines:
        if '-->' in line:
            start, end = line.strip().split(' --> ')
            start = time_pattern.sub(r'\1:\2:\3.\4', start)
            end = time_pattern.sub(r'\1:\2:\3.\4', end)
        elif line.strip() and not line.startswith('WEBVTT'):
            text = line.strip()
            ass_events.append(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}")

    writefile(outputfile,ass_header + '\n'.join(ass_events))