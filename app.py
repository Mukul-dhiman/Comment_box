from flask import Flask,render_template,session, request ,redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb

import os

# all important functions are in functions.py
from packages.functions import *

# for effective search
from packages.search import Result

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
                return redirect(url_for('CommentBox'))
        except Exception as e:
            return str(e)
    return render_template('EnterName.html')

@app.route('/EnterName')
def EnterName():
    if 'name' in session:
        session.pop('name', None)
    return render_template('EnterName.html')

@app.route('/CommentBox',methods=['GET','POST'])
def CommentBox():
    if(request.method == 'POST'):
        form = request.form
        text = form['comment']
        file = request.files['fileToUpload']
        name = 'UnKnown'
        
        if 'name' in session:
            name = session['name']
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            parent_id = "super"
            current_id = Generate_random_id(16)

            #store image in static/images
            store_image(file,current_id)

        
            current_time = current_time_string()
            cursor.execute("insert into comment value(%s,%s,%s,%s,%s)",(current_id,parent_id,  name, text, current_time))
            mysql.connection.commit()
            cursor.close()
        
        except Exception as e:
            return str(e)
    name = session['name']
    return render_template('CommentBox.html',Name=name)

@app.route('/CommentSection/<comment_id>')
def CommentSection(comment_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from comment  where parent_id  = %s", [comment_id])
    comment_data = cursor.fetchall()
    cursor.close()
    
    # for image 
    path = os.getcwd() + "/static/images/" + str(id) + os.path.splitext(file.filename)[1]
    if os.path.isfile(path):
        os.remove(path)
    return render_template('CommentSection.html',comment_data = comment_data)

@app.route('/search',methods=['POST'])
def search():
    if(request.method=='POST'):
        form = request.form
        query=form['search']
        if query=='':
            return render_template('CommentBox.html')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        result = Result(cursor,query)
        cursor.close()
    return render_template('search_results.html',result = result)

@app.route('/CommentReply/<comment_id>', methods=['POST'])
def CommentReply(comment_id):
    if(request.method=='POST'):
        form = request.form
        text = form['comment']
        name = 'UnKnown'
        if 'name' in session:
            name = session['name']
        reply_current_id = Generate_random_id(16)
        parent_id = comment_id
        current_time = current_time_string()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("insert into comment value(%s,%s,%s,%s,%s)",(reply_current_id,parent_id,  name, text, current_time))
        mysql.connection.commit()
        cursor.close()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select parent_id from comment  where comment_id  = %s", [comment_id])
    grand_parent = cursor.fetchall()
    cursor.close()
    return CommentSection(grand_parent[0]['parent_id'])



# setting a secret key for the session
app.secret_key = 'os.urandom(16)'

# running the main application
if __name__=='__main__':
    app.run(debug=True)