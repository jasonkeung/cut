import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer
from pytube import YouTube 

SAVE_PATH = "/home/jasonkeung/cut/songs/"


class Playback:
    def play(file):
        mixer.init()
        mixer.music.load(file)
        mixer.music.play()


class Youtube:
    def download(link):
        stream = YouTube(link).streams.get_audio_only(subtype='mp4')

        if not stream:
            raise Exception("No mp4 audio streams for this video")
        
        filename = "_".join(stream.title.lower().split(" ")[0:5]) + "." + stream.default_filename.split(".")[-1]
        stream.download(output_path=SAVE_PATH, filename=filename)
        print(f"Downloaded {filename}")

        return filename


link="https://www.youtube.com/watch?v=xWOoBJUqlbI"
downloaded_filename = Youtube.download(link)



Playback.play(SAVE_PATH + downloaded_filename)