# Laptop Service
import flask
from flask import Flask,request,render_template,make_response,jsonify,url_for,redirect
from flask_restful import Resource, Api
from pymongo import MongoClient
import pymongo
from flask_login import LoginManager,login_user,logout_user, login_required
from wtforms import Form, BooleanField,StringField,validators,PasswordField
from wtforms.validators import InputRequired, Length
from flask_wtf import FlaskForm
from urllib.parse import urlparse,urljoin
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer \
                                  as Serializer, BadSignature, \
                                  SignatureExpired)
# Instantiate the app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'UOCIS322'
app.config["LENGTH"] = 0
api = Api(app)

client = MongoClient("db", 27017)
db = client.tododb
# databse for the users
users = client.usersdb
# users.usersdb.delete_many({})
#global value for the user_id
#set login configuration
collection = db.control

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class user():
    def __init__(self, user_id):
        self.user_id = user_id
    #whithout this it will ge error
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return self.user_id
class RegisterForm(FlaskForm):
    username = StringField("username", validators = [InputRequired("Username is Required"),Length(min = 4, max = 20)])
    password = PasswordField("password", validators = [InputRequired("Password is Required")])
class LoginForm(FlaskForm):
    username =  StringField("username", validators = [InputRequired("Username is Required"),Length(min = 4, max = 20)])
    password = PasswordField("password", validators = [InputRequired("Password is Required")])
    remember = BooleanField("Remember Me")

@login_manager.user_loader
def load_user(user_id, _token = None):
    #find the user in the database
    usr = users.usersdb.find_one({"location": int(user_id)})
    if user == None:
        return None
    #if user equal None then return None
    #otherwise return the _id in the database
    return user(usr['location'])
##########################################################
#project8:
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods = ['GET', 'POST'])
def login():
    login_form = LoginForm()
    username = login_form.username.data
    password = login_form.password.data
    remember = login_form.remember.data

    if request.method == 'POST' and login_form.validate_on_submit():
        #try to find the username in the database
        user_in_db = users.usersdb.find_one({"username": username})
        if user_in_db == None: #which means the user not found in the database
            return "<h1> User not Found</h1>"
        else:
            hash_password = user_in_db["password"]
            if verify_password(password, hash_password):
                user_id = str(user_in_db['location'])
                user_obj = user(user_id)
                login_user(user_obj,remember = remember)
                token = generate_auth_token(user_in_db['location'], expiration = 300)
                return flask.jsonify({"token":token.decode(), "duration": 300}), 200
            else:
                return "<h1>Wrong Password</h1>"

    return render_template("login.html", form = login_form)

@app.route("/register", methods = ['GET', 'POST'])
def register_user():
    form = RegisterForm()
    username = form.username.data
    password = form.password.data
    item = users.usersdb.find_one({"username": username})
    if username is None or password is None:
        return render_template("register.html", form = form)
    elif item is not None:
        return "User Exists", 400
    else:
        password = hash_password(str(password))
        passwor = None
        app.config["LENGTH"] += 1
        _id = app.config["LENGTH"]
        new_user = { 'location' : _id, 'username' : username, 'password' : password}
        users.usersdb.insert_one(new_user)
        return redirect(url_for(login_manager.login_view))
#logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return "<h1>User logged out</h1>"


#list all open and close times
def hash_password(password):
    return pwd_context.encrypt(password)

def verify_password(password, hashVal):
    return pwd_context.verify(password, hashVal)

def generate_auth_token(_id, expiration = 600):
    s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
    #pass the index of users
    return s.dumps({'id':_id})

def verify_auth_token(token):
    s = Serializer(app.config['SECRET_KEY'])

    try:
        data = s.loads(token)
    except SignatureExpired:
        return None    # valid token, but expired
    except BadSignature:
        return None    # invalid token
    return True



class listAll(Resource):
    def get(self):
        top = request.args.get("top")
        if top == None:
            top = 20


        _items = db.tododb.find()
        #sort in multiple results,default it as ascending
        sort_items = _items.sort('open_time')
        #make it to limit k top
        k_items = sort_items.limit(int(top))

        items = [item for item in k_items]

        return{
        'open_time':[item['open_time'] for item in items],
        'close_time':[item['close_time'] for item in items],
        'km':[item['km'] for item in items]

        }
#List open times only
class listOpenOnly(Resource):
    def get(self):
        top = request.args.get("top")
        if top == None:
            top = 20
        _items = db.tododb.find()
        sort_items = _items.sort("open_time")
        k_items = sort_items.limit(int(top))

        return{
        'open_time':[item['open_time'] for item in k_items],
        'km':[item['km'] for item in k_items]

        }
#
#
#list close times only
class listCloseOnly(Resource):
    def get(self):
         top = request.args.get("top")
         if top == None:
              top =20
         _items = db.tododb.find()
         sort_items = _items.sort("close_time")
         k_items = sort_items.limit(int(top))

         return {
         'close_time':[item['close_time'] for item in k_items],
         'km':[item['km'] for item in k_items]
         }
#
# ##################################################

