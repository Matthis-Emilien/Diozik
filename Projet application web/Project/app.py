# Fichier : app.py
# @authors : Matthis Lelièvre & Emilien Le Labourier
# Application WEB : Diozik


# ---------- IMPORTATIONS ---------- #
from flask import Flask, render_template, session, redirect, url_for, request, Response
from datetime import timedelta
from werkzeug.utils import secure_filename
from pathlib import Path
from Project.mytracks import MyTracks
from Project.search import Search
import sqlite3 as sql
import os
import random
from wtforms import Form, StringField, SelectField

# ---------- INITIALISATION DE FLASK ---------- #
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(minutes=15)

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'mp3', 'wav'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ---------- VARIABLES GLOBALES ---------- #
char = {
    'username': 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_.',
    'mail': 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.@',
}


# ---------- ROUTES DES TEMPLATES HTML/CSS ---------- #
@app.route('/')
def home():
    if "user" in session:
        with sql.connect("database/database.db") as con:
            cur = con.cursor()
            account = session["user"]
            cur.execute("SELECT username FROM Accounts WHERE account=?", (account,))
            username = cur.fetchall()[0][0]
            cur.execute("SELECT plan FROM Users_Plan WHERE account=?", (account,))
            plan = cur.fetchall()[0][0]
            cur.execute("SELECT plan_title FROM Plans WHERE plan=?", (plan,))
            plan = cur.fetchall()[0][0]
            con.commit()
        msg = "Connecté en tant que : " + username + ". C'est un compte : " + plan + "."
        log = username
        sign = "Déconnexion"
        if "search_reply" in session:
            search_reply = session['search_reply']
            iframe = url_for('search_result')
            session.pop('search_reply', None)
        else:
            iframe = url_for('app_default')
            search_reply = ""
        return render_template("app.html", msg=msg, log=log, sign=sign, iframe=iframe, search_reply=search_reply)
    else:
        return render_template("index.html")
    con.close()


@app.route('/login')
def login():
    if "user" in session:
        return redirect(url_for("home"))
    elif "loginError" in session:
        msg = session["loginError"]
        session.pop("loginError", None)

        return render_template('login.html', msg=msg)
    else:
        return render_template('login.html')


@app.route('/signup')
def signup():
    if "user" in session:
        return redirect(url_for("home"))
    elif "signupError" in session:
        msg = session["signupError"]
        session.pop("signupError", None)
        return render_template('signup.html', msg=msg)
    else:
        return render_template('signup.html')


@app.route("/shop")
def shop():
    if "user" in session:
        session.pop("shop", None)
        with sql.connect("database/database.db") as con:
            cur = con.cursor()
            account = session["user"]
            cur.execute("SELECT username FROM Accounts WHERE account=?", (account,))
            username = cur.fetchall()[0][0]
            con.commit()
        log = username
        sign = "Déconnexion"
        if "change_planError" in session:
            msg = session["change_planError"]
            session.pop("change_planError", None)
            return render_template('shop.html', msg=msg, log=log, sign=sign)
        else:
            return render_template("shop.html", log=log, sign=sign)
    else:
        session["shop"] = True
        return redirect(url_for("signup"))


@app.route("/user")
def user():
    if "user" in session:
        session.pop("profile", None)
        with sql.connect("database/database.db") as con:
            cur = con.cursor()
            account = session["user"]
            cur.execute("SELECT username FROM Accounts WHERE account=?", (account,))
            username = cur.fetchall()[0][0]
            con.commit()
        log = username
        sign = "Déconnexion"
        if "user_iframe" in session:
            iframe = url_for(session["user_iframe"])
        else:
            session["user_iframe"] = "user_edit"
            iframe = url_for(session["user_iframe"])
        return render_template("user.html", log=log, sign=sign, iframe=iframe)
    else:
        session["profile"] = True
        return redirect(url_for("signup"))


