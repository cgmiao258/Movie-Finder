from flask import Flask, request, render_template, url_for, redirect, flash, session
from forms import RegistrationForm, LoginForm, SearchForm, DeleteAccountForm
from flaskext.mysql import MySQL
from flask_cors import CORS
from collections import OrderedDict
from datetime import datetime
import pymysql
import pandas as pd

# to run flask use "set FLASK_APP=backend.py"
# then "flask run" or "python backend.py" to have active changes for refresh (don't need to rerun code/flask)

app = Flask(__name__)

app.config['SECRET_KEY'] = 'f5a98f86109a27d16d08d2f0eaca8549'

isloggedin = False
def isloggedinfunc(x):
    global isloggedin
    isloggedin = x

currentusername = 'Please login to see username here'
def currentusernamefunc(x):
    global currentusername
    currentusername = x

timesloggedin = 0
def timesloggedinfunc(x):
    global timesloggedin
    timesloggedin = x

currentemail = 'Sample'
def currentemailfunc(x):
    global currentemail
    currentemail = x

# home page
@app.route('/')
@app.route('/home')
def home():
    # show top 10 movies that have at least 3000 ratings with their crew members (writers and directors) with the number of ratings, avg ratings, genres, movie name 
    # as recommendations on home page
    connection = pymysql.connect(host="fake", user="fake", passwd="fake",database="fake")
    cursor = connection.cursor()
    cursor.execute("Use fake")
    # find 10 random movies that are good with at least 3000 votes and a 7.5 rating
    cursor.execute("""SELECT shows.name, shows.genres, ratings.avgrating, ratings.numvotes, crew.directornum, crew.writernum
                FROM shows JOIN ratings ON shows.movienum=ratings.movienum JOIN crew ON shows.movienum=crew.movienum 
                WHERE ratings.numvotes > 3000 AND ratings.avgrating > 7.5
                ORDER BY RAND()
                LIMIT 10""")
    data = cursor.fetchall()

    # find all the directors of the movies
    directorfulllist = []
    for x in data:
        directors = x[4].split(",")
        listofdirectors = []
        for y in directors:
            query = "SELECT people.name FROM people WHERE people.personnum = %s"
            data_tuple = ([y])
            cursor.execute(query,data_tuple)
            listofdirectors.append(str(cursor.fetchone()).replace("'","").replace(",","").replace("(","").replace(")","").replace('"',''))
        directorfulllist.append(listofdirectors)
    
    # find all writers of the movies
    writerfulllist = []
    for x in data:
        writers = x[5].split(",")
        listofwriters = []
        for y in writers:
            query = "SELECT people.name FROM people WHERE people.personnum = %s"
            data_tuple = ([y])
            cursor.execute(query,data_tuple)
            listofwriters.append(str(cursor.fetchone()).replace("'","").replace(",","").replace("(","").replace(")","").replace('"',''))
        writerfulllist.append(listofwriters)

    # create the dictionary of movies to be show on home page
    display = []
    for (i,j,k) in zip(data, directorfulllist, writerfulllist):
        toappend = {
            'moviename': i[0],        
            'genres': i[1],        
            'rating': i[2],
            'num_votes': i[3],
            'directors': ', '.join(j),
            'writers' : ', '.join(k)
        }
        display.append(toappend)
       
    return render_template('home.html', data=display, title='Home', logg = isloggedin)

# about page
@app.route('/about')
def about():
    return render_template('about.html', title='About', logg = isloggedin)

