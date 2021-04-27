# Fichier : app.py
# @authors : Matthis Le Lièvre & Emilien Le Labourier
# Application WEB : Diozik


# ---------- IMPORTATIONS ---------- #
import os
import random
import smtplib
import datetime
import sqlite3 as sql
from datetime import timedelta
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Flask, render_template, session, redirect, url_for, request, Response
from werkzeug.utils import secure_filename

from Project.mytracks import MyTracks
from Project.track import Track
from Project.search import Search

# ---------- INITIALISATION DE FLASK ---------- #
app = Flask(__name__)
app.permanent_session_lifetime = timedelta(days=5)

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'mp3'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = "\xc7\x0c\x0b\xfe\x14\x88\xf3\xdd\x97\xc1?\xfa\xa1O\x90\xbduy#\xffw\r\xfb5"

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
        msg1 = "Bienvenue sur Diozik "
        msg2 = username
        msg3 = " !"
        log = username[0].upper() + username[1].upper()
        sign = "Déconnexion"
        if "search_reply" in session:
            search_reply = session['search_reply']
            iframe = url_for('search_result')
            session.pop('search_reply', None)
        else:
            f = open('templates/app_default.html', 'w')

            message = """
            <html lang="en">
                <head>
                    <meta charset="utf-8">
                    
                    <link rel="stylesheet" type="text/css" href="../static/css/app_default.css">
            
                    <link rel="preconnect" href="https://fonts.gstatic.com">
                    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600&display=swap" rel="stylesheet">
                    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300&display=swap" rel="stylesheet">
                    <script src="https://kit.fontawesome.com/d124f7e81a.js" crossorigin="anonymous"></script>
                </head>
                <body>
                    <h3 class="small_title">Découvrez quelques artistes :</h3>
                    <div class="suggestions"><center>
            """

            with sql.connect('database/database.db') as con:
                cur = con.cursor()
                cur.execute("SELECT account FROM Accounts")
                usernames = cur.fetchall()
                cur.execute("SELECT track FROM Tracklist")
                tracks = cur.fetchall()

                ids = []
                list_index = []

                for i in range(len(usernames)):
                    list_index.append(i)

                while len(ids) < 5:
                    c = random.randint(0, len(usernames) - 1)
                    if c in list_index:
                        list_index.remove(c)
                        ids.append(c)

                for i in range(5):
                    cur.execute("SELECT username FROM Accounts WHERE account = ?", (usernames[ids[i]][0],))
                    row = cur.fetchone()[0]
                    message += f'<a href="{url_for("profile", authorPK=usernames[ids[i]][0], )}"><div class="box artist">' + str(
                        row) + '</div></a>'

                message += '</center></div><h3 class="small_title">Découvrez quelques musiques :</h3>'

                ids = []
                list_index = []

                for i in range(len(tracks)):
                    list_index.append(i)

                while len(ids) < 5:
                    c = random.randint(0, len(tracks) - 1)
                    if c in list_index:
                        list_index.remove(c)
                        ids.append(c)

                for i in range(5):
                    t = tracks[ids[i]][0]
                    t = Track(t)
                    t.setAll()
                    message += f'''<a href="{url_for("profile", authorPK=t.getAuthorPK())}"><div class="box music"><i class="fas fa-user"></i>{t.getMusicTitle()} - {t.getAuthor()} </div></a>
                                    <iframe src="http://127.0.0.1:5000/player/{t.getPrimaryKey()}" frameborder="0" width="100%" height="95px"></iframe>
                                    '''
                message += '</body></html>'

            f.write(message)
            f.close()
            iframe = url_for('app_default')
            search_reply = ""
        return render_template("app.html", msg1=msg1, msg2=msg2, msg3=msg3, log=log, sign=sign, iframe=iframe,
                               search_reply=search_reply)
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
        log = username[0].upper() + username[1].upper()
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
            cur.execute("SELECT plan FROM Users_Plan WHERE account=?", (account,))
            plan = cur.fetchall()[0][0]
            cur.execute("SELECT plan_title FROM Plans WHERE plan=?", (plan,))
            plan = cur.fetchall()[0][0]
            con.commit()

        if plan == 'Premium':
            msg2 = 'Compte ' + plan
            msg3 = ""
            msg4 = ""
        elif plan == 'Essentiel':
            msg2 = ""
            msg3 = 'Compte ' + plan
            msg4 = ""
        elif plan == 'Student':
            msg2 = ""
            msg3 = ""
            msg4 = 'Compte ' + plan

        msg1 = username
        log = username[0].upper() + username[1].upper()
        sign = "Déconnexion"
        if "user_iframe" in session:
            iframe = url_for(session["user_iframe"])
        else:
            session["user_iframe"] = "user_edit"
            iframe = url_for(session["user_iframe"])
        if session["user_iframe"] == "user_edit":
            iframe_size = 638
        elif session["user_iframe"] == "user_tracks":
            iframe_size = 975
        else:
            iframe_size = 638
        return render_template("user.html", log=log, sign=sign, iframe=iframe, msg1=msg1, msg2=msg2, msg3=msg3,
                               msg4=msg4, iframe_size=iframe_size)
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
        log = username[0].upper() + username[1].upper()
        sign = "Déconnexion"
    else:
        log = "Connexion"
        sign = "S'inscrire"
    if "contact_msg" in session:
        msg = session["contact_msg"]
        session.pop("contact_msg", None)
    else:
        msg = ""
    return render_template("contact.html", log=log, sign=sign, msg=msg)


