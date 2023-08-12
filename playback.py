import os
import subprocess
from pytube import YouTube 
import moviepy.editor as mp

SAVE_PATH = "/Users/jkeung/cut/songs/"

def to_path(filename):
    return SAVE_PATH + filename + ".wav"

# filename refers to the filename without the path to folder or extension.

class Playback:
    def __init__(self):
        # Read all files and index what is available
        self.files = self.read_files()

    def read_files(self):
        files = []
        for file in os.listdir(SAVE_PATH):
            if file.endswith(".wav"):
                files.append("".join(file.split(".")[:-1]))
        return files
    
    def play(self, filename):
        if filename not in self.files:
            print("File not found. Either reinitialize Playback or download the file.")
            return
        print(f"Playing {to_path(filename)}")
        return subprocess.call(["afplay", to_path(filename), "-v", ".2"])


class Youtube:
    def download(link):
        stream = YouTube(link).streams.get_audio_only(subtype='mp4')
        if not stream:
            raise Exception("No webm audio streams for this video")
        words = stream.title.lower().split(" ")
        filename = "_".join(words[0:min(len(words), 3)] + [str(stream.filesize_approx)]) # + stream.default_filename.split(".")[-1]
        if not os.path.exists(to_path(filename)):
            stream.download(output_path=SAVE_PATH, filename=filename + ".wav")
            print(f"Downloaded {filename}")

        return filename

class Edit:

    # Takes in two filenames, converts to AudioFileClip objects, saves the concatenated CompositeAudioClip, and returns the filename of the concatenated clip
    def concatenate(filename1, filename2):
        filename = filename1 + "__" + filename2
        if not os.path.exists(to_path(filename)):
            clip1 = mp.AudioFileClip(SAVE_PATH + filename1 + ".wav")
            clip2 = mp.AudioFileClip(SAVE_PATH + filename2 + ".wav")
            final_clip = mp.concatenate_audioclips([clip1, clip2])
            
            final_clip.write_audiofile(to_path(filename), codec="pcm_s32le")

        return filename

    # def cut(filename, start, end):
    #     clip = mp.AudioFileClip(SAVE_PATH + filename).subclip(start, end)
    #     clip.audio.write_audiofile(SAVE_PATH + "cut_" + filename)
    #     return "cut_" + filename


link="https://www.youtube.com/watch?v=E3U_ABHg0J0"
link2="https://www.youtube.com/watch?v=bbmHk1p4TRk"
file1 = Youtube.download(link)
file2 = Youtube.download(link2)

concatenated = Edit.concatenate(file1, file2)

pb = Playback()
pb.play(concatenated)