import sqlite3 as sql


# ---------- Class Track ---------- #
class Track:
    def __init__(self, primarykey: int, dbpath: str = "database/database.db"):
        self.primarykey = primarykey
        self.music_title = None
        self.filename = None
        self.author = None
        self.author_PK = None
        self.dbpath = dbpath

    # ---------- Setters ---------- #
    def setAuthor(self):
        try:
            with sql.connect(self.dbpath) as con:
                cur = con.cursor()
                track = self.getPrimaryKey()
                cur.execute("SELECT author FROM Tracklist WHERE track = ?", (track,))
                account = cur.fetchall()[0][0]
                cur.execute("SELECT username FROM Accounts WHERE account = ?", (account,))
                author = cur.fetchall()[0][0]
                self.author = author
                con.commit()
        except:
            print("Erreur lors de l'opération de réception setAuthor.")
            return ""

    def setAuthorPK(self):
        try:
            with sql.connect(self.dbpath) as con:
                cur = con.cursor()
                track = self.getPrimaryKey()
                cur.execute("SELECT author FROM Tracklist WHERE track = ?", (track,))
                author = cur.fetchall()[0][0]
                self.author_PK = author
                con.commit()
        except:
            print("Erreur lors de l'opération de réception setAuthorPK.")
            return ""

    def setFilename(self):
        try:
            with sql.connect(self.dbpath) as con:
                cur = con.cursor()
                track = self.getPrimaryKey()
                cur.execute("SELECT filename FROM Tracklist WHERE track = ?", (track,))
                filename = cur.fetchall()[0][0]
                self.filename = filename
                con.commit()
        except:
            print("Erreur lors de l'opération de réception setFilename.")
            return ""

    def setMusicTitle(self):
        try:
            with sql.connect(self.dbpath) as con:
                cur = con.cursor()
                track = self.getPrimaryKey()
                cur.execute("SELECT music_title FROM Tracklist WHERE track = ?", (track,))
                music_title = cur.fetchall()[0][0]
                self.music_title = music_title
                con.commit()
        except:
            print("Erreur lors de l'opération de réception setMusicTitle.")
            return ""

    def setAll(self):
        self.setMusicTitle()
        self.setFilename()
        self.setAuthor()
        self.setAuthorPK()

    def setDBPath(self, dbpath: str):
        self.dbpath = dbpath

    # ---------- Getters ---------- #
    def getPrimaryKey(self):
        return self.primarykey

    def getAuthor(self):
        return self.author

    def getAuthorPK(self):
        return self.author_PK

    def getFilename(self):
        return self.filename

    def getMusicTitle(self):
        return self.music_title

    def getAll(self):
        dic = {"PK": self.getPrimaryKey(), "music_title": self.getMusicTitle(), "filename": self.getFilename(),
               "author": self.getAuthor(), "authorPK": self.getAuthorPK()}
        return dic
