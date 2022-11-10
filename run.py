# from crypt import methods
import psycopg2

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer

from flask import Flask ,render_template,request,redirect, url_for
from flask_socketio import SocketIO

app=Flask(__name__)
conn = psycopg2.connect(host="127.0.0.1", port="5432", dbname="intermiable_units", user="postgres", password="123")
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)
cur=conn.cursor()
cur.execute('SELECT datname FROM pg_database')
result=cur.fetchall()
print(result)


@app.route("/")
def home():
    return render_template('home.html')
@app.route("/message")
def message(methods=['GET', 'POST']):
    return render_template('message.html')
with open('file.txt','r') as file:
    conversation = file.read()
print(conversation)

bot = ChatBot(" ChatBot")
trainer = ListTrainer(bot)
trainer.train(conversation)

# @socketio.on('my event')
# def handle_my_custom_event(json, methods=['GET', 'POST']):
#     print('received my event: ' + str(json))
#     socketio.emit('my response', json, callback=message)

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    response=str(bot.get_response(userText))
    print(response)
    return response
	# return str(bot.get_response(userText))

@app.route("/logout")
def logout():
    return "logout"

@app.route("/login", methods=['GET','POST'])
def login():
    if request.method=='POST':
        name=request.form.get('name')
        password=request.form.get('password')
        cur.execute("SELECT * FROM  creds where name=%(name)s and pass=%(password)s",{"name":name, "password":password})
        # ermias=cur.execute("select * from creds where name=%(username)s and pass=%(password)s",{"username":name,"password":password}).fetchall()
        record=cur.fetchall()
        print(record)
        if record:
            print("man")
            return redirect(url_for('home'))
        print(name, password)
    return render_template('login.html')
@app.route("/register", methods=['GET','POST'])
def register():
    
    if request.method=='POST':
        
        first_name=request.form.get('first_name')
        last_name=request.form.get('last_name')
        email=request.form.get('email')
        name=request.form.get('name')
        password=request.form.get('password')
        print(first_name,last_name,email,name,password)
        cur.execute('INSERT INTO creds (username,password,email,first_name,last_name)'
            'VALUES ( %s, %s, %s,%s,%s)',
            (

            name,
             password,
             email,
             first_name,
             last_name,
             
            )
            );
        conn.commit()
        

        # cur.execute("INSERT INTO creds  VALUES(%(id)i,%(name)s,%(pass)s,%(first_name)s,%(last_name)s,%(email)s);",{"id":id},{"name":name},{"pass":password},{"first_name":first_name},{"last_name":last_name},{"email":email})
        # record_reg=cur.fetchall()
        # if record_reg:
        #     print('yes man ena 1 mechemer alber id')
        #     id+=1
        #     return redirect(url_for('login'))
        # print('post nw man')

    return render_template('register.html')

@app.route("/change_password")
def transaction():
    return render_template('change_password.html')
@app.route("/transaction")
def transaction():
    return render_template('transaction.html')

if __name__=="__main__":
    app.run()
    socketio.run(app, debug=True)