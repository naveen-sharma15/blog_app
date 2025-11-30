
from flask import Flask, render_template, redirect, request, session
from flask_bcrypt import Bcrypt
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key="secret123"

app.config['MYSQL_HOST']="mysql"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']="root"
app.config['MYSQL_DB']="blogdb"

mysql=MySQL(app)
bcrypt=Bcrypt(app)

@app.route('/')
def home():
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM posts ORDER BY id DESC")
    posts=cur.fetchall()
    return render_template('home.html', posts=posts)

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method=='POST':
        uname=request.form['username']
        email=request.form['email']
        password=bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO users(username,email,password) VALUES(%s,%s,%s)",(uname,email,password))
        mysql.connection.commit()
        return redirect('/login')

    return render_template('signup.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        uname=request.form['username']
        pwd=request.form['password']

        cur=mysql.connection.cursor()
        cur.execute("SELECT id,password FROM users WHERE username=%s",[uname])
        user=cur.fetchone()

        if user and bcrypt.check_password_hash(user[1],pwd):
            session['user']=user[0]
            return redirect('/')
        return "Invalid Credentials"

    return render_template('login.html')

@app.route('/add', methods=['GET','POST'])
def add():
    if 'user' not in session:
        return redirect('/login')

    if request.method=='POST':
        title=request.form['title']
        content=request.form['content']

        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO posts(title,content,user_id) VALUES(%s,%s,%s)",(title,content,session['user']))
        mysql.connection.commit()
        return redirect('/')

    return render_template('add.html')

@app.route('/edit/<id>', methods=['GET','POST'])
def edit(id):
    if 'user' not in session:
        return redirect('/login')

    cur=mysql.connection.cursor()

    if request.method=='POST':
        title=request.form['title']
        content=request.form['content']
        cur.execute("UPDATE posts SET title=%s,content=%s WHERE id=%s",(title,content,id))
        mysql.connection.commit()
        return redirect('/')

    cur.execute("SELECT * FROM posts WHERE id=%s",[id])
    post=cur.fetchone()
    return render_template('edit.html', post=post)

@app.route('/delete/<id>')
def delete(id):
    if 'user' not in session:
        return redirect('/login')
    cur=mysql.connection.cursor()
    cur.execute("DELETE FROM posts WHERE id=%s",[id])
    mysql.connection.commit()
    return redirect('/')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
