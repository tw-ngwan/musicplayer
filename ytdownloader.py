# from lxml import html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re, time, sys, webbrowser
from bs4 import BeautifulSoup

usage = """
Usage: 
There will be two possible functionalities for this code. The first is that you key in a few links under input, and the downloader downloads
them all. The second is that you key in a text document, it parses the document for links, and downloads every link in the text document. 
Key in "py ytdownloader.py a for links, py ytdownloader.py t <.txt> for text"
"""


def main():
    if len(sys.argv) < 2:
        print(usage)
    elif sys.argv[1].lower() == 'a' and len(sys.argv) == 2:
        links_parse()
    elif sys.argv[1].lower() == 't' and len(sys.argv) == 3:
        text_parse()
    else:
        print("No such function!")
        print(usage)
        sys.exit()


def text_parse():
    print("Opening the text document to extract links...")
    try:
        with open(sys.argv[2], 'r') as f:
            contents = f.read()
            print(contents)
            links = contents.split('\n')
            print("Added all links")
            download_videos(links)
    except:
        print("Can't open document!")


def links_parse():
    links_string = input("Copy the links you want to download, separated by a space \n")
    links = links_string.split()
    print("Added all links")
    print(links)
    download_videos(links)


PATH = 'C:\\Users\Tengwei\Desktop\PythonStuff\chromedriver.exe'


def download_videos(links):
    linkRegex = re.compile(r"(https://www\.)(.*)")
    print("Compiling links...")
    for link in links:
        while True:
            link_parts = linkRegex.findall(link)
            print("Obtaining download link...")
            download_link = link_parts[0][0] + 'ss' + link_parts[0][1]
            print(download_link)
            driver = webdriver.Chrome(PATH)
            driver.get(download_link)
            try:
                elem = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="sf_result"]/div/div[1]/div[2]/div[2]/div[1]/a'))
                )
                break
            except:
                print("Trying again 1...")

        time.sleep(1)
        soup_file = driver.page_source
        soup = BeautifulSoup(soup_file, features='lxml')
        video_downloader = soup.find('a', {"data-type": "mp4"})
        new_driver = webdriver.Chrome(PATH)
        new_driver.get(str(video_downloader.get('href')))
        # webbrowser.open(str(video_downloader.get('href'))) # Try and replace this with some webdriver. It's too damn slow in webbrowser

        print("Video downloading...")

    input("Press any key to conclude the downloads \n")
    # driver.close()
    print("All videos downloaded.")


if __name__ == "__main__":
    main()

# You may want to use BeautifulSoup to extract the href link from the Download button, instead of clicking it
# This ensures that you won't be redirected to another page for other stupid reasons.
# So this means extracting the href link, then opening it with selenium.webdriver again?