#class listAllJson):
class listAlljson(Resource):
    def get(self):
        top = request.args.get("top")
        if top == None:
          top = 20
        _items = db.tododb.find()
        sort_items = _items.sort("open_time")
         #make it to limit k top
        k_items = sort_items.limit(int(top))

        items = [item for item in k_items]

#
        return {
        'open_time':[item['open_time'] for item in items],
        'close_time':[item['close_time'] for item in items],
        'km':[item['close_time'] for item in items] }

#listOpenOnlyJson
class listOpenOnlyjson(Resource):
    def get(self):
        top = request.args.get("top")
        if top == None:
            top = 20


        _items = db.tododb.find()
        sort_items = _items.sort("open_time")
        k_items = sort_items.limit(int(top))

        return {
        'open_time': [item['open_time'] for item in k_items]
        }

#listCloseOnlyJson
class listCloseOnlyjson(Resource):
    def get(self):
        top = request.args.get("top")
        if top == None:
            top =20
        #      _items = db.tododb.find()
        #      return { 'close_time': [item["close_time"] for item in _items]}
        # else:
        _items = db.tododb.find()
        sort_items = _items.sort("close_time")
        k_items = sort_items.limit(int(top))
        #actually km wont show up
        return {
        'close_time': [item["close_time"] for item in k_items]
        }
class listAllcsv(Resource):
    def get(self):
        top = request.args.get("top")
        if top == None:
            top = 20 # total have 20 row
        _items = db.tododb.find()
        sort_items = _items.sort("open_time")
        k_items = sort_items.limit(int(top))

        csv = "List All Time In CSV: "
        for item in k_items:
            csv += item['km']+ ' , ' +item['open_time']+ ' , '+ item['close_time'] + ', '
        # app.logger.debug('csv:{}'.format(csv))
        return csv

class listOpenOnlycsv(Resource):
    def get(self):
        top = request.args.get('top')
        if top == None:
            top = 20

        _items = db.tododb.find()
        sort_items = _items.sort("open_time")
        k_items = sort_items.limit(int(top))

        csv = 'List Open Only in CSV: '
        #\n doesnt work here
        for item in k_items:
            csv += item['km']+' , '+item['open_time']+', '

        return csv


class listCloseOnlycsv(Resource):
    def get(self):
        top = request.args.get('top')
        if top == None:
            top = 20

        _items = db.tododb.find()
        sort_items = _items.sort("close_time")
        k_items = sort_items.limit(int(top))

        csv = 'List Close Only in CSV: '

        for item in k_items:
            csv += item['km'] + ' , ' + item['close_time']+ ', '

        # app.logger.debug('csv:{}'.format(csv))
        return csv

# Create routes
# Another way, without decorators
# class index(Resource):
#     def get(self):
#         return make_response(render_template('index.html'))


# this is for the project7
class register(Resource):
    def post(self):
        username = request.form['username']
        password = request.form['password']
        existing_username = users.usersdb.find_one({'username' : username})
        if username == None or password == None:
            return "Need password or usename", 400
        elif existing_username is not None:
            return "The username already exist", 400
        else:
            password = hash_password(str(password))
            #define the id
            app.config["LENGTH"] += 1
            _id = app.config["LENGTH"]
            new_user = { 'location' : _id, 'username' : username, 'password' : password}

            users.usersdb.insert_one(new_user)
            #check the databse for the usersdb
            _items = users.usersdb.find()
            app.logger.debug(_items)
            items = [item for item in _items]
            app.logger.debug(items)
            reponse = {'location':_id,'username':username,'password':password}
            return reponse, 201


class token(Resource):
    def get(self):
        username = request.args.get("username")
        password = request.args.get("password")
        existing_username = users.usersdb.find_one({'username': username})

        if username == None or password == None:
            return "Please go to localhost:5001/api, have a registration", 400
        elif existing_username == None:
            return "Please re-typing your username", 401
        else:
            password_correct = verify_password(password, existing_username["password"])
            if(password_correct):
                _token = generate_auth_token(existing_username['location'], 600)
                return make_response(jsonify({'token' : _token.decode('ascii'), 'duration' : 600}), 201)
            else:
                return "Password or Username is wrong", 401

class protected(Resource):
    def get(self,token):
        if(verify_auth_token(token)):
            _items = db.tododb.find()
            items = [item for item in _items]
            return {'open_time':[item['open_time'] for item in items],
            'close_time':[item['close_time'] for item in items]}
        else:
            return "Unauthorized", 401







#register

#_token
# api.add_resource(index, '/api')
api.add_resource(token, '/api/token')
api.add_resource(register,'/api/register')
api.add_resource(protected,'/api/protected/<string:token>')

#first part:
api.add_resource(listAll,'/listAll')
api.add_resource(listOpenOnly,'/listOpenOnly')
api.add_resource(listCloseOnly,'/listCloseOnly')
#
# #################################################
api.add_resource(listAllcsv,'/listAll/csv')
api.add_resource(listOpenOnlycsv,'/listOpenOnly/csv')
api.add_resource(listCloseOnlycsv,'/listCloseOnly/csv')
# ########################################################
#
api.add_resource(listAlljson,'/listAll/json')
api.add_resource(listOpenOnlyjson, '/listOpenOnly/json')
api.add_resource(listCloseOnlyjson, '/listCloseOnly/json')



# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
