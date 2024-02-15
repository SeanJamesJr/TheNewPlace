import pymysql
from flask import Flask
from flask import Flask, render_template,redirect
from flask import request 
import pymysql
import flask_login
from flask import g

app = Flask(__name__)
app.secret_key = "nugget_secret_recipe" #change this
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User:
    is_authenticated = True
    is_anonymous = False
    is_active= True
    def __init__(self,id,username):
        self.username = username
        self.id = id
    def get_id(self):
        return str(self.id)

@login_manager.user_loader
def load_user(user_id):
   cursor = get_db().cursor()
   cursor.execute(f"SELECT * FROM `Users` WHERE `id` = {user_id}")
   result = cursor.fetchone()
   cursor.close()
   get_db().commit()
   if result is None:
    return None
   return User(result["ID"], result["Username"])


def connect_db():
    return pymysql.connect(
        host="10.100.33.60",
        user="sjamesjr",
        password="250415031",
        database="sjamesjr_thenewplace",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )
def get_db():
    '''Opens a new database connection per request.'''        
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db    

@app.teardown_appcontext
def close_db(error):
    '''Closes the database connection at the end of request.'''    
    if hasattr(g, 'db'):
        g.db.close() 

@app.route('/')
def index():
  if flask_login.current_user.is_authenticated:
     return redirect('/feed')
  
  return render_template("index.html.jinja")

@app.route('/signin',methods =['GET','POST'])
def Signin():
 if request.method == 'POST':
    Username = request.form["Username"]
    Password = request.form["Password"]
    cursor =get_db().cursor()
    cursor.execute(f"SELECT * FROM `Users` WHERE `Username` = '{Username}'")   
    User = cursor.fetchone()
    {User['Password']}
    if Password == User["Password"]:
        user =load_user(User['ID'])
        flask_login.login_user(user)
        return redirect('/feed')

    
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
    cursor =get_db().cursor()
    cursor.execute(f"INSERT INTO `Users` (`Username`,`Password`,`Name`,`Pronouns`,`User_Bio`,`Birthday`,`Email`) VALUES ('{Username}','{Password}','{Name}','{User_Bio}','{Pronouns}','{Birthday}','{Email}')")
    cursor.close()
    get_db().commit()
    return redirect("/Signin")
 return render_template("signup.html.jinja")

@app.route('/feed')
@flask_login.login_required
def post_feed():
    cursor = get_db().cursor()
    cursor.execute('SELECT * from `Post` ORDER BY `Timestamp`')
    results = cursor.fetchall()
    cursor.close()
    return render_template("feed.html.jinja",post_list=results)
  

@app.route('/post', methods = ['POST'])
@flask_login.login_required
def create_post():
    Description = request.form['Description']
    UserID = flask_login.current_user.id
    cursor = get_db().cursor()
    cursor.execute(f"INSERT INTO `Post` (`Description`,`UserID`) VALUES ('{Description}','{UserID}')")
    return redirect("/feed")