import sqlite3 as sql
import random
from track import Track

sortmods = ["alphabetic", "non-alphabetic", "random"]


# ---------- Class MyTracks ---------- #
class MyTracks:
    def __init__(self, authorPK: int, dbpath: str = "database/database.db", sortmod: str = "alphabetic"):
        self.authorPK = authorPK
        self.author = None
        self.dbpath = dbpath
        self.track_list = []
        if sortmod in sortmods:
            self.sortmod = sortmod
        else:
            self.sortmod = "alphabetic"

    # ---------- Setters ---------- #
    def setAuthor(self):
        try:
            with sql.connect(self.dbpath) as con:
                cur = con.cursor()
                account = self.authorPK
                cur.execute("SELECT username FROM Accounts WHERE account = ?", (account,))
                author = cur.fetchall()[0][0]
                self.author = author
                con.commit()
        except:
            print("Erreur lors de l'opération de réception setAuthor.")

    def setTrackList(self):
        try:
            with sql.connect(self.dbpath) as con:
                cur = con.cursor()
                author = self.authorPK
                cur.execute("SELECT * FROM Tracklist WHERE author = ?", (author,))
                row = cur.fetchall()

                for f in row:
                    f = Track(f[0], self.dbpath)
                    f.setAll()
                    self.track_list.append(f)

                #self.sortTracklist()

        except:
            print("Erreur lors de l'oppération de réception setTracklist.")

    def setDBPath(self, dbpath: str):
        self.dbpath = dbpath

    def setSortMod(self, sortmod: str):
        if sortmod in sortmods:
            self.sortmod = sortmod
        else:
            self.sortmod = "alphabetic"

    # ---------- Getters ---------- #
    def getAuthorPK(self):
        return self.authorPK

    def getAuthor(self):
        return self.author

    def getTracklist(self):
        return self.track_list

    # ---------- Methods ---------- #
    def sortTracklist(self):
        if self.sortmod == "alphabetic":
            self.track_list.sort()
        elif self.sortmod == "non-alphabetical":
            self.track_list.sort(reverse=True)
        elif self.track_list == "random":
            random.shuffle(self.track_list)
        else:
            print("Erreur lors du tri.")