@app.route("/about")
def about():
    if "user" in session:
        with sql.connect("database/database.db") as con:
            cur = con.cursor()
            account = session["user"]
            cur.execute("SELECT username FROM Accounts WHERE account=?", (account,))
            username = cur.fetchall()[0][0]
            con.commit()
        log = username[0].upper() + username[1].upper()
        sign = "Déconnexion"
    else:
        log = "Connexion"
        sign = "S'inscrire"
    return render_template("about.html", log=log, sign=sign)


@app.route("/profile/<int:authorPK>")
def profile(authorPK):
    with sql.connect("database/database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT username FROM Accounts WHERE account = ?", (authorPK,))
        username = cur.fetchall()[0][0]
    return render_template("profile.html", authorPK=authorPK, username=username)


@app.route("/select")
def select():
    return render_template("select.html")


@app.route("/cgu_cgv_pdc/")
def cgu_cgv_pdc():
    if "user" in session:
        session.pop("cgu_cgv_pdc", None)
        with sql.connect("database/database.db") as con:
            cur = con.cursor()
            account = session["user"]
            cur.execute("SELECT username FROM Accounts WHERE account=?", (account,))
            username = cur.fetchall()[0][0]
            con.commit()
        log = username[0].upper() + username[1].upper()
        sign = "Déconnexion"
    else:
        session["cgu_cgv_pdc"] = True
        log = "Connexion"
        sign = "S'inscrire"
    if 'cgu' in session:
        session.pop('cgu', None)
        url = url_for('cgu')
    elif 'cgv' in session:
        session.pop('cgv', None)
        url = url_for('cgv')
    elif 'pdc' in session:
        session.pop('pdc', None)
        url = url_for('pdc')
    else:
        url = url_for('cgu')
    return render_template("cgu_cgv_pdc.html", log=log, sign=sign, url=url)


@app.route("/cgu_cgv_pdc/cgu")
def cgu():
    return render_template("cgu.html")


@app.route("/cgu_cgv_pdc/cgv")
def cgv():
    return render_template("cgv.html")


@app.route("/cgu_cgv_pdc/pdc")
def pdc():
    return render_template("pdc.html")


@app.route("/shop/buy_student")
def buy_student():
    if "user" in session:
        session.pop("shop", None)
        return render_template('buy_student.html')
    else:
        session["shop"] = True
        return redirect(url_for("signup"))


@app.route("/shop/buy_premium")
def buy_premium():
    if "user" in session:
        session.pop("shop", None)
        return render_template('buy_premium.html')
    else:
        session["shop"] = True
        return redirect(url_for("signup"))


@app.route("/login/forgot_password")
def forgot_password():
    if 'recovery' in session:
        msg = session['recovery']
        session.pop('recovery', None)
    else:
        msg = ''
    return render_template('forgot_password.html', msg=msg)


