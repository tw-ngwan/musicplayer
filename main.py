import os
import pyinputplus as pyip
import shutil
import time
import threading
from mttkinter import mtTkinter as tk
import random
import pygame

import ytdownloader
import musicconverter
import musictracker

# A lot of old code from the old musicplayer that I never bothered erasing

"""Basically, this is supposed to be like a mini spotify. It's supposed to shuffle audio files in a folder, 
then play them to me in a random order. After one is over, the next one should play. Though I fail to see how I can do 
that."""

"""This will probably be the most complicated one, because there needs to be a way to seamslessly add songs, and that 
may be difficult. And of course sort the songs. That presents its own challenges: I need to use some algorithm 
to rate my songs for myself. For example: Every listen is +1, and the higher the rating, the higher the chance of 
appearing first? And you also need a function where you can choose the song order."""


def main():
    open_threading_music_player()


# This will be used to determine whether music is on autoplay, repeat, random, or none (0).
autoplay_music = 0
"""If autoplay_music == 0, normal. If autoplay_music == 1, autoplays based on index. 
If autoplay_music == 2, repeats the current song consistently. If autoplay_music == 3, autoplays at random."""

# This will be used to start the thread
started_player = False

# This will be used to check if loop should be entered
loop_enter = True


# The function used to create a music player that can autoplay, using threading to
# let user change whether he wants to autoplay or not (and thus whether it hangs)
def open_threading_music_player():
    threads = []
    functions = [open_music_player, change_autoplay_bool]
    for function in functions:
        thread = threading.Thread(target=function)
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


# Returns music genres
def get_music_genres():
    music_genres = []
    directory = 'C:/Users/Tengwei/Desktop/Music'
    for file in os.listdir(directory):
        if os.path.isdir(f'{directory}/{file}'):
            music_genres.append(file)
    return music_genres


# Returns instruction string
def get_instructions(music_genres, basic_instructions):
    if basic_instructions == "welcome":
        instructions = [
            "Welcome to the music player! Select your preferred genre today by keying in the appropriate number:\n"]
    elif basic_instructions == "add songs":
        instructions = ["Which folder would you like to add your downloaded songs to:\n"]
    else:
        instructions = [basic_instructions]

    for i, genre in enumerate(music_genres):
        instructions.append(f"{i + 1}. {genre}\n")

    if basic_instructions == "welcome":
        instructions.append(f"{len(music_genres) + 1}. Mix\n")
        instructions.append(f"{len(music_genres) + 2}. Add Song \n")

    return ''.join(instructions)


# Actual function creating the music player
def open_music_player():
    root = tk.Tk()
    musicMenu = MusicMenu(root)
    root.mainloop()
    return musicMenu


# Used to change whether music is autoplaying (and thus, whether musicplayer hangs)
def change_autoplay_bool():
    global autoplay_music
    global started_player
    global loop_enter
    while loop_enter:
        while started_player:
            entry = input("Press enter to change the state of the music! Type anything to end the loop")
            loop_enter = False
            if entry != '':
                print("Exiting music player...")
                break
            autoplay_music = (autoplay_music + 1) % 4
            print(autoplay_music)
        else:
            time.sleep(1)


# Function that moves downloaded audio files to appropriate folder to add songs
def move_music_files(folder_name):
    backdated_time = time.time() - 3600
    os.chdir('C:/Users/Tengwei/Downloads')
    for file in os.listdir('.'):
        if file.endswith('.mp3') and os.path.getctime(file) >= backdated_time:
            print(file)
            shutil.move(f"C:/Users/Tengwei/Downloads/{file}", f"C:/Users/Tengwei/Desktop/Music/{folder_name}/{file}")


