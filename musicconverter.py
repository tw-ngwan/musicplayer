import os, sys, time, pyinputplus as pyip

from moviepy.editor import VideoFileClip

os.chdir("C:/Users/Tengwei/Downloads")

usage = """Usage: This programme will be able to either convert individual video files into audio (with their names), 
or convert all video files within a certain period into audio files. If not specified, this will automatically be taken to be 1 day. 
Key in py musicconverter.py n for the first, and py musicconverter.py t <time, in hours> for the second. For the first, 
you will be prompted to key in the names. Separate them by a space. 
"""

directory = 'C:/Users/Tengwei/Downloads'

def main():
    if len(sys.argv) < 2:
        print(usage)
    elif sys.argv[1].lower() == "n":
        convert_files_with_name()
    elif sys.argv[1].lower() == "t":
        if len(sys.argv) == 2:
            time_to_subtract = 86400
        else:
            time_to_subtract = sys.argv[2] * 3600
        convert_files_with_time(time_to_subtract)
    else:
        print("No such function!")
        print(usage)
        sys.exit()


def convert_files_with_name():
    files_string = input("Copy the links you want to download, separated by a space \n")
    video_files = files_string.split()
    convert_video_to_audio(video_files)
    print("All video files converted!")


def convert_files_with_time(time_to_subtract):
    current_time = time.time()
    video_files = []
    backdated_time = current_time - time_to_subtract
    for file in os.listdir(directory):
        if file.endswith('.mp4') and os.path.getctime(f'{directory}/{file}') >= backdated_time:
            video_files.append(file)
            print(file)

    convert_video_to_audio(video_files)
    print("All video files converted!")


def convert_video_to_audio(video_files):
    os.chdir(directory)
    for video_file in video_files:
        filename, ext = os.path.splitext(video_file)

        clip = VideoFileClip(video_file)
        clip.audio.write_audiofile(f"{filename}.mp3", verbose=False, progress_bar=False)
        clip.__del__()
        print("Video file converted!")

    delete_file_choice = pyip.inputYesNo("Do you want to delete the video files?")
    if delete_file_choice == 'yes':
        for video_file in video_files:
            os.remove(video_file)
        print("All video files deleted!")


if __name__ == "__main__":
    convert_video_to_audio([r'C:\Users\Tengwei\Downloads\pianomusic2h.mp4'])
