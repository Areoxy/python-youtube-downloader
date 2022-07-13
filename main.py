from pytube import YouTube
import io 
import os

"""

Code was written by Areo / Envyre Development

"""


def download():
    # text

    start_text = """
D̶̖̺͙̱̩̤̞̰̈͗̍̈͊͗̍͜͝o̴̢̯̻̜̩̫̟̬̰͋͑͂̀͛̀͌͠ẘ̷̨̢̛̺̝̻̭̯͕͊̈͐̌̐́͋̈́n̴͇̹͎̰̳̺̐̍̈́̇͒l̷̡̬͉̞͔̤͔̿̓̔͂̂͐̄̄̆͘͜ͅo̷̢͍̮̟͌a̵̳̳̫͙̲̬̗̼̪̐͑̂d̸̡̰̘̈́̈́̏̍͆ȅ̷̥͖͖̭͚̝̞̯̱̫̌ŗ̵̘̪̰͍̖̲̙̍̈́͐̎͜
    """
    # Get the url and type
    print(start_text)
    youtube_url = input("YouTube URL:")

    print("Choose between mp4 and mp3")

    video_type = input("Type:")

    if not "mp3" or "Mp3" in video_type:
        if not "mp4" or "Mp4" in video_type:
            print("Choose a valid download type and try again")
            return

    # get video information

    if "mp3" or "Mp3" in video_type:
        yt = YouTube(youtube_url)

        stream = yt.streams.get_audio_only()

        title = yt.title

        print("-" * 75)
        print("Video Details: ")
        print("Title: ", yt.title, "\nAuthor: ", yt.author, "\nLength: ", yt.length)
        print("-" * 75)

        # download and save the youtube video

        stream.download(filename=title + ".mp3", filename_prefix="mp3")

        print("Your video was downloaded successfully. You'll find it in the folder of this script")
    else:
        yt = YouTube(youtube_url)

        stream = yt.streams.get_highest_resolution()

        title = yt.title

        print("-" * 75)
        print("File Details: ")
        print("Title: ", yt.title, "\nAuthor: ", yt.author, "\nLength: ", yt.length)
        print("-" * 75)

        # download and save the youtube video

        stream.download(filename=title + ".mp4", filename_prefix="mp4")

        print("Your video was downloaded successfully. You'll find it in the folder of this script")

download()