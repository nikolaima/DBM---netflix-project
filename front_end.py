from tkinter import *
import random
import mysql.connector
import pprint
from tkinter import ttk

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

front_end_window=Tk()
front_end_window.title("NetflixSurfer - What Should I Watch?")
front_end_window.geometry("1000x800")

#creating a cursor and initializing it
#my_cursor = db.cursor()


#Create Table

#update list
def update_list():
    pass


trv = ttk.Treeview()
def display(query):
    def update(rows):
        for i in rows:
            trv.insert('', 'end', values=i)

    clearFrame()
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


def selectItem():
    print(trv)
    curItem = trv.focus()
    print (trv.item(curItem)['values'])


trv.bind("<<TreeviewSelect>>", selectItem) # single click, without "index out of range" error



def clearFrame():
    for widget in middle_frame.winfo_children():
        widget.destroy()
    tv_show.select()
    movie.select()
    topicBox.delete(0, 'end')
    inputbox.delete(0, 'end')


#please wite the query here
list_movies_query=["SELECT title, duration, description FROM shows;", "Viewing Movies"]
list_tv_shows_query=["SELECT title, description FROM shows;", "Viewing TV SHOWS"]

var1 = StringVar()
var2 = StringVar()
genre = ["Every genre"]

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

#list all movie
movie_list_button = Button(top_frame, text="Show All Movies", command=lambda: display(list_movies_query))
#movie_list_button.grid(row=2, column=2, padx=10, pady=10, sticky=W)

tvshow_list_button = Button(top_frame, text="Show All TV Shows", command=lambda: display(list_tv_shows_query))
#tvshow_list_button.grid(row=2, column=3, padx=10, pady=10, sticky=W)

btn_Clear = Button(bottom_frame, text = "Clear", width = 15, command = clearFrame)
btn_Clear.pack(side = RIGHT, pady = 10, padx = 5)

btn_Clear = Button(bottom_frame, text = "Add to my list", width = 15, command = selectItem())
btn_Clear.pack(side = RIGHT, pady = 10, padx = 5)

front_end_window.mainloop()