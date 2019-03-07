from cx_Oracle import *
class Model:
    def __init__(self):
        self.song_dic={}#instance veriable
        self.db_status=True
        self.conn=None
        self.cur=None
        try:
            self.conn=connect("mouzikka/music@ABC/xe")
            print("Connect sucessfully to the DB")
            self.cur=self.conn.cursor()
        except DatabaseError as e:
            print(e)
            self.db_status=False
            print(self.db_status)

    def get_db_status(self):
        return self.db_status
    def close_db_connection(self):
        if self.cur is not None:
            self.cur.close()
            print("Disconnect successfully")

    def add_song(self,song_name,song_path):
        self.song_dic[song_name]=song_path
        #print("song path :",self.song_dic[song_name])
    def get_song_path(self,song_name):
        return self.song_dic[song_name]
    def remove_song(self,song_name):
        self.song_dic.pop(song_name)
        #print(self.song_dic)
    def search_song_in_favorites(self,song_name):
        self.cur.execute("select song_name from myfavourites where song_name=:1",(song_name,))
        #we give the values in tuple
        song_tuple=self.cur.fetchone()
        if song_tuple is None:
            return  False
        else:
            return  True


    def add_song_to_favourites(self,song_name,song_path):
        is_song_present=self.search_song_in_favorites(song_name)
        try:
            if is_song_present:
                return "song alredy present in your fevourites"
            self.cur.execute("select max(song_id) from myfavourites")  # it will retrun None if table is empty
            last_song_id = self.cur.fetchone()[0]
                # it will retun None if data is not thre in tablwe itherwise t will t=return tuple
            next_song_id = 1
            if last_song_id is not None:
                next_song_id = last_song_id + 1
            self.cur.execute("insert into myfavourites values(:1,:2,:3)", (next_song_id, song_name, song_path))
            self.conn.commit()
            return "song added to your favourites"
        except DatabaseError as e1:
            print(e1)



    def load_songs_from_favourites(self):
        self.cur.execute("select song_name,song_path from myfavourites")
        songs_present=False
        for song_name,song_path in self.cur:
            self.song_dic[song_name]=song_path
            #if songs are already there in dic so it will over ride not repeated in the dic and we will print all to  playlist listbox
            songs_present=True
        if songs_present==True:
            return "List populated from favourites"
        else:
            return "No song in the favourites"

    def remove_song_from_favourites(self,song_name):
        self.cur.execute("delete  myfavourites where song_name=:1",(song_name,))
        count=self.cur.rowcount
        self.conn.commit()
        if(count==0):
            return "Song is not present in the favourites"
        self.song_dic.pop(song_name)
        return "Song is deleted from the fevourites...!"








