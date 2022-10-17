import os
import sys
import pyinputplus as pyip
from moviepy.editor import VideoFileClip
import sqlite3
from backend_implementations import input_parse
from settings import musicconverter_usage, database_name


# The main function that is called
def main():
    # Handling incorrect usage
    if len(sys.argv) < 2:
        print(musicconverter_usage)
        return
    # Convert video by video
    if sys.argv[1] == 'v':
        video_names = input_parse(name="video names", function="convert")
        for video in video_names:
            convert_video_to_audio(video)
        print("All video files converted")
    # Convert by folder
    elif sys.argv[1] == 'f' and len(sys.argv) >= 3:
        input_dir = sys.argv[2]
        output_dir = input_dir if len(sys.argv) == 3 else sys.argv[3]
        convert_all_videos_to_audios(input_dir=input_dir, output_dir=output_dir)
        os.chdir(input_dir)  # For deleting video files
    else:
        print("No such function!")
        print(musicconverter_usage)
        return

    # Checks whether user wants to delete
    delete_choice = pyip.inputYesNo("Do you want to delete the video files?")
    if delete_choice == 'yes':
        delete_video_files('.')
    return


# Converts a video file to audio file
def convert_video_to_audio(video_file: str, output_ext: str = "mp3", input_dir: str = '.', output_dir: str = '.'):
    os.chdir(input_dir)
    filename, ext = os.path.splitext(video_file)
    clip = VideoFileClip(video_file)
    # Saves file to a new directory
    os.chdir(output_dir)
    audio_filename = f"{filename}.{output_ext}"
    clip.audio.write_audiofile(audio_filename)
    return audio_filename


# Converts all videos in input dir into output
def convert_all_videos_to_audios(input_dir: str = '.', output_dir: str = ''):
    # Check if output_dir is given
    if output_dir == '':
        output_dir = input_dir

    video_files = [file for file in os.listdir('.') if file.endswith('.mp4')]
    audio_filenames = []
    # Converts all video files
    for file in video_files:
        audio_file = convert_video_to_audio(file, input_dir=input_dir, output_dir=output_dir)
        audio_filenames.append(audio_file)

    print("ALl video files converted")
    return audio_filenames


# Deletes all video files in directory
def delete_video_files(dir='.'):
    video_files = [file for file in os.listdir('.') if file.endswith('.mp4')]
    for file in video_files:
        os.remove(file)
    print("All video files deleted")


# Inserts list of new audio into sqlite database
def insert_new_audio(audio_files: list[str], genre: str):
    data = [(audio_file, genre, 20) for audio_file in audio_files]
    with sqlite3.connect(database_name) as con:
        cur = con.cursor()
        cur.executemany(
            """
            INSERT INTO music
            (title, genre, score)
            VALUES (?, ?, ?)
            """, data
        )


if __name__ == "__main__":
    main()