@app.route("/contact")
def contact():
    if "user" in session:
        with sql.connect("database/database.db") as con:
            cur = con.cursor()
            account = session["user"]
            cur.execute("SELECT username FROM Accounts WHERE account=?", (account,))
            username = cur.fetchall()[0][0]
            con.commit()
        log = username
        sign = "Déconnexion"
    else:
        log = "Connexion"
        sign = "S'inscrire"
    return render_template("contact.html", log=log, sign=sign)


@app.route("/about")
def about():
    if "user" in session:
        with sql.connect("database/database.db") as con:
            cur = con.cursor()
            account = session["user"]
            cur.execute("SELECT username FROM Accounts WHERE account=?", (account,))
            username = cur.fetchall()[0][0]
            con.commit()
        log = username
        sign = "Déconnexion"
    else:
        log = "Connexion"
        sign = "S'inscrire"
    return render_template("about.html", log=log, sign=sign)


@app.route("/cgu_cgv")
def cgu_cgv():
    if "user" in session:
        with sql.connect("database/database.db") as con:
            cur = con.cursor()
            account = session["user"]
            cur.execute("SELECT username FROM Accounts WHERE account=?", (account,))
            username = cur.fetchall()[0][0]
            con.commit()
        log = username
        sign = "Déconnexion"
    else:
        log = "Connexion"
        sign = "S'inscrire"
    return render_template("cgu_cgv.html", log=log, sign=sign)


# ---------- ROUTES DES PROCESSUS FLASK DE L'APPLICATION ---------- #
@app.route('/login/result', methods=['POST', 'GET'])
def login_result():
    if request.method == 'POST':
        msg = None

        try:
            find = False

            user_mail = request.form['user_mail']
            password = request.form['password']
            try:
                keeplog = request.form['keeplog']
            except:
                keeplog = "off"

            with sql.connect("database/database.db") as con:
                cur = con.cursor()

                mail = user_mail
                username = user_mail
                cur.execute("SELECT account FROM Accounts WHERE username=? OR mail=?", (username, mail))
                row = cur.fetchall()
                if len(row) > 1:
                    msg = "Erreur dans l'opération de sélection."
                elif len(row) < 1:
                    msg = "Identifiants invalides."
                else:
                    msg = "Done."
                    cur.execute("SELECT password FROM Accounts WHERE username=? OR mail=?", (username, mail))
                    identify = cur.fetchall()[0][0]
                    if password == identify:
                        find = True
                        if keeplog == "on":
                            session.permanent = True
                        else:
                            session.permanent = False
                        session["user"] = str(row[0][0])
                    else:
                        msg = "Identifiants invalides."
                con.commit()

        except:
            msg = "Erreur dans l'opération de réception."

        finally:
            if find:
                if "shop" in session:
                    if session["shop"]:
                        return redirect(url_for("shop"))
                elif "profile" in session:
                    if session["profile"]:
                        return redirect(url_for("user"))
                else:
                    return redirect(url_for("home"))
            else:
                session["loginError"] = msg
                return redirect(url_for("login"))
            con.close()