class MusicMenu:

    def __init__(self, root):
        self.root = root
        # Title of the window
        self.root.title("Selection Panel")
        # Window Geometry
        self.root.geometry("1000x200+200+200")

        # Creating frame for label
        frame = tk.LabelFrame(self.root, text="Select your preferred genre", font=("arial", 15, "bold"),
                              bg="Navyblue", fg="white", bd=5, relief=tk.GROOVE)
        frame.place(x=0, y=0, width=500, height=100)

        # Creating frame for select button
        buttonframe = tk.LabelFrame(self.root, text="Control Panel", font=("arial", 15, "bold"), bg="grey",
                                    fg="white", bd=5, relief=tk.GROOVE)
        buttonframe.place(x=0, y=100, width=500, height=100)

        # Creating select button
        selectbtn = tk.Button(buttonframe, text="Select", command=self.select_genre,
                              width=10, height=1, font=("arial", 16, "bold"),
                              fg="navyblue", bg="#90ee90").grid(row=0, column=0, padx=10, pady=5)

        # Creating Genres Frame
        genresframe = tk.LabelFrame(self.root, text="Song Genres", font=("arial", 15, "bold"), bg="gold",
                                    fg="white", bd=5, relief=tk.GROOVE)
        genresframe.place(x=500, y=0, width=500, height=200)
        # Inserting scrollbar
        scrollbar_y = tk.Scrollbar(genresframe, orient=tk.VERTICAL)
        # Inserting Playlist listbox
        self.genreslist = tk.Listbox(genresframe, yscrollcommand=scrollbar_y.set, selectbackground="gold",
                                     selectmode=tk.SINGLE,
                                     font=("arial", 12, "bold"), bg="silver", fg="navyblue", bd=5, relief=tk.GROOVE)

        # Applying Scrollbar to listbox
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_y.config(command=self.genreslist.yview)
        self.genreslist.pack(fill=tk.BOTH)

        os.chdir(f"C:/Users/Tengwei/Desktop/Music")

        genres_list = [genre for genre in os.listdir() if os.path.isdir(genre)]
        for genre in genres_list:
            self.genreslist.insert(tk.END, genre)

        # Inserting all option
        self.genreslist.insert(tk.END, "All")

        # Inserting add song option
        self.genreslist.insert(tk.END, "Add Song")

    def return_genre(self):
        current_genre = self.genreslist.get(self.genreslist.curselection()[0])
        self.root.destroy()
        return current_genre

    def select_genre(self):
        global started_player
        global loop_enter
        current_genre = self.return_genre()
        if current_genre == "Add Song":
            music_genres = get_music_genres()
            ytdownloader.links_parse()
            musicconverter.convert_files_with_time(86400)
            add_to_folder_instructions = get_instructions(music_genres, 'add songs')
            numbered_choice_folder = pyip.inputInt(add_to_folder_instructions, min=1, max=len(music_genres)) - 1
            user_choice_folder = music_genres[numbered_choice_folder]
            move_music_files(user_choice_folder)
            musictracker.update_music_list()
            print("All files added!")
            loop_enter = False
        else:
            started_player = True
            new_root = tk.Tk()
            # print(current_genre)
            musicPlayer = MusicPlayer(new_root, current_genre)
            new_root.mainloop()


