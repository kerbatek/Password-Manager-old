from flask import render_template, request, redirect, url_for, Blueprint, jsonify
import sqlite3

bp = Blueprint('bp', __name__)
@bp.route('/')
def home():
    conn = sqlite3.connect('Database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, website FROM websites")
    fetc = cursor.fetchall()
    print(fetc)

    res = []
    for row in fetc:
        res.append({"id":row[0], "website":row[1]})

    conn.close()
    return render_template('index.html', websites=res)

@bp.route('/add_password', methods = ["POST"])
def insert_password():
    if request.method == "POST":
        conn = sqlite3.connect('Database.db')
        cursor = conn.cursor()
 
        cursor.execute("INSERT INTO websites(website, username, email, password) VALUES (?, ?, ?, ?)", 
                       (request.form['site_name'], request.form['username'], request.form['email'], request.form['password']))
        conn.commit()
        conn.close()
    return redirect(url_for('bp.home'))

@bp.route('/get_password', methods = ["GET"])
def get_userdata():
    if request.method == "GET":
        u_id = request.args.get("i")

        conn = sqlite3.connect('Database.db')
        cursor = conn.cursor()
 
        cursor.execute("SELECT username, email, password FROM websites where id = (?)", u_id)
        fetc = cursor.fetchone()
        res = {"username":fetc[0], "email":fetc[1], "password":fetc[2]}
        conn.close()
        return jsonify(res)