@app.route('/signup/result', methods=['POST', 'GET'])
def signup_result():
    if request.method == 'POST':
        msg = None
        try:
            username = request.form['username']
            mail = request.form['mail']
            password = request.form['password']
            password_2 = request.form['password_2']
            try:
                keeplog = request.form['keeplog']
            except:
                keeplog = "off"

            with sql.connect("database/database.db") as con:

                if password != password_2:
                    msg = "Les mots de passe ne correspondent pas."

                else:

                    if len(password) < 8 or len(password) > 100:
                        msg = "Le mot de passe doit faire entre 8 et 100 caractères."
                    else:
                        chars = []
                        valid = True
                        for k in char['mail']:
                            chars.append(k)
                        for c in mail:
                            if c not in chars:
                                valid = False

                        if not "@" in mail or not "." in mail:
                            valid = False

                        if len(mail) > 1000:
                            valid = False

                        if not valid:
                            msg = "L'adresse mail saisie est invalide."
                        else:
                            if len(username) < 4 or len(username) > 100:
                                msg = "Le nom d'utilisateur doit faire entre 4 et 100 caractères."
                            else:
                                chars = []
                                valid = True
                                for k in char['username']:
                                    chars.append(k)
                                for c in username:
                                    if c not in chars:
                                        valid = False

                                if not valid:
                                    msg = "Le nom d'utilisateur comporte des caractères interdits. Les caractères autorisés sont les caractères alphanumériques et les caractères spéciaux suivants : '.' et '_'."
                                else:
                                    cur = con.cursor()

                                    try:
                                        cur.execute("INSERT INTO Accounts (mail,password,username) VALUES(?, ?, ?)",
                                                    (mail, password, username))

                                        msg = True
                                    except:
                                        try:
                                            cur.execute("INSERT INTO Accounts (username) VALUES(?)", (username,))
                                        except:
                                            msg = "Le nom d'utilisateur est déjà utilisé."
                                        try:
                                            cur.execute("INSERT INTO Accounts (mail) VALUES(?)", (mail,))
                                        except:
                                            msg = "L'adresse mail est déjà utilisé."

                                    con.commit()
        except:
            con.rollback()
            msg = "Erreur dans l'opération d'insertion."

        finally:

            if msg == True:
                cur.execute("SELECT account FROM Accounts WHERE username=? OR mail=?", (username, mail))
                account = cur.fetchall()[0][0]

                if keeplog == "on":
                    session.permanent = True
                else:
                    session.permanent = False
                session["user"] = str(account)

                cur.execute("INSERT INTO Users_Plan VALUES(?,1)", (account,))

                con.commit()

                if "shop" in session:
                    if session["shop"]:
                        return redirect(url_for("shop"))
                elif "profile" in session:
                    if session["profile"]:
                        return redirect(url_for("user"))
                else:
                    return redirect(url_for("home"))
            else:
                session["signupError"] = msg
                return redirect(url_for("signup"))
            con.close()


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))


@app.route("/shop/change_plan", methods=['POST', 'GET'])
def change_plan():
    if request.method == "POST":
        msg = ""
        try:
            plan = request.form.get("plan")
            with sql.connect("database/database.db") as con:
                cur = con.cursor()

                account = session["user"]
                cur.execute("UPDATE Users_Plan SET plan = ? WHERE account = ?", (plan, account))

                con.commit()
            msg = "Nouvelle formule appliquée !"
        except:
            msg = "Erreur lors de l'opération d'insertion."
        finally:
            session["change_planError"] = msg
            return redirect(url_for("shop"))
        con.close()


@app.route("/headerlog")
def headerlog():
    if "user" in session:
        return redirect(url_for("user"))
    else:
        return redirect(url_for("login"))


@app.route("/headersign")
def headersign():
    if "user" in session:
        return redirect(url_for("logout"))
    else:
        return redirect(url_for("signup"))


@app.route("/user/edit")
def user_edit():
    if "user_iframe" in session:
        if session["user_iframe"] == "user_edit":
            session.pop("user_iframe", None)
            msg = ""
            if "user_edit_message" in session:
                msg = session["user_edit_message"]
                session.pop("user_edit_message", None)
            with sql.connect("database/database.db") as con:
                cur = con.cursor()
                account = session["user"]
                cur.execute("SELECT username FROM Accounts WHERE account=?", (account,))
                username = cur.fetchall()[0][0]
                cur.execute("SELECT mail FROM Accounts WHERE account=?", (account,))
                mail = cur.fetchall()[0][0]
                con.commit()
            return render_template("user_edit.html", msg=msg, username=username, mail=mail)
    else:
        session["user_iframe"] = "user_edit"
        return redirect(url_for("user"))


@app.route("/user/sub")
def user_sub():
    if "user_iframe" in session:
        if session["user_iframe"] == "user_sub":
            session.pop("user_iframe", None)
            return render_template("user_sub.html")
    else:
        session["user_iframe"] = "user_sub"
        return redirect(url_for("user"))


@app.route("/user/follow")
def user_follow():
    if "user_iframe" in session:
        if session["user_iframe"] == "user_follow":
            session.pop("user_iframe", None)
            return render_template("user_follow.html")
    else:
        session["user_iframe"] = "user_follow"
        return redirect(url_for("user"))


