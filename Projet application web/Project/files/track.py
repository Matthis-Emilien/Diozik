import sqlite3 as sql


class Track:
    def __init__(self, primarykey):
        self.primarykey = primarykey
        self.music_title = self.setMusicTitle()
        self.filename = self.setFilename()
        self.author = self.setAuthor()
        self.author_PK = self.setAuthorPK()

    def setAuthor(self):
        try:
            with sql.connect("../database/database.db") as con:
                cur = con.cursor()
                track = self.primarykey
                cur.execute("SELECT account FROM Tracklist WHERE track = ?", (track,))
                account = cur.fetchall()[0][0]
                cur.execute("SELECT usernem FROM Accounts WHERE account = ?", (account,))
                author = cur.fetchall()[0][0]
                self.author = author
            return "Auteur correctement modifié."

        except:
            return "Erreur lors de l'opération de réception."

    def setAuthorPK(self):
        try:
            with sql.connect("../database/database.db") as con:
                cur = con.cursor()
                track = self.primarykey
                cur.execute("SELECT author FROM Tracklist WHERE track = ?", (track,))
                author = cur.fetchall()[0][0]
                self.author_PK = author
        except:
            return "Erreur lors de l'opération de réception."

    def setFilename(self):
        try:
            with sql.connect("../database/database.db") as con:
                cur = con.cursor()
                track = self.primarykey
                cur.execute("SELECT filename FROM Tracklist WHERE track = ?", (track,))
                filename = cur.fetchall()[0][0]
                self.filename = filename

        except:
            return "Erreur lors de l'opération de réception."

    def setMusicTitle(self):
        try:
            with sql.connect("../database/database.db") as con:
                cur = con.cursor()
                track = self.primarykey
                cur.execute("SELECT music_title FROM Tracklist WHERE track = ?", (track,))
                music_title = cur.fetchall()[0][0]
                self.music_title = music_title

        except:
            return "Erreur lors de l'opération de réception."