@app.route("/login/change_password")
def change_password():
    if "save_password_result" in session:
        msg = session["save_password_result"]
    else:
        msg = ""
    return render_template("change_password.html", msg=msg)


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
                elif "cgu_cgv_pdc" in session:
                    if session["cgu_cgv_pdc"]:
                        return redirect(url_for("cgu_cgv_pdc"))
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

            try:
                accept = request.form['accept']
            except:
                accept = "off"

            with sql.connect("database/database.db") as con:
                if accept != "on":
                    msg = "Veuillez accepter les conditions générales d'utilisation."
                else:

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
                                if len(username) < 4 or len(username) > 15:
                                    msg = "Le nom d'utilisateur doit faire entre 4 et 15 caractères."
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
    else:
        session["user_iframe"] = "user_edit"
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
            return redirect(url_for("user_tracks"))
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
                            if 0 < t <= 15:
                                cur.execute("INSERT INTO Tracklist (music_title,author,filename) VALUES(?, ?, ?)",
                                            (music_title, author, filename))
                                f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                                msg = "Fichier correctement téléversé !"
                            else:
                                msg = "Le nom de votre musique doit faire entre en 0 et 15 caractères."
                        else:
                            msg = "Erreur lors de l'enregistrement du fichier"
                        con.commit()

                else:
                    msg = "Votre fichier doit être au format mp3."
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


@app.route('/find_tracks/<int:authorPK>')
def displaytracks(authorPK):
    try:
        dbpath = Path("database", "database.db")
        author = authorPK
        mytracks = MyTracks(author, dbpath)
        mytracks.setTrackList()
        tracklist = mytracks.getTracklist()
        trackdic = {}
        for t in tracklist:
            pk = t.getPrimaryKey()
            trackdic[f'{pk}'] = t
        display = ""
        for t in trackdic:
            display += f'''<iframe src="http://127.0.0.1:5000/player/{trackdic[t].getPrimaryKey()}" frameborder="0" width="100%" height="95px"></iframe>'''
        if trackdic == {}:
            display = '''
            <!DOCTYPE html>
                <html lang="en">
                    <! -- HEAD -- >
                    <head>
                        <meta charset="utf-8">
                
                        <link rel="stylesheet" type="text/css" href="/static/css/profile.css">
                
                        <link rel="preconnect" href="https://fonts.gstatic.com">
                        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600&display=swap" rel="stylesheet">
                        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300&display=swap" rel="stylesheet">
                        <script src="https://kit.fontawesome.com/d124f7e81a.js" crossorigin="anonymous"></script>
                    </head>
                    <! -- HEAD -- >
                
                    <! -- BODY -- >
                    <body id="itsbody">
                
                        <h3>Aucunes musiques...</h3>
                
                    </body>
                </html>           
            
            '''
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
    f = open('templates/app_result.html', 'w')
    if "search_result" in session:
        get = session['search_result']
        rslt = get['result']
        extra = get['extra']
        try:
            with sql.connect("database/database.db") as con:
                cur = con.cursor()

                result = f'''
                <html lang="en">
                    <! -- HEAD -- >
                    <head>
                        <meta charset="utf-8">
                        
                        <link rel="stylesheet" type="text/css" href="/static/css/app_result.css">
                
                        <link rel="preconnect" href="https://fonts.gstatic.com">
                        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600&display=swap" rel="stylesheet">
                        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300&display=swap" rel="stylesheet">
                        <script src="https://kit.fontawesome.com/d124f7e81a.js" crossorigin="anonymous"></script>
                    </head>
                <body id = "itsbody">
                    
                '''
                lenr = len(rslt[0]) + len(rslt[1])
                lene = len(extra[0]) + len(extra[1])
                if lenr > 0:
                    result += f'<div class="big_title">Meilleurs résultats :</div>'
                    if len(rslt[0]) > 0:
                        result += '<h3 class="small_title">Artistes :</h3>'
                        for i in range(len(rslt[0])):
                            cur.execute("SELECT username FROM Accounts WHERE account = ?", (rslt[0][i][0],))
                            row = cur.fetchone()[0]
                            result += f'<a href="{url_for("profile", authorPK=rslt[0][i][0], )}"><div class="box artist">' + str(
                                row) + '</div></a>'
                        result += '<div class="block"></div>'
                    if len(rslt[1]) > 0:
                        result += '<h3 class="small_title">Musiques :</h3>'
                        for i in range(len(rslt[1])):
                            t = rslt[1][i][0]
                            t = Track(t)
                            t.setAll()
                            result += f'''<a href="{url_for("profile", authorPK=t.getAuthorPK())}"><div class="box music"><i class="fas fa-user"></i>{t.getMusicTitle()} - {t.getAuthor()} </div></a>
                                        <iframe src="http://127.0.0.1:5000/player/{t.getPrimaryKey()}" frameborder="0" width="100%" height="95px"></iframe>'''

                if lene > 0:
                    result += f'<div class="big_title">Résultats pertinents :</div>'
                    if len(extra[0]) > 0:
                        result += '<h3 class="small_title">Artistes :</h3>'
                        for i in range(len(extra[0])):
                            cur.execute("SELECT username FROM Accounts WHERE account = ?", (extra[0][i][0],))
                            row = cur.fetchone()[0]
                            result += f'<a href="{url_for("profile", authorPK=extra[0][i][0], )}"><div class="box artist">' + str(
                                row) + '</div></a>'
                        result += '<div class="block"></div>'
                    if len(extra[1]) > 0:
                        result += '<h3 class="small_title">Musiques :</h3>'
                        for i in range(len(extra[1])):
                            t = extra[1][i][0]
                            t = Track(t)
                            t.setAll()
                            result += f'''<a href="{url_for("profile", authorPK=t.getAuthorPK())}"><div class="box music"><i class="fas fa-user"></i>{t.getMusicTitle()} - {t.getAuthor()} </div></a>
                                        <iframe src="http://127.0.0.1:5000/player/{t.getPrimaryKey()}" frameborder="0" width="100%" height="95px"></iframe>'''
                else:
                    result += f'<h4>Aucun résultat pour votre recherche...</h4>'

                result += '</body></html>'
                con.commit()
        except:
            result = "<h4>Erreur lors de l'opération de réception.</h4>"
    else:
        result = "<h4>Aucun résultat pour votre recherche...</h4>"
    f.write(result)
    f.close()
    return render_template('app_result.html')


