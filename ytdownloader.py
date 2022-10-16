from pytube import YouTube
from pytube.exceptions import RegexMatchError
import sys
from settings import ytdownloader_usage


# The main function in ytdownloader that gets user input and downloads all videos
def get_all_videos():
    if len(sys.argv) < 2:
        print(ytdownloader_usage)
        sys.exit()
    elif sys.argv[1].lower() == 'a' and len(sys.argv) == 2:
        video_links = links_parse()
    elif sys.argv[1].lower() == 't' and len(sys.argv) == 3:
        video_links = text_parse()
    else:
        print("No such function!")
        print(ytdownloader_usage)
        sys.exit()
    download_all_videos(video_links)


# Parses through the text document to find all links to download
def text_parse() -> list[str]:
    print("Opening the text document to extract links...")
    try:
        with open(sys.argv[2], 'r') as f:
            contents = f.read()
            print(contents)
            links = contents.split()
            print("Added all links")
            return links
    except FileNotFoundError:
        print("Can't open document!")


# Gets all links to be downloaded
def links_parse():
    links_string = input("Copy the links you want to download, separated by a space \n")
    links = links_string.split()
    print("Added all links")
    return links


# Downloads all videos with their urls
def download_all_videos(urls: list[str], outpath: str="./"):
    for url in urls:
        download_video(url, outpath)
    print("All videos downloaded")


# Downloads a video with the url
def download_video(url: str, outpath: str="./"):
    yt = YouTube(url)
    try:
        yt.streams.filter(file_extension="mp4").get_by_resolution("240p").download(outpath)
    except RegexMatchError:
        print(f"{url} video not found!")
        return
    print(f"{url} downloaded")


if __name__ == "__main__":
    get_all_videos()
