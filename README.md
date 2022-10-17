**Desktop Music Player** 

This music player is unique, in that unlike other music players, it 
enables the user to repeatedly play songs, without freezing the player. 
This is done using a multi-thread safe tkinter module, that enables 
the user to indicate their preferences while tkinter is open, and 
the music is playing. 

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



