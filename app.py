from flask import Flask,render_template
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
    return render_template('index.html')

if __name__=='__main__':
    app.run(debug=True)