@app.route("/user/rating")
def user_rating():
    if "user_iframe" in session:
        if session["user_iframe"] == "user_rating":
            session.pop("user_iframe", None)
            return render_template("user_rating.html")
    else:
        session["user_iframe"] = "user_rating"
        return redirect(url_for("user"))


@app.route("/user/tracks")
def user_tracks():
    if "user_iframe" in session:
        if session["user_iframe"] == "user_tracks":
            session.pop("user_iframe", None)
            msg = ""
            if "user_tracks_message" in session:
                msg = session["user_tracks_message"]
                session.pop("user_tracks_message", None)
            return render_template("user_tracks.html", msg=msg)
    else:
        session["user_iframe"] = "user_tracks"
        return redirect(url_for("user"))


@app.route("/user/edit/save", methods=['POST', 'GET'])
def user_edit_save():
    if request.method == 'POST':
        msg = ''
        try:
            username = request.form['username']
            mail = request.form['mail']
            password = request.form['password']
            new_password = request.form['new_password']
            new_password_2 = request.form['new_password_2']

            with sql.connect("database/database.db") as con:

                chars = []
                valid = True
                for k in char['mail']:
                    chars.append(k)
                for c in mail:
                    if c not in chars:
                        valid = False

                if not "@" in mail or not "." in mail:
                    valid = False

                if len(mail) > 1000:
                    valid = False

                if not valid:
                    msg = "L'adresse mail saisie est invalide."
                else:
                    if len(username) < 4 or len(username) > 100:
                        msg = "Le nom d'utilisateur doit faire entre 4 et 100 caractères."
                    else:
                        chars = []
                        valid = True
                        for k in char['username']:
                            chars.append(k)
                        for c in username:
                            if c not in chars:
                                valid = False

                        if not valid:
                            msg = "Le nom d'utilisateur comporte des caractères interdits. Les caractères autorisés " \
                                  "sont les caractères alphanumériques et les caractères spéciaux suivants : '.' et " \
                                  "'_'. "
                        else:
                            cur = con.cursor()
                            account = session["user"]
                            cur.execute("SELECT password FROM Accounts WHERE account=?", (account,))
                            password_2 = cur.fetchall()[0][0]
                            con.commit()

                            if password == password_2:

                                if new_password == new_password_2:

                                    try:
                                        account = session["user"]
                                        cur.execute("UPDATE Accounts SET username = ? WHERE account = ?",
                                                    (username, account))
                                        cur.execute("UPDATE Accounts SET mail = ? WHERE account = ?", (mail, account))

                                        if new_password != "":
                                            cur.execute("UPDATE Accounts SET password = ? WHERE account = ?",
                                                        (new_password, account))

                                        msg = "Les informations ont bien été enregistrée !"

                                    except:
                                        try:
                                            cur.execute("UPDATE Accounts (username) VALUES(?)", (username,))
                                        except:
                                            msg = "Le nom d'utilisateur est déjà utilisé."
                                        try:
                                            cur.execute("UPDATE Accounts (mail) VALUES(?)", (mail,))
                                        except:
                                            msg = "L'adresse mail est déjà utilisé."

                                    con.commit()
                                else:
                                    msg = "Les nouveaux mot de passe ne correspondent pas."

                            else:
                                msg = "Le mot de passe n'est pas valide."

        except:
            con.rollback()
            msg = "Erreur dans l'opération d'insertion."

        finally:

            session["user_iframe"] = "user_edit"
            session["user_edit_message"] = msg
            return redirect(url_for("user_edit"))
            con.close()


