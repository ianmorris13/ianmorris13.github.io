---
layout: post
title: Blog Post 2
---
# Web Development

In this blog post, I will show you how to create a webapp using Flask. The app will take in a user submitted message and their handler into a database. In addition, we will be able to view a sample of the messages by pulling from the database.

## Python Functions

There are five functions that I used in the creation of this web app. 

### 1
The overall function of get_message_db() is to make sure there is a table 'messages' in a database 'message_db' and a connection to this database. This will ensure that we can later modify the database in future functions.


```python
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
```

### 2
The insert_message(request) function will take in request as a parameter. Request is a built in object of the Flask library. Its built in attributes make it easy to extract user submitted data from a POST form. It will take this extracted data, which is the user's message and handle, and then submit it into the previously made database.


```python
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
```

### 3
This function will allow the url ".../submit/" to display the html template with the added variables that I will go through below. It will give tangible proof of the functions from above.


```python
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
```

### 4
This function will take a parameter n, which is the max number of messgaes and their handles extracted from the database that it shall return. This will make it possible that there is a list of messages and handles that can be displayed on the website.


```python
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
```

### 5
This last function will allow the url ".../view/" to display the html template with the added variable of the randomized messages, the final product of all the above functions


```python
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
```

## HTML Template
Below I will show an example of the HTML templates I referenced to in the functions explination. I will comment line by line the importance of each code.


```python
#extends 'base.html' allows you to import another html file 
#this is useful since the template for base.html was used in multiple html files
{% extends 'base.html' %}

#block gives you a way to divide code into coherent groupings
{% block header %}
  <h1>{% block title %}Some Cool Messages{% endblock %}</h1>
{% endblock %}

{% block content %}

#the if jinja operator allows for variables to be passed in from the functions that are
#beneath the @app.route as long as the function is under the path
{% if error %} 
#this code says that if an error exists, then print this statement and end
<br>
Uhhh idk what happened but an error occured sorry idk why.
{% endif %}

{% if mssg %}
#this code says if the variable mssg exists...
    <br>
    #loop through each element
    {% for m in mssg %}
    #this section has id 'quote' to make it easy to read in CSS
    <section id="quote">
    #this will print the 0th element of the m element of mssg
        "{{m[0]}}"
    </section>
    #same as above
    <section id ="author">
        - {{m[1]}}<br>
    </section>
    <br>
    {% endfor %}

# I added this just if there was no mssg yet uploaded in the database
# there will be a small message letting you know.
{% else %}
    I'm sorry, it seems there have been no messages submitted. 
    You can start by clicking submit a message.
{% endif %}
{% endblock %}

```

These HTML templates make it easy to compile websites, especially when extending, as it provides ways to quickly keep a website uniform. The Jinja syntax also makes passing varibles easy to ajust websites as new imformation is presented.

## Screencaps

![Screencap 1](ianmorris13.github.io/static/images/scrnshtOne.png "Screencap 1")
![Screencap 2](ianmorris13.github.io/static/images/scrnshtTwo.png "Screencap 2")

## Repository Link
https://github.com/ianmorris13/ianmorris13.github.io/tree/master/blog-post-2
