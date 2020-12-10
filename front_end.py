from tkinter import *
import random
import mysql.connector
import pprint
from tkinter import ttk
import tkinter.messagebox as MessageBox
from login import getUser

global user_name
user_name = getUser()



def logout():
    front_end_window.destroy()
    import login
    login.root.mainloop()

def search_now():
    #default filter
   # print("{}, {}, {}, {}".format(var1.get(), var2.get(), drop.get(), inputbox.get()))
    #variables
    checkMovie = int(var1.get())
    checkShow = int(var2.get())
    if ((checkMovie == True) & (checkShow == False)):
        target = "movies"
    elif ((checkMovie == False) & (checkShow == True)):
        target = "tvShows"
    elif ((checkMovie == True) & (checkShow == True)):
        target = "shows"
    elif ((checkMovie == False) & (checkShow == False)):
        target = "shows"

    query = "SELECT title, type, description FROM {}".format(target)

    actorDirector = drop.get()
    actorDirectorValue = inputbox.get()
    ifGenre = genreSelected.get()
    topic = topicBox.get()


    if (ifGenre == 'Every genre'):

        if ((actorDirector == "Actor") and  inputbox.index("end") != 0):
            query = ("SELECT s.title, s.type, s.release_year, s.description, s.show_id FROM (actor a join show_actor sa on a.actor_id = sa.actor_id) JOIN {} s on sa.show_id = s.show_id WHERE a.actor LIKE '%{}%' AND s.description LIKE '%{}%'").format(target,actorDirectorValue, topic)
        elif((actorDirector == "Director") and  inputbox.index("end") != 0):
            query = ("SELECT s.title, s.type, s.release_year, s.description, s.show_id FROM (director d join show_director sd on d.director_id = sd.director_id) JOIN {} s on sd.show_id = s.show_id WHERE d.director LIKE '%{}%' AND s.description LIKE '%{}%'").format(target, actorDirectorValue, topic)
        elif inputbox.index("end") == 0:
            query = ("SELECT s.title, s.type, s.release_year, s.description, s.show_id FROM {} s WHERE s.description LIKE '%{}%'").format(target, topic)

    else:
        if ((actorDirector == "Actor") and inputbox.index("end") != 0):
            query = ("""
                SELECT s.title, s.type, s.release_year, s.description , s.show_id FROM 
                    (actor a join show_actor sa on a.actor_id = sa.actor_id)
                    JOIN {} s on sa.show_id = s.show_id
                    join show_genre sg on s.show_id = sg.show_id
                    JOIN genre g ON sg.genre_id = g.genre_id
                    WHERE a.actor LIKE '%{}%' AND g.genre = '{}' AND s.description LIKE '%{}%'
                    GROUP BY 1,2
                """).format(target, actorDirectorValue, ifGenre, topic)

        elif ((actorDirector == "Director") and inputbox.index("end") != 0):
            query = ("""
            SELECT s.title, s.type, s.release_year, s.description, s.description, s.show_id FROM 
                ((( director d join show_director sd on d.director_id = sd.director_id)
                JOIN {} s on sd.show_id = s.show_id) 
                JOIN show_genre sg ON s.show_id = sg.show_id)
                JOIN genre g ON sg.genre_id = g.genre_id
                WHERE d.director LIKE '%{}%' AND g.genre = '{}' AND s.description LIKE '%{}%'
                GROUP BY s.title
            """).format(target, actorDirectorValue, ifGenre, topic)
        elif inputbox.index("end") == 0:
            query = ("""
            SELECT s.title, s.type, s.release_year, s.description, s.show_id  FROM {} s
            JOIN show_genre sg ON s.show_id = sg.show_id
            JOIN genre g ON sg.genre_id = g.genre_id
            WHERE g.genre = '{}' AND s.description LIKE '%{}%'
            """
            ).format(target, ifGenre, topic)


    #print(query)
    my_query = [query + " LIMIT 150;", "Viewing Rentals"]
    #print(filter)
    #print(my_query)
    display(my_query)


def connect():
    global db
    db = mysql.connector.connect(host="localhost", user="root", passwd="1fcn", database='dbm_netflix_project', auth_plugin='mysql_native_password', charset='utf8')
    return db

def getFilterValues():
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT genre FROM genre;")
    rows = cur.fetchall()
    con.close()
    for i in rows:
        genre.append(i[0])



global front_end_window
front_end_window=Tk()
front_end_window.title("NetflixSurfer - What Should I Watch?")
front_end_window.geometry("1000x800")

#creating a cursor and initializing it
#my_cursor = db.cursor()


#Create Table

#update list
def update_list():
    pass



