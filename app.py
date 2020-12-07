from flask import Flask,render_template,session, request ,redirect, url_for
from flask_mysqldb import MySQL

# constructiong Flask object
app=Flask(__name__)


import yaml
db = yaml.load(open('db.yaml'))
app.config['MYSQ_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db'] 
mysql = MySQL(app)



@app.route('/',methods=['POST'])
def NamePage():
    if(request.method == 'POST'):
        if 'name' in session:
            session.pop('name', None)
        form = request.form
        name = form['name']
        try:
            session['name'] = name
            if(name!=''):
                print(name)
                return redirect(url_for('CommentBox'))
        except Exception as e:
            return str(e)
    return render_template('EnterName.html')

@app.route('/EnterName')
def EnterName():
    if 'name' in session:
        session.pop('name', None)
    return render_template('EnterName.html')

@app.route('/CommentBox',methods=['GET'])
def CommentBox():
    name = session['name']
    return render_template('CommentBox.html',Name=name)


# setting a secret key for the session
app.secret_key = 'os.urandom(16)'

# running the main application
if __name__=='__main__':
    app.run(debug=True)