import sqlite3 as sql


class Search:

    def __init__(self, search_content: str, dbpath: str = "database/database.db", ):
        self.search_content = search_content
        self.dbpath = dbpath
        self.dbdic = {}
        self.result = {}

    def setDBDic(self):
        try:
            with sql.connect(self.dbpath) as con:
                cur = con.cursor()
                cur.execute("SELECT account, username FROM Accounts")
                username = cur.fetchall()
                self.dbdic["username"] = username
                cur.execute("SELECT track, music_title FROM Tracklist")
                music_title = cur.fetchall()
                self.dbdic["music_title"] = music_title
                con.commit()
        except:
            print("Erreur lors de l'opération de réception setDBDic.")

    def setResult(self):
        result = [[], []]
        extra = [[], []]
        if "username" in self.dbdic:
            for f in self.dbdic["username"]:
                if f[1].lower() == self.search_content.lower():
                    result[0].append(f)
                if f[1][0].lower() == self.search_content[0].lower():
                    extra[0].append(f)

        if "music_title" in self.dbdic:
            for f in self.dbdic["music_title"]:
                if f[1].lower() == self.search_content.lower():
                    result[1].append(f)
                if f[1][0].lower() == self.search_content[0].lower():
                    extra[1].append(f)

        if not result:
            result.append("Aucun résultat trouvé.")

        extra[0].sort()
        extra[1].sort()

        for f in range(len(extra[0])):
            if extra[0][f] in result[0]:
                del extra[0][f]

        for f in range(len(extra[1])):
            if extra[1][f] in result[1]:
                del extra[1][f]

        self.result = {"result": result, "extra": extra}

    def getSearchContent(self):
        return self.search_content

    def getDBPath(self):
        return self.dbpath

    def getDBDic(self):
        return self.dbdic

    def getResult(self):
        return self.result