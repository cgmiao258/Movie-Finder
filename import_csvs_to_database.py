import pymysql
import pandas as pd

# function to create all tables in database
def createtables():
    # connect to database
    connection = pymysql.connect(host="fakehost", user="fakeroot", passwd="fakepwd",database="fakedb")
    cursor = connection.cursor()
    # creating people table
    # personnum is the identifier
    # name is the person's full name
    # birthyear is the person's birthyear
    # deathyear is the person's date of death if they have died already
    # profession is the person's top 3 professions
    # knownfor is the titles that the person is most known for
    createtablequery = "create table if not exists people(personnum varchar(255), name varchar(255), birthyear int, deathyear int, profession varchar(255), knownfor varchar(255))" 
    cursor.execute(createtablequery)
    
    # creating shows table
    # movienum is the identifier
    # type is the type of media of the title
    # name is the name of the media
    # originalname is the name of the media in the original language
    # adult is an identifier if the show is for adults or not - 0 for no and 1 for yes
    # startytear is when the media was released
    # endyear is the end of a series otherwise none
    # length is how long the media is in minutes
    # genres is the top 3 genres associated with this media
    createtablequery = "create table if not exists shows(movienum varchar(255), type varchar(255), name LONGTEXT, originalname LONGTEXT, adult int, startyear int, endyear int, length varchar(255), genres varchar(255))"
    cursor.execute(createtablequery)
    
    # creating crew table
    # movienum is the identifier
    # directornum is the list of director's identifiers
    # writernum is the list of writer's identifiers
    createtablequery = "create table if not exists crew(movienum varchar(255), directornum LONGTEXT, writernum LONGTEXT)"
    cursor.execute(createtablequery)
    
    # creating episode table
    # episodenum is the identifier
    # parentnum is the identifier of the parent TV series
    # season is the season number
    # episode is the episode number
    createtablequery = "create table if not exists episode(episodenum varchar(255), parentnum varchar(255), season int, episode int)"
    cursor.execute(createtablequery)
    
    # creating principals table
    # movienum is identifier
    # ordernum is which row for given movienum
    # personnum is identifier
    # category is what category the job belongs to
    # job is the job title
    # charname is the name of the character that is played
    createtablequery = "create table if not exists principals(movienum varchar(255), ordernum int, personnum varchar(255), category varchar(255), job LONGTEXT, charname LONGTEXT)"
    cursor.execute(createtablequery)
    
    # creating table ratings
    # movienum is the identifier
    # avgrating is the average rating that the media received
    # numvotes is the number of votes received
    createtablequery = "create table if not exists ratings(movienum varchar(255), avgrating double, numvotes int)"
    cursor.execute(createtablequery)


# function to insert data into ratings table 
def insertratings():
    connection = pymysql.connect(host="fakehost", user="fakeroot", passwd="fakepwd",database="fakedb")
    cursor = connection.cursor()
    # load local file for ratings
    df = pd.read_csv(r'C:\Users\cmiao5\Desktop\projects\title.ratings.csv')
    dataarray = df.to_numpy()
    # insert data into ratings table in database
    for x in dataarray:
        movienum = x[0]
        avgrating = x[1]
        numvotes = x[2]
        cursor.execute("insert into ratings value(\"{}\", \"{}\", \"{}\")".format(movienum,avgrating,numvotes))  
    connection.commit()

# function to insert data into crew table 
def insertcrew():
    connection = pymysql.connect(host="fakehost", user="fakeroot", passwd="fakepwd",database="fakedb")
    cursor = connection.cursor()
    # load local file for crew
    df = pd.read_csv(r'C:\Users\cmiao5\Desktop\projects\title.crew.csv')
    dataarray = df.to_numpy()
    # insert data into crew table in database
    for x in dataarray:
        movienum = x[0]
        directornum = x[1]
        writernum = x[2]
        cursor.execute("insert into crew value(\"{}\", \"{}\", \"{}\")".format(movienum,directornum,writernum))   
    connection.commit()
    
# function to insert data into episode table 
def insertepisode():
    connection = pymysql.connect(host="fakehost", user="fakeroot", passwd="fakepwd",database="fakedb")
    cursor = connection.cursor()
    # load local file for episode
    df = pd.read_csv(r'C:\Users\cmiao5\Desktop\projects\title.episode.csv')
    dataarray = df.to_numpy()
    # insert data into episode table in database
    for x in dataarray:
        episodenum = x[0]
        parentnum = x[1]
        if x[2].isdigit():
            season = x[2]
        else:
            season = 0
        if x[2].isdigit():
            episode = x[2]
        else:
            episode = 0
        cursor.execute("insert into episode value(\"{}\", \"{}\", \"{}\",\"{}\")".format(episodenum,parentnum,season,episode))  
    connection.commit()