class MusicPlayer:

    def __init__(self, root, user_choice):
        self.root = root
        self.user_choice = user_choice
        # Whether music is paused
        self.paused = True
        # Title of the window
        self.root.title("MusicPlayer")
        # Window Geometry
        self.root.geometry("1000x250+200+200")
        # Initiating pygame and the music mixer
        pygame.init()
        pygame.mixer.init()
        # Declaring track var, status var
        self.track = tk.StringVar()
        self.status = tk.StringVar()

        # Creating track frames for song label and status label
        trackframe = tk.LabelFrame(self.root, text="Song Track", font=("arial", 15, "bold"), bg="Navyblue",
                                   fg="white", bd=5, relief=tk.GROOVE)
        trackframe.place(x=0, y=0, width=600, height=100)
        # Inserting the songtrack label
        songtrack = tk.Label(trackframe, textvariable=self.track, width=20, font=("arial", 24, "bold"),
                             bg="Orange", fg="Gold").grid(row=0, column=0, padx=10, pady=5)
        # Inserting Status Label
        trackstatus = tk.Label(trackframe, textvariable=self.status, font=("arial", 24, "bold"),
                               bg="Orange", fg="Gold").grid(row=0, column=1, padx=10, pady=5)

        # Creating button frame
        buttonframe = tk.LabelFrame(self.root, text="Control Panel", font=("arial", 15, "bold"), bg="grey",
                                    fg="white", bd=5, relief=tk.GROOVE)
        buttonframe.place(x=0, y=100, width=600, height=100)
        # Inserting Play Button
        playbtn = tk.Button(buttonframe, text="Play", command=lambda: self.playsong(self.playlist.curselection()[0]),
                            width=8, height=1,
                            font=("arial", 16, "bold"), fg="navyblue", bg="#90ee90").grid(row=0, column=0, padx=10,
                                                                                          pady=5)
        # Inserting Pause Button
        pausebtn = tk.Button(buttonframe, text="Pause", command=self.pausesong, width=8, height=1,
                             font=("arial", 16, "bold"), fg="navyblue", bg="orange").grid(row=0, column=1, padx=10,
                                                                                          pady=5)
        # Inserting Return Button
        returnbtn = tk.Button(buttonframe, text="Return", command=self.return_to_menu, width=8, height=1,
                              font=("arial", 16, "bold"), fg="navyblue", bg="red").grid(row=0, column=3, padx=10,
                                                                                        pady=5)

        # Creating Playlist Frame
        songsframe = tk.LabelFrame(self.root, text="Song Playlist", font=("arial", 15, "bold"), bg="gold",
                                   fg="white", bd=5, relief=tk.GROOVE)
        songsframe.place(x=600, y=0, width=400, height=300)
        # Inserting scrollbar
        scrollbar_y = tk.Scrollbar(songsframe, orient=tk.VERTICAL)
        # Inserting Playlist listbox
        self.playlist = tk.Listbox(songsframe, yscrollcommand=scrollbar_y.set, selectbackground="gold",
                                   selectmode=tk.SINGLE,
                                   font=("arial", 12, "bold"), bg="silver", fg="navyblue", bd=5, relief=tk.GROOVE)

        # Applying Scrollbar to listbox
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_y.config(command=self.playlist.yview)
        self.playlist.pack(fill=tk.BOTH)

        # Creating volume slider
        self.slider = tk.Scale(self.root, from_=0, to=100, orient='horizontal')
        self.slider.set(100)
        self.slider.place(x=0, y=200, width=300, height=50)
        self.slidertitle = tk.Label(self.root, text="Volume", font=("arial", 10, "bold"), bg="white",
                                    fg="black")
        self.slidertitle.place(x=100, y=200)

        # # Creating video slider (to be created when playsong called instead)
        # self._calibrate_videoslider()

        # Changing Directory for fetching Songs. Two options, either all songs, or selected
        if user_choice.lower() == 'all':
            os.chdir(f"C:/Users/Tengwei/Desktop/Music")
            songtracks_list = []
            for roots, dirs, files in os.walk('.'):
                songtracks_list.append([roots, files])
            for songtracks in songtracks_list:
                for track in songtracks[1]:
                    self.playlist.insert(tk.END, f"{songtracks[0]}/{track}")

        else:
            os.chdir(f"C:/Users/Tengwei/Desktop/Music/{user_choice}")
            songtracks = os.listdir()
            sorted_songtracks = sorted(songtracks, key=musictracker.get_music_score, reverse=True)  # This doesn't work
            print(sorted_songtracks)
            for track in sorted_songtracks:
                self.playlist.insert(tk.END, track)

        self.playlist.after(200, self._setvolume)
        # # Checking which mode the musicplayer should be in
        # if autoplay_music == 1:
        #     self.playsong(self.playlist.get(0))
        # elif autoplay_music == 2:
        #     if self.paused:
        #         self.playsong(self.playlist.curselection()[0])
        # elif autoplay_music == 3:
        #     pass

    def playsong(self, song_index):
        # Checking if the song is paused or not first
        if self.status.get() == "-Paused":
            self.status.set("-Playing")
            self.paused = False
            pygame.mixer.music.unpause()
            return None

        song = self.playlist.get(song_index)
        print("Starting play_song")
        # Displaying Selected Song Title
        self.track.set(song)
        # Displaying Status
        self.status.set("-Playing")
        # Changing pause status
        self.paused = False
        # Selects relevant element of playlist, and shows that it is selected
        self.playlist.selection_clear(0, tk.END)
        self.playlist.selection_set(song_index)
        self.playlist.activate(song_index)
        # Loading Selected Song
        pygame.mixer.music.load(song)
        # Playing Selected Song
        pygame.mixer.music.play(start=0)
        # Adding 1 point to song
        musictracker.change_music_score(song, 1)

        song_length = int(pygame.mixer.Sound(song).get_length() * 1000)
        self._calibrate_videoslider(song_length=song_length // 1000)
        print(autoplay_music)

        def autoplay(songindex):
            if not self.check_if_finished():
                self.playlist.after(1000, lambda: autoplay(songindex))
            else:
                musictracker.change_music_score(song, 3)
                songindex += 1
                try:
                    self.playsong(songindex)
                except:
                    self.playsong(0)

        def repeat():
            if not self.check_if_finished():
                self.playlist.after(1000, repeat)
            else:
                musictracker.change_music_score(song, 1)
                self.playsong(song_index)

        def random_autoplay():
            if not self.check_if_finished():
                self.playlist.after(1000, random_autoplay)
            else:
                musictracker.change_music_score(song, 3)
                songindex = random.randint(0, self.playlist.size() - 1)
                self.playsong(songindex)

        def normal():
            if not self.check_if_finished():
                self.playlist.after(1000, normal)
            else:
                musictracker.change_music_score(song, 3)

        possible_functions = [normal, lambda: autoplay(song_index), repeat, random_autoplay]

        self.playlist.after(1000, possible_functions[autoplay_music])

    def pausesong(self):
        # Displaying Status
        self.status.set("-Paused")
        # Changing Pause status
        self.paused = True
        # Paused Song
        pygame.mixer.music.pause()

    def return_to_menu(self):
        global started_player
        global loop_enter
        started_player = False
        loop_enter = True
        self.close_player()
        new_root = tk.Tk()
        musicMenu = MusicMenu(new_root)
        new_root.mainloop()

    def close_player(self):
        pygame.mixer.music.stop()
        self.root.destroy()

    def check_if_finished(self):
        # Check if the music is playing
        if self.paused or pygame.mixer.music.get_busy():
            return False
        else:
            return True

    def _setvolume(self):
        volume = self.slider.get() / 100
        pygame.mixer.music.set_volume(volume)
        self.playlist.after(200, self._setvolume)

    # Add code to automatically make videoslider move
    def _calibrate_videoslider(self, song_length=100):
        self.videoslider = tk.Scale(self.root, from_=0, to=song_length, orient='horizontal', command=self._on_scale)
        self.videoslider.set(0)
        self.videoslider.place(x=300, y=200, width=300, height=50)
        self.videoslider_label = tk.Label(self.root, text="")
        self.videoslider_label.place(x=300, y=200)
        self.videoslider_scrubberlabel = tk.Label(self.root, text="Scrubber", font=("arial", 10, "bold"),
                                                  bg="white", fg="black")
        self.videoslider_scrubberlabel.place(x=400, y=200)
        self.playlist.after(1000, lambda: self._setvideoslider(1))

    def _setvideoslider(self, seconds):
        if not self.paused:
            original_seconds = self.videoslider.get()
            if original_seconds > seconds + 2 or original_seconds < seconds - 2:  # Only change if more than 2 sec away
                seconds = original_seconds
                pygame.mixer.music.play(start=original_seconds)

            self.videoslider.set(seconds)
            seconds += 1
        self.playlist.after(1000, lambda: self._setvideoslider(seconds))

    def _on_scale(self, value):
        value = int(value)
        hours = value // 3600
        minutes = (value - hours * 3600) // 60
        seconds = value - hours * 3600 - minutes * 60
        if hours > 0:
            self.videoslider_label.configure(text="%02d:%02d:%02d" % (hours, minutes, seconds))
        else:
            self.videoslider_label.configure(text="%02d:%02d" % (minutes, seconds))


if __name__ == "__main__":
    main()
