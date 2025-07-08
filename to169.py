import ffmpeg
import os

def convert_to_9_16(inputfile, outputfile):
    inputfile = os.path.normpath(inputfile)
    outputfile = os.path.normpath(outputfile)

    print(f"Processing: {inputfile} → {outputfile}")

    # Get input video dimensions
    probe = ffmpeg.probe(inputfile)
    video_streams = [stream for stream in probe["streams"] if stream["codec_type"] == "video"]

    if not video_streams:
        raise ValueError("No video stream found in the input file.")

    width = int(video_streams[0]["width"])
    height = int(video_streams[0]["height"])

    # Ensure height matches 9:16 ratio
    target_height = height
    target_width = int((height * 9) / 16)

    # Center crop if needed
    x_offset = (width - target_width) // 2 if width > target_width else 0

    # FFmpeg processing
    stream = ffmpeg.input(inputfile)
    stream = stream.filter("crop", target_width, target_height, x_offset, 0)
    stream = ffmpeg.output(stream, outputfile, vcodec="libx264", an=None)  # Remove audio
    ffmpeg.run(stream)


convert_to_9_16("C:/Users/flori/Brainbrot/zzz/satisf1.mp4", "C:/Users/flori/Brainbrot/zzz/satis1.mp4")