# register page
@app.route("/register", methods=['GET', 'POST'])
def register():
    if isloggedin:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # check if user already exists
        connection = pymysql.connect(host="fake", user="fake", passwd="fake",database="fake")
        cursor = connection.cursor()
        cursor.execute("use fake")
        sql_query = "SELECT COUNT(*) FROM users WHERE username = %s"
        data_tuple = (form.username.data)
        cursor.execute(sql_query,data_tuple)
        datausers = cursor.fetchone()[0]
        
        cursor.execute("use fake")
        sql_query = "SELECT COUNT(*) FROM users WHERE email = %s"
        data_tuple = (form.email.data)
        cursor.execute(sql_query,data_tuple)
        dataemail = cursor.fetchone()[0]
        # if user doesn't exist, insert into database
        if datausers==0 and dataemail==0:
            sql_query2 = """Insert into users(username, email, password, timesloggedin) VALUES(%s, %s, %s, %s)"""
            data_tuple2 = ([form.username.data],[form.email.data],[form.password.data], [0])
            cursor.execute(sql_query2,data_tuple2)
            connection.commit()
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('home'))
        elif datausers!=0:
            flash(f'Username already taken. Please choose a differet one.','danger')
        elif dataemail!=0:
            flash(f'Email already taken. Please choose a differet one.','danger')            
    return render_template('register.html', title='Register', form=form)
    
# login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if isloggedin:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        # confirm that the email+password are in the sql database for users
        connection = pymysql.connect(host="fake", user="fake", passwd="fake",database="fake")
        cursor = connection.cursor()
        cursor.execute("use fake")
        sql_query = "SELECT COUNT(*) FROM users WHERE email = %s AND password = %s"
        data_tuple = ([form.email.data],[form.password.data])
        cursor.execute(sql_query,data_tuple)
        data = cursor.fetchone()[0]
        if data!=0:
            flash('Login successful!', 'success')
            isloggedinfunc(True)
            # update the number of times loggedin
            cursor.execute("use fake")
            sql_query = "SELECT timesloggedin, username FROM users WHERE email = %s AND password = %s"
            data_tuple = ([form.email.data],[form.password.data])
            cursor.execute(sql_query,data_tuple)
            accountdata = cursor.fetchone()
            logincount = accountdata[0] + 1
            username = accountdata[1]
            cursor.execute("use fake")
            sql_query = "UPDATE users SET timesloggedin = %s WHERE email = %s AND password = %s"
            data_tuple = (([logincount]),[form.email.data],[form.password.data])
            cursor.execute(sql_query,data_tuple)
            connection.commit()
            # grab the currentusername and number of times loggedin
            currentusernamefunc(username)
            timesloggedinfunc(logincount)
            currentemailfunc(form.email.data)
            return redirect(url_for('home'))
        else:
            flash("Login failed, Please check email and password", "danger")
    return render_template('login.html', title='Login', form=form)

# logout route
@app.route('/logout')
def logout():
    isloggedinfunc(False)
    flash(f'Logged out!', 'success')
    return redirect(url_for('home'))

# account route
@app.route('/account', methods = ['GET','POST'])
def account():
    form = DeleteAccountForm()
    if isloggedin == False:
        return redirect(url_for('home'))
    if form.deletebutton.data:
        connection = pymysql.connect(host="fake", user="fake", passwd="fake",database="fake")
        cursor = connection.cursor()
        cursor.execute("use fake")
        sqlquery = """DELETE FROM users WHERE users.username = %s AND users.email = %s"""
        data_tuple = ([currentusername],[currentemail])
        cursor.execute(sqlquery,data_tuple)
        connection.commit()
        isloggedinfunc(False)
        return redirect(url_for('home'))
    return render_template('account.html', title='Account', username=currentusername, timesloggedin=timesloggedin, email = currentemail, logg = isloggedin, form=form)

