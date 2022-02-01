from flask import Flask, g, render_template, request
import sqlite3
import random

app = Flask(__name__)

def get_message_db():

    #Checks whether there is a database called message_db in the g attribute of the app
    if 'message_db' not in g:
        g.message_db = sqlite3.connect('message_db.sqlite')
        
    #Checks whether a table called messages exists in message_db, 
    #and creates it if not. Gives the columns id, handle, and message
    g.message_db.execute(   '''
                            CREATE TABLE IF NOT EXISTS messages 
                            (id INTEGER, handle TEXT, message TEXT);
                            ''')
    #returns the connection to the database
    return g.message_db

def insert_message(request):

    #extracts the message and handle from the post request
    #ie. assigns the user's submission to variables 
    mVal = request.form["mess"]
    hVal = request.form["user"]

    #assigns database connection to variable
    db = get_message_db()

    #will find length of table in database
    count = db.execute("SELECT COUNT(*) FROM messages;")
    #add one to length of table to ensure every submission has a unique id
    iVal = int(count.fetchall()[0][0]) + 1
    #assign previous variables to each sequential column in database
    db.execute('INSERT INTO messages (id, handle, message) VALUES (?, ?, ?)',
                (iVal, hVal, mVal))
    #saves your varibles into database
    db.commit()
    #close connection to database
    db.close()

    return 

def random_messages(n):

    #connect to the database
    db = get_message_db()
    
    #extract a randomized list containing 5 random messages and their handles
    id = db.execute('''
                    SELECT message, handle FROM messages 
                    ORDER BY RANDOM() LIMIT (?);
                    ''', (n,))
    idFetch = id.fetchall()

    #close the database
    db.close()

    #return list of tuples of all the messages and their handles
    return idFetch

#route this function to the url ".../submit/" w/ both POST and GET methods usable
@app.route('/submit/', methods=['POST', 'GET'])
def submit():
    if request.method == 'GET':
        #this will render the base templete submit.html to the website when there has not been a post method submitted
        return render_template('submit.html')
    else:
        #try to extract the user submission and upload it into the database
        try:
            insert_message(request)
            return render_template('submit.html', thanks = True)
        #if fails, shows a message on the base template saying there was an error
        except:
            return render_template('submit.html', error = True)

#route this function to the url ".../view/" w/ GET method only
@app.route('/view/', methods=['GET'])
def view():
    try:
        #try to extract a random number of messages (1-5) from the database
        rNum = random.randint(1, 5)
        mssg = random_messages(rNum)
        #if succesful, post those messages to the template
        return render_template('view.html', mssg = mssg)
    except:
        #if fails, shows a message on the base template saying there was an error
        return render_template('view.html', error = True)

