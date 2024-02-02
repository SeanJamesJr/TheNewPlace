import pymysql
from flask import Flask
from flask import Flask, render_template
from flask import request 
import pymysql

app = Flask(__name__)
conn = pymysql.connect(
    database ='sjamesjr_thenewplace',
    user='sjamesjr',
    password='250415031',
    host='10.100.33.60',
    cursorclass=pymysql.cursors.DictCursor
)

@app.route('/')
def index():
 return render_template("index.html.jinja")

@app.route('/signin')
def Signin():
 return render_template("signin.html.jinja")


@app.route('/signup', methods=['GET', 'POST'])
def Signup():
 if request.method == 'POST':
    Username = request.form["Username"]
    Password = request.form["Password"]
    Name = request.form["Name"]
    User_Bio = request.form["User_Bio"]
    Pronouns = request.form["Pronouns"]
    Birthday = request.form["Birthday"]
    Email = request.form["Email"]
    cursor =conn.cursor()
    cursor.execute(f"INSERT INTO `Users` (`Username`,`Password`,`Name`,`Pronouns`,`User_Bio`,`Birthday`,`Email`) VALUES ('{Username}','{Password}','{Name}','{User_Bio}','{Pronouns}','{Birthday}','{Email}')")
    cursor.close()
    conn.commit()
 return render_template("signup.html.jinja")