@app.route("/stream/<int:trackPK>")
def stream(trackPK):
    def generate(path):
        with open(path, "rb") as fmp3:
            data = fmp3.read(1024)
            while data:
                yield data
                data = fmp3.read(1024)

    t = Track(trackPK)
    t.setAll()
    filename = t.getFilename()
    file = filename.rsplit('.', 1)[1]
    path = "uploads/" + filename
    if file == "mp3":
        return Response(generate(path), mimetype="audio/mp3")
    else:
        return "Erreur lors de la lecture du media : extension non supportée."


@app.route('/select/access_cgu')
def access_cgu():
    session['cgu'] = True
    return redirect(url_for('cgu_cgv_pdc'))


@app.route('/select/access_cgv')
def access_cgv():
    session['cgv'] = True
    return redirect(url_for('cgu_cgv_pdc'))


@app.route('/select/access_pdc')
def access_pdc():
    session['pdc'] = True
    return redirect(url_for('cgu_cgv_pdc'))


@app.route('/contact/send', methods=['POST', 'GET'])
def send():
    if request.method == 'POST':
        msg = ''
        try:
            mail = request.form['mail']
            subject = request.form['subject']
            content = request.form['content']

            if len(subject) < 1 or len(subject) > 50:
                msg = "L'objet doit être compris entre 1 et 50 caractères."
            else:

                if len(content) < 1 or len(content) > 1500:
                    msg = "L'objet doit être compris entre 1 et 50 caractères."
                else:

                    subject += " - From: " + mail

                    port_number = 587

                    content2 = f'''
                    Bonjour !
                    
                    Vous avez récemment contacté l'assistance Diozik.
                    
                    Votre objet :
                    {subject}
                    Votre message :
                    {content}
                    
                    Un membre de l'équipe vous recontactera au plus vite après avoir pris connaissance de votre 
                    demande. Si vous n'êtes pas à l'origine de cette demande, veuillez nous le signalé à cette même 
                    adresse mail. Merci pour votre confiance. 
                    
                    Bien Cordialement,
                    L'Équipe de Diozik
                    diozik.assistance@gmail.com
                    
                    http://127.0.0.1:5000                    
                    '''

                    message = MIMEMultipart()

                    message['From'] = 'diozik.assistance@gmail.com'
                    message['To'] = 'diozik.assistance@gmail.com'
                    message['Subject'] = subject

                    message.attach(MIMEText(content))

                    message2 = MIMEMultipart()

                    message2['From'] = 'diozik.assistance@gmail.com'
                    message2['To'] = mail
                    message2['Subject'] = 'Demande de contact - Diozik'

                    message2.attach(MIMEText(content2))

                    mailserver = smtplib.SMTP('smtp.gmail.com', port_number)
                    mailserver.starttls()
                    mailserver.login("diozik.assistance@gmail.com", "stevejobs")

                    mailserver.sendmail("diozik.assistance@gmail.com", "diozik.assistance@gmail.com",
                                        message.as_string())
                    mailserver.sendmail("diozik.assistance@gmail.com", mail,
                                        message2.as_string())
                    mailserver.quit()

                    msg = 'Message envoyé avec succès ! Consultez vos mails.'

        except:
            msg = "Erreur lors de l'opération d'envoi."
        finally:
            session['contact_msg'] = msg
            return redirect(url_for('contact'))