def display(query):
    def update(rows):
        for i in rows:
            trv.insert('', 'end', values=i)

    clearMiddleFrame()
    x = connect()
    c = x.cursor()
    c.execute(query[0])
    rows = c.fetchall()
    global trv
    trv = ttk.Treeview(middle_frame, columns = (1,2,3,4,5), show = "headings", height = "28")
    trv.pack(side = 'left',expand=True, fill='both')
    trv.heading(1, text = "Title")
    trv.heading(2, text="Type")
    trv.heading(3, text="Release Year")
    trv.heading(4, text="Description")
    trv.heading(5, text="showId")
    trv.column("1",minwidth=0, width = 200, anchor = 'c')
    trv.column("2",minwidth=0, width=100, anchor='c')
    trv.column("3",minwidth=0, width = 100, anchor = 'c')
    trv.column("4",minwidth=0, width=500, anchor='c')
    trv.column("5",stretch = NO,minwidth=0, width=0)
    trv.grid_columnconfigure(1, weight=1)
    trv.grid_columnconfigure(2, weight=1)
    trv.grid_columnconfigure(3, weight=1)
    trv.grid_columnconfigure(4, weight=10)
    trv.grid_columnconfigure(5, weight=0)
    update(rows)

    vsb = ttk.Scrollbar(middle_frame, orient="vertical", command = trv.yview)
    vsb.pack(side='right', fill ='y')
    trv.configure(yscrollcommand=vsb.set)

    x.close()

#add a movie to a personal list of the current user
def addWatchlist(a):
    #print(trv)
    curItem = trv.focus()
    #print (trv.item(curItem)['values'])
    con = connect()
    cur = con.cursor()
    #print(user_name)
    #print((trv.item(curItem)['values'])[4])
    try:
        connection = connect()
        cur = connection.cursor()
        query = "INSERT INTO USERS_SHOWS VALUES ('{}', '{}', NOW());".format(user_name,
                                                                             (trv.item(curItem)['values'])[4])
        cur.execute(query)
        connection.commit()
        connection.close()
        MessageBox.showinfo("Movie/Show added", "The movie is now on your watchList!")
    except mysql.connector.errors.IntegrityError:
        print("movie is already on the list")
        MessageBox.showinfo("Warning", "The movie is already on your watchList")

#defaultButton.pack_forget()
#defaultButton.destroy()
#trv.bind("<<TreeviewSelect>>", selectItem) # single click, without "index out of range" error


def clearFrame():
    for widget in middle_frame.winfo_children():
        widget.destroy()
    tv_show.select()
    movie.select()
    topicBox.delete(0, 'end')
    inputbox.delete(0, 'end')

def clearMiddleFrame():
    for widget in middle_frame.winfo_children():
        widget.destroy()

def openWindow():
    global customer_name
    top = Toplevel()
    top.geometry("900x500")
    top.title("myWatchList")

    #frames and label of the new window
    top_frame2 = Frame(top, height=120, width=600, bg =  'coral')
    top_frame2.pack(fill=BOTH)
    middle_frame2 = Frame(top, bg='azure', height=320, width=600)
    middle_frame2.pack(fill=BOTH, expand=True)
    label = Label(top_frame2, text="Your watchList", font="Arial 15 bold", fg='white', bg = 'coral')
    label.pack(side = 'bottom')

    #connection to the database to get the movies of the user
    con = connect()
    cur = con.cursor()
    query = ("""
                SELECT s.title, s.type, s.release_year, s.description,  us.last_update, s.show_id AS 'DATEADDED' FROM users_shows us JOIN shows s ON us.show_id = s.show_id WHERE us.user_name = '{}';
                """).format(user_name)
    cur.execute(query)
    rows = cur.fetchall()
    con.close()

    ##Just show the movies and maybe an option to delete it out of the database
    def update(rows):
        for i in rows:
            trv2.insert('', 'end', values=i)
    def selectItem(a):
        # print(trv)
        curItem = trv2.focus()
        #print (trv2.item(curItem)['values'])

        try:
            connection = connect()
            cur = connection.cursor()
            query = "DELETE FROM users_shows WHERE user_name = '{}' AND show_id = '{}';".format(user_name,
                                                                                 (trv2.item(curItem)['values'])[5])
            cur.execute(query)
            connection.commit()
            connection.close()
            MessageBox.showinfo("Movie/Show deleted", "The movie is not longer on your watchList!")
        except mysql.connector.errors.IntegrityError:
            print("movie is already deleted")
            MessageBox.showinfo("Warning", "Reload your watchlist")

    global trv2
    trv2 = ttk.Treeview(middle_frame2, columns=(1, 2, 3, 4, 5, 6), show="headings", height="28")
    trv2.pack(side='left', expand=True, fill='both')
    trv2.heading(1, text="Title")
    trv2.heading(2, text="Type")
    trv2.heading(3, text="Release Year")
    trv2.heading(4, text="Description")
    trv2.heading(5, text="Date added")
    trv2.column("1", minwidth=0, width=150, anchor='c')
    trv2.column("2", minwidth=0, width=60, anchor='c')
    trv2.column("3", minwidth=0, width=60, anchor='c')
    trv2.column("4", minwidth=0, width=470, anchor='c')
    trv2.column("5", minwidth=0, width=100, anchor = 'c')
    trv2.column("6", stretch = NO, minwidth=0, width=0, anchor='c')
    trv2.grid_columnconfigure(1, weight=1)
    trv2.grid_columnconfigure(2, weight=1)
    trv2.grid_columnconfigure(3, weight=1)
    trv2.grid_columnconfigure(4, weight=10)
    trv2.grid_columnconfigure(5, weight=1)
    trv2.grid_columnconfigure(6, weight=0)
    update(rows)

    button = ttk.Button(top_frame2, text="Delete movie/show", width=25, command=lambda: selectItem(1))
    button.pack(side=RIGHT, pady=10, padx=5)