# function to insert data into people table 
def insertpeople():
    connection = pymysql.connect(host="fakehost", user="fakeroot", passwd="fakepwd",database="fakedb")
    cursor = connection.cursor()
    # load local file for people
    df = pd.read_csv(r'C:\Users\cmiao5\Desktop\projects\name.basics.csv')
    dataarray = df.to_numpy()
    # insert data into people table in database
    for x in dataarray:
        personnum = x[0]
        name = x[1].replace('"', '')
        if x[2].isdigit():
            birthyear = x[2]
        else:
            birthyear = 0
        if x[3].isdigit():
            deathyear = x[3]
        else:
            deathyear = 3000
        profession = x[4]
        knownfor = x[5]
        cursor.execute("insert into people value(\"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\")".format(personnum,name,birthyear,deathyear,profession,knownfor))  
    connection.commit()
    
# function to insert data into principals table 
def insertprincipals():
    connection = pymysql.connect(host="fakehost", user="fakeroot", passwd="fakepwd",database="fakedb")
    cursor = connection.cursor()
    # load local file for principals
    df = pd.read_csv(r'C:\Users\cmiao5\Desktop\projects\title.principals.csv')
    dataarray = df.to_numpy()
    # insert data into principals table in database
    for x in dataarray:
        movienum = x[0]
        ordernum = x[1]
        personnum = x[2]
        category = x[3]
        job = x[4].replace('"','')
        charname = x[5].replace('"','')
        cursor.execute("insert into principals value(\"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\")".format(movienum,ordernum,personnum,category,job,charname))  
    connection.commit()
    
# function to insert data into shows table 
def insertshows():
    connection = pymysql.connect(host="fakehost", user="fakeroot", passwd="fakepwd",database="fakedb")
    cursor = connection.cursor()
    # load local file for shows
    df = pd.read_csv(r'C:\Users\cmiao5\Desktop\projects\title.basics.csv')
    dataarray = df.to_numpy()
    # insert data into shows table in database
    for x in dataarray:
        movienum = x[0]
        type = x[1]
        name = str(x[2]).replace('"', '')
        originalname = str(x[3]).replace('"', '')
        adult = x[4]
        if isinstance(adult, int) == False:
            adult = 999
        if isinstance(x[6], str):
            startyear = 0
        else:
            startyear = x[5]
        if x[6].isdigit():
            endyear = x[6]
        else:
            endyear = 3000
        length = x[7]
        genres = x[8]
        cursor.execute("insert into shows value(\"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\",\"{}\")".format(movienum,type,name,originalname,adult,startyear,endyear,length,genres))  
    connection.commit()

#add primary keys to all tables
def primarykeyscrew():
    connection = pymysql.connect(host="fakehost", user="fakeroot", passwd="fakepwd",database="fakedb")
    cursor = connection.cursor()
    cursor.execute("ALTER TABLE crew ADD PRIMARY KEY (movienum);")
    connection.commit()
def primarykeysepisode():
    connection = pymysql.connect(host="fakehost", user="fakeroot", passwd="fakepwd",database="fakedb")
    cursor = connection.cursor()
    cursor.execute("ALTER TABLE episode ADD PRIMARY KEY (episodenum);")
    connection.commit()
def primarykeyspeople():
    connection = pymysql.connect(host="fakehost", user="fakeroot", passwd="fakepwd",database="fakedb")
    cursor = connection.cursor()
    cursor.execute("ALTER TABLE people ADD PRIMARY KEY (personnum);")
    connection.commit()
def primarykeysratings():
    connection = pymysql.connect(host="fakehost", user="fakeroot", passwd="fakepwd",database="fakedb")
    cursor = connection.cursor()
    cursor.execute("ALTER TABLE ratings ADD PRIMARY KEY (movienum);")
    connection.commit()
def primarykeysshows():
    connection = pymysql.connect(host="fakehost", user="fakeroot", passwd="fakepwd",database="fakedb")
    cursor = connection.cursor()
    cursor.execute("ALTER TABLE shows ADD PRIMARY KEY (movienum);")
    connection.commit()

# extra table for user login information
def createuserstable():
    connection = pymysql.connect(host="fakehost", user="fakeroot", passwd="fakepwd",database="fakedb")
    cursor = connection.cursor()
    createtablequery = "create table if not exists users (username varchar(255) NOT NULL UNIQUE, email varchar(255) NOT NULL, password varchar(255), timesloggedin int, PRIMARY KEY (username))"
    cursor.execute(createtablequery)    
    connection.commit()


# createtables()
# insertratings()
# insertcrew()
# insertepisode()
# insertpeople()
# insertprincipals()
# insertshows()
# primarykeyscrew()
# primarykeysepisode()
# primarykeyspeople()
# primarykeysratings()
# primarykeysshows()
# createuserstable()

