from flask import Flask,render_template,session
from flask_mysqldb import MySQL
# import MySQLdb

app=Flask(__name__)

import yaml
db = yaml.load(open('db.yaml'))
app.config['MYSQ_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db'] 
mysql = MySQL(app)



@app.route('/')
def home():
    if(request.method == 'POST'):
        form = request.form
        name = form['name']
        try:
                session['name'] = name 
        except Exception as e:
            return str(e)
    return render_template('EnterName.html')



app.secret_key = 'os.urandom(16)'
if __name__=='__main__':
    app.run(debug=True)