@app.route("/upload_file", methods=["POST", "GET"])
def upload_file():
    if request.method == 'POST':
        msg = ''
        try:
            f = request.files['file']
            music_title = request.form['music_title']
            if f.filename != "":
                if f and allowed_file(f.filename):
                    with sql.connect("database/database.db") as con:
                        cur = con.cursor()
                        author = session['user']
                        filename = secure_filename(f.filename)
                        cur.execute("SELECT filename FROM Tracklist")
                        row = cur.fetchall()
                        allowed_filename = False
                        error = False
                        c = 0
                        while not allowed_filename:
                            file = filename.rsplit('.', 1)[1].lower()
                            filename = str(author) + str(random.randint(0, 1000000000)) + "." + file
                            filename = secure_filename(filename)
                            c += 1
                            if filename not in row:
                                allowed_filename = True
                            if c == 1000000:
                                error = True
                                allowed_filename = True
                        if not error:
                            t = len(music_title)
                            if 0 < t <= 100:
                                cur.execute("INSERT INTO Tracklist (music_title,author,filename) VALUES(?, ?, ?)",
                                            (music_title, author, filename))
                                f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                                msg = "Fichier correctement téléversé !"
                            else:
                                msg = "Le nom de votre musique doit faire entre en 0 et 100 caractères."
                        else:
                            msg = "Erreur lors de l'enregistrement du fichier"
                        con.commit()

                else:
                    msg = "Le format du fichier doit faire partie des formats suivants : mp3, wav."
            else:
                msg = "Veuillez choisir un fichier."

        except:
            con.rollback()
            msg = "Erreur dans l'opération d'insertion."

        finally:
            session["user_iframe"] = "user_tracks"
            session["user_tracks_message"] = msg
            return redirect(url_for("user_tracks"))
            con.close()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/find_tracks')
def displaytracks():
    try:
        dbpath = Path("database", "database.db")
        author = int(session['user'])
        mytracks = MyTracks(author, dbpath)
        mytracks.setTrackList()
        tracklist = mytracks.getTracklist()
        trackdic = {}
        for t in tracklist:
            pk = t.getPrimaryKey()
            trackdic[f'{pk}'] = t
        display = ""
        for t in trackdic:
            display += f'<a href="" id={t}>' + '<div>' + trackdic[t].getMusicTitle() + '</div>' + '</a>'
        return display
    except:
        return "Erreur lors de l'opération de réception."


@app.route('/app/search', methods=['POST', 'GET'])
def search():
    if request.method == "POST":
        msg = ""
        content = request.form['content']
        try:
            dbpath = Path("database", "database.db")
            result = Search(content, dbpath)
            result.setDBDic()
            result.setResult()
            session['search_result'] = result.getResult()
            msg = ""
        except:
            msg = "Erreur lors de l'opération de réception."
        finally:
            session['search_reply'] = msg
            return redirect(url_for('home'))


@app.route('/app/default')
def app_default():
    return render_template("app_default.html")


@app.route('/app/search/result')
def search_result():
    if "search_result" in session:
        get = session['search_result']
        rslt = get['result']
        extra = get['extra']
        try:
            with sql.connect("database/database.db") as con:
                cur = con.cursor()

                '''
                Meilleur résultat :
                
                Artistes : 
                
                Musiques : 
                
                '''

                result = ''''''
                lenr = len(rslt[0]) + len(rslt[1])
                lene = len(extra[0]) + len(extra[1])
                if lenr > 0:
                    result += 'Meilleurs résultats :'
                    if len(rslt[0]) > 0:
                        for i in range(len(rslt[0])):
                            result += str(rslt[0][i])
                    if len(rslt[1]) > 0:
                        for i in range(len(rslt[1])):
                            result += str(rslt[1][i])
                if lene > 0:
                    result += 'Résultat de la recherche :'
                    if len(extra[0]) > 0:
                        for i in range(len(extra[0])):
                            result += str(extra[0][i])
                    if len(extra[1]) > 0:
                        for i in range(len(extra[1])):
                            result += str(extra[1][i])
                else:
                    result += 'Aucun résultat pour votre recherche...'

                # result = rslt + extra
                con.commit()
        except:
            result = "Erreur lors de l'opération de réception."
    else:
        result = "Aucun résultat trouvé."
    return render_template("app_search_result.html", result=result)


if __name__ == '__main__':
    app.run(debug=True)
