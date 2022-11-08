from crypt import methods
import psycopg2
from flask import Flask ,render_template,request,redirect, url_for

app=Flask(__name__)
conn = psycopg2.connect(host="127.0.0.1", port="5432", dbname="intermiable_units", user="postgres", password="postgres")
cur=conn.cursor()
cur.execute('SELECT datname FROM pg_database')
result=cur.fetchall()
print(result)


@app.route("/")
def home():
    return render_template('home.html')
@app.route("/message")
def message():
    return render_template('message.html')

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
    id=3
    if request.method=='POST':
        id+=1
        first_name=request.form.get('first_name')
        last_name=request.form.get('last_name')
        email=request.form.get('email')
        name=request.form.get('name')
        password=request.form.get('password')
        print(first_name,last_name,email,name,password)
        cur.execute('INSERT INTO creds (user_name,first_name,last_name,email,password)'
            'VALUES (%s, %s, %s, %s,%s,%s)',
            (
            # id,
            name,
             password,
             first_name,
             last_name,
             email,
            )
            )
        conn.commit()
        

        # cur.execute("INSERT INTO creds  VALUES(%(id)i,%(name)s,%(pass)s,%(first_name)s,%(last_name)s,%(email)s);",{"id":id},{"name":name},{"pass":password},{"first_name":first_name},{"last_name":last_name},{"email":email})
        # record_reg=cur.fetchall()
        # if record_reg:
        #     print('yes man ena 1 mechemer alber id')
        #     id+=1
        #     return redirect(url_for('login'))
        # print('post nw man')

    return render_template('register.html')
@app.route("/transaction")
def transaction():
    return render_template('transaction.html')

if __name__=="__main__":
    app.run()