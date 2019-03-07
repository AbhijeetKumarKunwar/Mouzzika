import Model
from pygame import mixer
from tkinter import  filedialog
import os
from mutagen.mp3 import MP3
class Player:
    def __init__(self):
        mixer.init()
        self.my_model=Model.Model()
    def get_db_status(self):
        return self.my_model.get_db_status()
    def close_player(self):
        mixer.music.stop()
        self.my_model.close_db_connection()
    def set_volume(self,volume_leval):
        mixer.music.set_volume(volume_leval)#It takes in decimal value
    def add_song(self):
        song_path=filedialog.askopenfilename(title="select your song..",filetype=[("Mp3 files",".mp3")])
        print("song path is :",song_path)
        if song_path=="":
            return
        song_name=os.path.basename(song_path)#it will take name with path and return song name or file name
        #print("song name is  ",song_name)
        self.my_model.add_song(song_name,song_path)
        return song_name
    def remove_song(self,song_name):
        self.my_model.remove_song(song_name)
    def get_song_path(self,song_name):
        self.song_path=self.my_model.get_song_path(song_name)
        self.audio_tag=MP3(self.song_path)#obj of mp3 class
        song_length=self.audio_tag.info.length#info is the obj inside the mp3 class which has length attribute
        return song_length
    def get_song_length(self,song_name):
        self.song_path=self.my_model.get_song_path(song_name)
        self.audio_tag=MP3(self.song_path)
        song_length=self.audio_tag.info.length
        return song_length
    def play_song(self):
        mixer.quit()#it stop the current song
        mixer.init(frequency=self.audio_tag.info.sample_rate)#mixer is for the wave frequency so we have to give the frequency of song
        mixer.music.load(self.song_path)
        mixer.music.play()
    def stop_song(self):
        mixer.music.stop()
    def pause_song(self):
        mixer.music.pause()
    def unpause_song(self):
        mixer.music.unpause()

    def add_song_to_favourite(self,song_name):
        song_path=self.my_model.get_song_path(song_name)
        result=self.my_model.add_song_to_favourites(song_name,song_path)
        return result

    def load_song_from_favourites(self):
        result=self.my_model.load_songs_from_favourites()
        return(result,self.my_model.song_dic) #1st value contain message and senond is the list of song which is added to the dic
    def remove_song_from_favourites(self,song_name):
        result=self.my_model.remove_song_from_favourites(song_name)
        return result




if __name__=="__main__":

    p=Player()
    print("db connection",p.get_db_status())
    p.add_song()


