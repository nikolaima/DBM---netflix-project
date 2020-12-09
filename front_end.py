from tkinter import *
import random
import mysql.connector
import pprint
from tkinter import ttk

def search_now():
    #default filter
    print("{}, {}, {}, {}".format(var1.get(), var2.get(), drop.get(), inputbox.get()))
    my_query=["SELECT title, type, duration, description FROM shows LIMIT 50;", "Viewing Rentals"]

    '''
    
    if var1==True and var2==True:
        checkbox_val=""
    '''

    #print(filter)
    print(my_query)
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
front_end_window.title("Return Rental")
front_end_window.geometry("1000x800")

#creating a cursor and initializing it
#my_cursor = db.cursor()


#Create Table

#update list
def update_list():
    pass


def display(query):
    x = connect()
    c = x.cursor()
    c.execute(query[0])
    result = c.fetchall()

    # Label in top row
    t=1
    columns = c.column_names
    print(columns)
    label = Label(middle_frame, text=query[1])
    label.grid(row=0, column=2)
    #create column names
    for i in range(len(columns)):
        e = Entry(middle_frame, width=20, fg='blue')
        e.grid(row=1, column=i)
        e.insert(END, columns[i])

    for i in range(len(result)):
        for j in range(len(columns)):
            e = Entry(middle_frame, width=20, fg='blue')
            e.grid(row=i+2, column=j)
            e.insert(END, result[i][j])
    x.close()

#please wite the query here
list_movies_query=["SELECT title, duration, description FROM shows;", "Viewing Movies"]
list_tv_shows_query=["SELECT title, duration, description FROM shows;", "Viewing TV SHOWS"]
    
var1 = StringVar()
var2 = StringVar()
genre = ["Every genre"]

#variable getvalues
getFilterValues()

top_frame = Frame(front_end_window, bd=5)
top_frame.place(relwidth=1, relheight= 0.20, relx=0.5, rely=0.1, anchor=CENTER)
#top_frame.columnconfigure(0, weight=3)
label=Label(top_frame, text="Full List of Movies and TV Shows on Netflix", font="Arial 15 bold", fg='blue3')
label.grid(row=0,column=1, sticky=N, columnspan = 100)
label=Label(top_frame, text="Are you wondering what's new – or what's best – on Netflix? \n Flixable is a search engine for video streaming services that offers a complete list \n"
                            "of all the movies and TV shows that are currently streaming on Netflix in the U.S.",
            font="Arial 8", fg='blue3')
label.grid(row=1,column=1, sticky=N, columnspan = 100)


#entry box to search
inputbox = Entry(top_frame, width=50)
inputbox.grid(row=2,column=5, sticky=W)

search_button = Button(top_frame, text="Search", command=search_now)
search_button.grid(row=2, column=6, padx=10)


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

#OptionMenu
variable2 = StringVar(top_frame)
variable2.set(genre[0]) # default value

w2 = OptionMenu(top_frame, variable2, *genre)
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

middle_frame = Frame(front_end_window, bg="#80c1ff", bd=5)
middle_frame.place(relwidth=1, relheight= 0.70, relx=0.5, rely=0.20, anchor=N)



front_end_window.mainloop()