# search route
@app.route("/search", methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        if form.person.data != form.mediatype.data:
            # allows other routes to use this data
            session['search'] = form.search.data
            session['persontype'] = form.person.data
            session['mediatype'] = form.mediatype.data
            return redirect(url_for('results'))
        else:
            flash("Please choose only one of Actor/Writer/Director or Movie/Show", "danger")
    return render_template('search.html', title="Search", logg=isloggedin, form=form)

# results route
@app.route("/results")
def results():
    # grab the data from other search route
    search = session.get('search')
    persontype = session.get('persontype')
    mediatype = session.get('mediatype')
    connection = pymysql.connect(host="fake", user="fake", passwd="fake",database="fake")
    cursor = connection.cursor()
    cursor.execute("USE fake")
    returnthis = []
    actorbool = False
    showbool = False
    if persontype:
        actorbool = True
        # find out who the person that is being searched for is
        searchquery = ("""SELECT people.name, people.birthyear, people.deathyear, people.profession, people.knownfor
                FROM people
                WHERE people.name LIKE %s
                ORDER BY RAND()
                LIMIT 50""")
        cursor.execute(searchquery, '%' + search + '%')
        data = cursor.fetchall()
        moviesknownfor = []
        
        # find out what movies that person is known for
        for x in data:
            movies = x[4].split(",")
            listofmovies = []
            for y in movies:
                query = ("""SELECT shows.name, ratings.avgrating
                            FROM shows NATURAL JOIN ratings NATURAL JOIN crew
                            WHERE shows.movienum = %s
                            """)
                data_tuple = ([y])
                cursor.execute(query, data_tuple)
                fetched = cursor.fetchall()
                if len(fetched) == 0:
                    continue
                else:
                    listofmovies.append(str(fetched[0][0]).replace("'","").replace(",","").replace("(","").replace(")","").replace('"','') + ", Rating: " 
                                    + str(fetched[0][1]).replace("'","").replace(",","").replace("(","").replace(")","").replace('"',''))
            if len(listofmovies) == 0:
                moviesknownfor.append(["None, Rating: None"])
            else:
                moviesknownfor.append(listofmovies)

        # put all data in a dict to be returned
        for (i,j) in zip(data, moviesknownfor):
            toappend = {
            'personname': i[0],        
            'birthyear': i[1],        
            'deathyear': i[2],
            'profession': i[3],
            'knownfor': j
            }  
            returnthis.append(toappend) 
        for i in returnthis:
            if i['birthyear'] == 0:
                i['birthyear'] = "unknown"
            if i['deathyear'] == 3000:
                i['deathyear'] = "unknown"
                
    elif mediatype:
        showbool = True
        # find the movie that is being searched for
        searchquery = ("""SELECT shows.name, shows.genres, ratings.avgrating, ratings.numvotes, crew.directornum, crew.writernum
                FROM shows JOIN ratings ON shows.movienum=ratings.movienum JOIN crew ON shows.movienum=crew.movienum 
                WHERE shows.name LIKE %s
                ORDER BY RAND()
                LIMIT 50""")
        cursor.execute(searchquery, '%' + search + '%')
        data = cursor.fetchall()

        # find all the directors of the movies
        directorfulllist = []
        for x in data:
            directors = x[4].split(",")
            listofdirectors = []
            for y in directors:
                query = "SELECT people.name FROM people WHERE people.personnum = %s"
                data_tuple = ([y])
                cursor.execute(query,data_tuple)
                listofdirectors.append(str(cursor.fetchone()).replace("'","").replace(",","").replace("(","").replace(")","").replace('"',''))
            directorfulllist.append(listofdirectors)
        
        # find all writers of the movies
        writerfulllist = []
        for x in data:
            writers = x[5].split(",")
            listofwriters = []
            for y in writers:
                query = "SELECT people.name FROM people WHERE people.personnum = %s"
                data_tuple = ([y])
                cursor.execute(query,data_tuple)
                listofwriters.append(str(cursor.fetchone()).replace("'","").replace(",","").replace("(","").replace(")","").replace('"',''))
            writerfulllist.append(listofwriters)

        # create the dictionary of movies to be show on home page
        for (i,j,k) in zip(data, directorfulllist, writerfulllist):
            toappend = {
                'moviename': i[0],        
                'genres': i[1],        
                'rating': i[2],
                'num_votes': i[3],
                'directors': ', '.join(j),
                'writers' : ', '.join(k)
            }
            returnthis.append(toappend)
                
    return render_template('results.html', title='Results', logg = isloggedin, data=returnthis, show=showbool, person=actorbool)


if __name__ == "__main__":
    app.run(debug=True)