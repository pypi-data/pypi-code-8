import os
import sys
import subprocess
def convert(filename):
    path = os.getcwd()
    filenames = [filename]
    for filename in filenames:
        subprocess.call([
            "ffmpeg", "-i",
            os.path.join(path, filename),
            "-acodec", "libmp3lame", "-ab", "256k",
            os.path.join(OUTPUT_Audio_DIR, '%s.mp3' % filename[:-4])
            ])
    return 0
def video_download(url):
    """
    Provide the url to download the video from YouTube
    eg: video_download('https://www.youtube.com/watch?v=cpPG0bKHYKc')
    """
    video = pafy.new(url)
    best = video.getbest(preftype="mp4")
    print "Downloading started"
    filename = best.download(filepath=OUTPUT_Video_DIR,quiet=False)
    print "File saved to",filename


def audio_download(url):
    """
    Provide the url to download the video from YouTube
    eg: audio_download('https://www.youtube.com/watch?v=cpPG0bKHYKc')
    """
    audio = pafy.new(url)
    best = audio.getbestaudio()
    print "Downloading started"
    filename = best.download(filepath=OUTPUT_Audio_DIR,quiet=False)
    # choice = raw_input("Do you want to convert (yes:no)")
    # if choice=='yes':
    #     convert(filename)
    # else:
    #     pass
    convert(filename)
    subprocess.call(['rm',filename])