var1 = StringVar()
var2 = StringVar()
genre = ["Every genre"]

#standard testUser
#user_name = "admin"
#user_name = User


#variable getvalues
getFilterValues()

top_frame = Frame(front_end_window, bd=5, height = 300, width = 1000)
#top_frame.place(relwidth=1, relheight= 0.20, relx=0.5, rely=0.1, anchor=CENTER)
#top_frame.columnconfigure(0, weight=3)
top_frame.pack(side = TOP)

middle_frame = Frame(front_end_window, bg="#80c1ff", bd=5, height = 600, width = 1000)
#middle_frame.place(relwidth=1, relheight= 0.70, relx=0.5, rely=0.20, anchor=N)
middle_frame.pack(fill = "both", expand = True)

bottom_frame = Frame(front_end_window, height = 100, width = 1000)
bottom_frame.pack(fill = X, side = BOTTOM)


label=Label(top_frame, text="Full List of Movies and TV Shows on Netflix", font="Arial 15 bold", fg='red2')
label.grid(row=0,column=1,sticky="nsew", columnspan = 5)
label=Label(top_frame, text="Are you wondering what's new – or what's best – on Netflix? \n NetflixSurfer is an application for video streaming services that offers a complete list \n"
                            "of all the movies and TV shows that are currently streaming on Netflix in the U.S.",
            font="Arial 8", fg='red1')
label.grid(row=1,column=1,sticky="nsew",  columnspan = 5)


#entry box to search
inputbox = Entry(top_frame, width=50)
inputbox.grid(row=2,column=5, sticky=W)

search_button = Button(top_frame, text="Search", command=search_now)
search_button.grid(row=2, column=6, padx=10, rowspan = 2)


types = Label(top_frame, text="Enter a topic you want to watch:")
types.grid(row=3, column=4, sticky=W)

topicBox = Entry(top_frame, width=50)
topicBox.grid(row=3,column=5, sticky=W)

addLabel = Label(bottom_frame, text="Add a Movie/Show per double click to your watchlist", font = ("Arial", 10), fg = "red2")
addLabel.pack(side = LEFT)

#drop box
drop = ttk.Combobox(top_frame, value=["Actor", "Director"])
drop.current(0)
drop.grid(row=2, column=4)

#checkbox
movie = Checkbutton(top_frame, text="Movie", variable=var1)
movie.grid(row=2, column=2, sticky=W)
movie.select()
tv_show = Checkbutton(top_frame, text="TV Shows", variable=var2)
tv_show.grid(row=2, column=3, sticky=W)
tv_show.select()

types = Label(top_frame, text="Type:")
types.grid(row=2, column=1, sticky=W)

# leave outside row + columns empty to centre
top_frame.grid_columnconfigure(0, weight=1)
top_frame.grid_columnconfigure(8, weight=1)

#OptionMenu
genreSelected = StringVar(top_frame)
genreSelected.set(genre[0]) # default value

w2 = OptionMenu(top_frame, genreSelected, *genre)
w2.grid(row=3, column = 2, pady = 5, columnspan = 2)
label_w2 = Label(top_frame, text="Genre:")
label_w2.grid(row=3, column=1, sticky=W, pady = 5)

#update
update_button = Button(top_frame, text="Update List", command=update_list)
#update_button.grid(row=2, column=1, padx=10, pady=10, sticky=W)




btn_Clear = Button(bottom_frame, text = "Clear", width = 20, command = clearFrame)
btn_Clear.pack(side = RIGHT, pady = 10, padx = 5)

myList = Button(bottom_frame, text = "Go to your WatchList", width = 20, command = openWindow)
myList.pack(side = RIGHT, pady = 10, padx = 5)

logout = Button(top_frame, text='Logout ',
                fg='white', bg='red',
                activebackground='blue',
                width=13, height=1, command=logout, compound=RIGHT)
logout.grid(row = 0, column = 7, sticky = E)

#defaultButton = ttk.Button(bottom_frame, text="Add watchlist", width=20)
#defaultButton.pack(side=RIGHT, pady=10, padx=5)

defaultButton = ttk.Button(bottom_frame, text="Add watchlist", width=20, command=lambda: addWatchlist(1))
defaultButton.pack(side=RIGHT, pady=10, padx=5)

#front_end_window.mainloop()