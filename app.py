from flask import Flask,render_template,session, request ,redirect, url_for
import sqlite3

import os



# all important functions are in functions.py
from packages.functions import *

# for effective search
from packages.search import Result

# constructiong Flask object
app=Flask(__name__)

cur_dir = os.getcwd()

conn = sqlite3.connect('database.db')





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
            with sqlite3.connect("database.db") as conn:
                cursor = conn.cursor()
                parent_id = "super"
                current_id = Generate_random_id(16)

                #store image in static/images
                store_image(file,current_id)


                current_time = current_time_string()

                query = "insert into comment (comment_id ,parent_id,author,comments_text,comment_on) values('" + str(current_id) +"','" + str(parent_id) + "','" + str(name) + "','" + str(text) + "','" + str(current_time) + "')"
                cursor.execute(query)
                conn.commit()
        except:
            conn.rollback()

        finally:
            name = session['name']
            return render_template('CommentBox.html',Name=name)
            conn.close()
    name = session['name']
    return render_template('CommentBox.html',Name=name)

@app.route('/CommentSection/<comment_id>')
def CommentSection(comment_id):
    try:
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            query = "select * from comment  where parent_id  = '" +str(comment_id) + "'"
            cursor.execute(query)
            comment_data = cursor.fetchall()
    except:
            conn.rollback()

    finally:
        conn.close()
        return render_template('CommentSection.html',comment_data = comment_data)

@app.route('/search',methods=['POST'])
def search():
    result = []
    if(request.method=='POST'):
        form = request.form
        query=form['search']
        if query=='':
            return render_template('CommentBox.html')
        try:
            with sqlite3.connect("database.db") as conn:
                cursor = conn.cursor()
                result = Result(cursor,query)
        except:
            conn.rollback()

        finally:
            conn.close()
            print("yes")
            return render_template('search_results.html',result = result)
    

@app.route('/CommentReply/<comment_id>', methods=['POST'])
def CommentReply(comment_id):
    if(request.method=='POST'):
        form = request.form
        text = form['comment']
        file = request.files['fileToUpload']

        name = 'UnKnown'
        if 'name' in session:
            name = session['name']
        reply_current_id = Generate_random_id(16)

        #store image in static/images
        store_image(file,reply_current_id)

        parent_id = comment_id
        current_time = current_time_string()
        try:
            with sqlite3.connect("database.db") as conn:
                cursor = conn.cursor()
                query = "insert into comment (comment_id ,parent_id,author,comments_text,comment_on) values('"+str(reply_current_id)+"','"+str(parent_id)+"','"+str(name)+"','"+str(text)+"','"+str(current_time)+"')"
                cursor.execute(query)
                conn.commit()
        except:
            conn.rollback()

        finally:
            conn.close()
    try:
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            query = "select parent_id from comment  where comment_id  = '" + str(comment_id) +"'"
            cursor.execute(query)
            grand_parent = cursor.fetchall()
    except:
        conn.rollback()
    finally:
        conn.close()
    return CommentSection(grand_parent[0][0])



# setting a secret key for the session
app.secret_key = 'os.urandom(16)'

# running the main application
if __name__=='__main__':
    app.run(debug=True)