@app.route("/login/forgot_password/recovery", methods=['POST', 'GET'])
def recovery():
    if request.method == 'POST':
        msg = ''

        mail = request.form['mail']

        try:
            with sql.connect("database/database.db") as con:
                cur = con.cursor()
                cur.execute("SELECT account FROM Accounts WHERE mail = ?", (mail,))
                row = cur.fetchall()
                if not row:
                    msg = "L'adresse mail renseignée ne correspond à aucun compte existant."
                else:
                    t = False

                    try:
                        with sql.connect("database/database.db") as con:
                            code = random.randint(1000000, 9999999)
                            time = datetime.datetime.now()
                            cur = con.cursor()
                            cur.execute("SELECT account FROM Accounts WHERE mail = ?", (mail,))
                            account = cur.fetchall()[0][0]
                            cur.execute("SELECT * FROM Change_Password_Security WHERE account = ?", (account,))
                            col = cur.fetchall()
                            if col:
                                cur.execute("DELETE FROM Change_Password_Security WHERE account = ?", (account,))
                            cur.execute("INSERT INTO Change_Password_Security VALUES(?, ?, ?)", (account, code, time))
                            t = True
                    except:
                        t = False

                    if t:
                        content = f'''
                    Bonjour !
                    
                    Vous avez récemment fait une demande de modification de votre mot de passse.
                    
                    Code : (Expirera dans 60 minutes)
                    {code}
                    Modifier votre mot de passe :
                    http://127.0.0.1:5000/login/change_password
                    
                    Si vous n'êtes pas à l'origine de cette demande, veuillez nous le signalé à cette même 
                    adresse mail et modifier votre mot de passe au plus vite. Merci pour votre confiance. 
                    
                    Bien Cordialement,
                    L'Équipe de Diozik
                    diozik.assistance@gmail.com
                    
                    http://127.0.0.1:5000                    
                    '''

                        port_number = 587

                        message = MIMEMultipart()

                        message['From'] = 'diozik.assistance@gmail.com'
                        message['To'] = mail
                        message['Subject'] = 'Demande de modification du mot de passe - Diozik'

                        message.attach(MIMEText(content))

                        mailserver = smtplib.SMTP('smtp.gmail.com', port_number)
                        mailserver.starttls()
                        mailserver.login("diozik.assistance@gmail.com", "stevejobs")

                        mailserver.sendmail("diozik.assistance@gmail.com", mail,
                                            message.as_string())

                        mailserver.quit()

                        msg = 'Message envoyé avec succès ! Consultez vos mails.'
                    else:
                        msg = "Erreur lors de l'opération d'insertion. Veuillez rééssayer."
        except:
            msg = "Erreur lors de l'opération d'envoi."
        finally:
            session['recovery'] = msg
            return redirect(url_for('forgot_password'))


