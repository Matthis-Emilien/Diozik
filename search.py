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

            username_list = self.dbdic["username"]

            for i in range(len(username_list)):
                lower = username_list[i][1].lower()
                username_list[i] = (username_list[i][0], lower)

            for f in username_list:
                if f[1] == self.search_content.lower():
                    result[0].append(f)
                    username_list.remove(f)

            s = True
            while s:
                x = closestWord(self.search_content.lower(), username_list)
                if x:
                    extra[0].append(x)
                    username_list.remove(x)
                else:
                    if len(username_list) > 0:
                        del username_list[0]
                    else:
                        s = False

        if "music_title" in self.dbdic:

            music_title_list = self.dbdic["music_title"]
            for i in range(len(music_title_list)):
                lower = music_title_list[i][1].lower()
                music_title_list[i] = (music_title_list[i][0], lower)

            for f in music_title_list:
                if f[1] == self.search_content.lower():
                    result[1].append(f)
                    music_title_list.remove(f)

            s = True
            while s:
                x = closestWord(self.search_content.lower(), music_title_list)
                if x:
                    extra[1].append(x)
                    music_title_list.remove(x)
                else:
                    if len(music_title_list) > 0:
                        del music_title_list[0]
                    else:
                        s = False

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


def closestWord(x: str, L):
    L.sort()
    if len(x) > 0:
        for f in L:
            if len(f[1]) >= len(x):
                a = f[1][len(x) - 1]
                if x == a:
                    return f
            c = len(x)
            a = ""
            if c > 1:
                for i in range(c - 1):
                    a += x[i]
            x = a
            return closestWord(x, L)
    else:
        return False
