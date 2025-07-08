from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir
from systemfunctions import mergesubfile
from polly_vtt import PollyVTT
from VIDMOD import merge_vtt
import ffmpeg

class AWSCLI:
    def __init__(self,profile="adminuser",region="eu-west-2",VoiceId="Matthew",OutputFormat="mp3"):
        self.outformat = OutputFormat
        self.VoiceId = VoiceId
        self.session = Session(profile_name=profile,region_name=region)
        self.polly = self.session.client("polly")

    def generate(self,text,saveloc,sub=True,Voice="Matthew"):
        if sub :
            polly_vtt = PollyVTT()
            polly_vtt.generate(
                saveloc,
                Text=text,
                VoiceId=Voice,
                OutputFormat="mp3",
                
            )
        else :
            polly = self.polly
            try:
                response = polly.synthesize_speech(Text=text, OutputFormat=self.outformat,VoiceId=Voice)
            except (BotoCoreError, ClientError) as error:
                print(error)
                sys.exit(-1)

            if "AudioStream" in response:
                    with closing(response["AudioStream"]) as stream:
                        output = os.path.join(saveloc)
                        print(output)
                    try:
                        with open(output, "wb") as file:
                            file.write(stream.read())
                    except IOError as error:
                        print(error)
                        sys.exit(-1)
            else:
                print("Could not stream audio")
                sys.exit(-1)
            return output
        
    def multigenerate(self, saveloc, sub=True, Voice="Matthew", **parts):
        """Generates multiple TTS audio files and merges them using FFmpeg."""
        polly_vtt = PollyVTT()

        parts_filtered = {key: value for key, value in parts.items() if "part" in key}
        sorted_parts = sorted(parts_filtered.items(), key=lambda x: int(x[0].replace("part", "")))

        audio_files = []

        for key, text in sorted_parts:
            partnumber = int(key.replace("part", ""))
            output_file = os.path.join(saveloc, f"speech{partnumber}.mp3")

            if sub:
                polly_vtt.generate(output_file, Text=text, VoiceId=Voice, OutputFormat="mp3")
            else:
                try:
                    response = self.polly.synthesize_speech(Text=text, OutputFormat=self.outformat, VoiceId=Voice)
                    if "AudioStream" in response:
                        with closing(response["AudioStream"]) as stream:
                            with open(output_file, "wb") as file:
                                file.write(stream.read())
                    else:
                        raise ValueError("Audio stream could not be retrieved.")
                except (BotoCoreError, ClientError) as error:
                    print(f"Error synthesizing speech: {error}")
                    sys.exit(-1)

            audio_files.append(output_file)

        if sub:
            vtt_files = [f"{file}.vtt" for file in audio_files]
            mergesubfile(*vtt_files, os.path.join(saveloc, "speech.mp3.vtt"))

        concat_file = os.path.join(saveloc, "concat_list.txt")
        with open(concat_file, "w") as f:
            for file in audio_files:
                f.write(f"file '{file}'\n")

        ffmpeg.input(concat_file, format="concat", safe=0).output(os.path.join(saveloc, "speech.mp3"), acodec="copy").run()

        return "Success!"