@app.route("/login/change_password/save_password", methods=['POST', 'GET'])
def save_password():
    if request.method == "POST":
        msg = ""
        try:
            code = int(request.form['code'])
            new_password = request.form['new_password']
            new_password2 = request.form['new_password2']

            with sql.connect("database/database.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM Change_Password_Security WHERE code = ?", (code,))
                col = cur.fetchall()
                if col:
                    cur.execute("SELECT time FROM Change_Password_Security WHERE code = ?", (code,))
                    code_time = cur.fetchall()[0][0]
                else:
                    msg = "Code expiré."
                    code_time = False
            con.close()
            if code_time:
                i = 0
                year = ""
                month = ""
                day = ""
                hour = ""
                minute = ""
                second = ""
                microsecond = ""
                for c in str(code_time):
                    if i < 4:
                        year += c
                    elif 4 < i < 7:
                        month += c
                    elif 7 < i < 10:
                        day += c
                    elif 10 < i < 13:
                        hour += c
                    elif 13 < i < 16:
                        minute += c
                    elif 16 < i < 19:
                        second += c
                    elif 19 < i:
                        microsecond += c
                    i += 1

                code_time = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second),
                                              int(microsecond), None)
                delta = datetime.timedelta(minutes=60)
                time = datetime.datetime.now()
                if code_time + delta > time:
                    if new_password == new_password2:
                        with sql.connect("database/database.db") as con:
                            cur = con.cursor()
                            cur.execute("SELECT account FROM Change_Password_Security WHERE code = ?", (code,))
                            account = cur.fetchall()[0][0]
                            cur.execute("SELECT password FROM Accounts WHERE account = ?", (account,))
                            password = cur.fetchall()[0][0]
                            if password != new_password:
                                cur.execute("UPDATE Accounts SET password = ? WHERE account = ?",
                                            (new_password, account))
                                cur.execute("DELETE FROM Change_Password_Security WHERE code = ?", (code,))
                                msg = "Modification du mot de passe réalisée avec succès !"
                            else:
                                msg = "Le nouveau mot de passe doit être différent du précédent."
                    else:
                        msg = "Les mots de passe ne correspondent pas."
                else:
                    msg = "Code expiré."
        except:
            msg = "Erreur lors de l'opération de modification."
        finally:
            session['save_password_result'] = msg
            return redirect(url_for('change_password'))


@app.route("/player/<int:PK>")
def player(PK: int):
    t = Track(PK)
    t.setAll()
    f = open('templates/player.html', 'w')
    message = f'''
                <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                    
                        <link rel="stylesheet" type="text/css" href="../static/css/player.css">
                    
                        <link rel="preconnect" href="https://fonts.gstatic.com">
                        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600&display=swap" rel="stylesheet">
                        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300&display=swap" rel="stylesheet">
                        <script src="https://kit.fontawesome.com/d124f7e81a.js" crossorigin="anonymous"></script>
                    
                        <title>Diozik</title>
                    </head>
                    <body>
                        <div class="music-container" id="music-container">
                            <div class="music-info">
                                <h4 id="title"></h4>
                            </div>
                    
                            <audio src="http://127.0.0.1:5000/stream/{PK}" id="audio"></audio>
                            <div class="navigation">
                                <button id="play" class="action-btn action-btn-big">
                                    <i class="fas fa-play"></i>
                                </button>
                                <button id="volume" class="action-btn">
                                    <i class="fas fa-volume-up"></i>
                                </button>
                                <input type="range" min="0" max="100" value="50" id="volume-controller">
                            </div>
                            <div class="progress-container" id="progress-container">
                                    <div class="progress" id="progress"></div>
                            </div>
                            <div class="timecode">
                                <h4 id="current-time">0:00</h4>

                            </div>
                    
                            <script src="../static/js/app.js" type="text/javascript"></script>
                            <script>
                                loadSong("{t.getMusicTitle()}", "http://127.0.0.1:5000/stream/{PK}");
                            </script>
                        </div>
                    </body>
                </html>
                '''
    f.write(message)
    f.close()
    return render_template("player.html")


if __name__ == '__main__':
    app.run(debug=True)
