**Desktop Music Player** 

This music player is unique, in that unlike other music players, it 
enables the user to repeatedly play songs, without freezing the player. 
This is done using a multi-thread safe tkinter module, that enables 
the user to indicate their preferences while tkinter is open, and 
the music is playing. 

I started work on this Music Player in Dec 2021, because I knew that 
I would be going to Germany for an attachment for 2 months, where WiFi 
was scarce. I wanted to be able to continue listening to my favourite music 
when I was overseas, therefore, I created the first iteration of this player. 

There are 4 modes to the music player: Normal, Progressive, Repeat, 
and Random. 

Normal mode plays just the song, and stops afterwards. This is what 
most music players online are capable of. 

Progressive mode plays songs in order of their appearance in the 
playlist, like an actual playlist. Some other music players are 
able to do this, but it causes their screen to freeze up. 

Repeat mode repeats the current song continuously after it ends. 

Random mode plays all the songs at random. 

User preferences are tracked in a SQLite file that gets updated 
with a simple algorithm to reflect user preferences. 

Apart from playing songs, the player is capable of automatically 
downloading songs from YouTube in order to add to 


Some of the challenges I faced: 

It was quite hard to implement the thread-safe user-preference 
changes, without the music player hanging. Therefore, I had to 
replace the use of traditional tkinter with mttkinter, that 
enables the user to indicate their preferences on the Command Line
while still not affecting the music player 

Interactivity: Adding the volume slider and duration slider 
similarly required thread-safe changes. 

Adding song functionality: I had to navigate between different 
directories and tackle all of them to ensure that the videos went to
the right places.
Also, because moviepy's resource release is not the best, I had to
create a Process to process the creating of the audio clip, before
deleting the video file. 


Enjoy! 



