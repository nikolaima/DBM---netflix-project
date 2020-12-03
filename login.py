import tkinter as tk
import mysql.connector as mysql
from tkinter import *
import tkinter.messagebox as MessageBox
import hashlib
import PIL

userID = 'urEmailDomain'
home = 'UrHomeWindow'

def logout2():
    global home
    home.withdraw()
    root.deiconify()
    print("Logged out Sucessfully...")

def login():
    global userID
    try:
        connection = mysql.connect(host="localhost", user="root", passwd="1fcn", database='dbm_netflix_project')#
    except:
        print("You are not connected to server(localhost)")
    else:
        print('Connected Successfully')
        print('Enter ur Email and password')
        User = EntryUser.get()
        Password = EntryPass.get()
        # encoding Password using encode()
        # then sending to SHA1()
        Password = hashlib.sha1(Password.encode())
        cur = connection.cursor()
        query = "SELECT user_name, password FROM users"
        cur.execute(query)
        login = False
        for (user, pas) in cur:
            if User == user and Password.hexdigest() ==pas:
                login = True
                break
            else:
                login = False
        if login == True:
            print("Logged in succesfully as", User)
            newWindow()
        else:
            MessageBox.showinfo("Wrong User or Password", "Please try it again")

def createAccount():
    global userID
    login = False
    try:
        connection = mysql.connect(host="localhost", user="root", passwd="1fcn", database='dbm_netflix_project')#
    except:
        print("You are not connected to server(localhost)")
    else:
        Email = EntryUser.get()
        Password = EntryPass.get()
        cur = connection.cursor()
        try:
            query = "INSERT into users VALUES ('{}', sha1('{}'));".format(Email, Password)
            cur.execute(query)
            connection.commit()
            connection.close()
            login = True
            MessageBox.showinfo("Registration succesfull", "Hello " + Email + "! \n\nYou are now a new user of our website. Have fun and we are hoping that you will find many new Netflix shows")
        except mysql.connection.errors.IntegrityError:
            print("username already exists")
            MessageBox.showinfo("Warning", "The username already exists. Please use a different username")

        else:

            userID = (Email.split('@')[0])
            if login == True:
                print("Logged in succesfully as", userID)
                newWindow()

def newWindow():
    global userID, home
    root.withdraw() #CLOSE THE LOGIN WINDOW
    #open new window ==========================================
    home = Toplevel(root)
    home.title('Main Window')
    home.geometry('500x600')
    home.config(bg = 'azure')
    something = Label(home, text="You are logged in SuccessFully\n".format(userID),
                      fg='green', bg='azure')
    something.place(x=120, y = 20)
    logout = Button(home, text='Logout ', #image = lo,
                    fg = 'white', bg = 'red',
                    activebackground = 'blue',
                    width = 13, height = 1, command = logout2, compound = LEFT)
    logout.pack(anchor = 'se')
    #home.mainloop()

#root window
root = Tk()
root.config(bg = 'blue')
root.title('Login Window')
root.geometry('520x380')
root.resizable(0,0)
image = PhotoImage(file='bg.png')
#root.wm_iconbitmap('icon.ico')
#login & logout image =========================
#li = PhotoImage(file='login.png')
#lo = PhotoImage(file='logout.png')
#=============================================
bgLabel = Label(root, image = image)
bgLabel.place(x=-4, y = 0)

#login System
site = Label(root, text = 'Login to "What should I watch at Netflix"',
             font = ('arial', 15, 'bold', 'underline'), fg='blue3')
site.place(x=80, y = 120)
#Username
username = Label(root, text="Username: ", font=('arial', 10, 'bold'),
                 fg = 'blue').place(x=120, y = 180)
EntryUser = Entry(root, width = 30, font = ('calibri', 12), highlightbackground = 'blue',
             highlightthickness=1)
EntryUser.place(x=200, y = 180)
#Password
password = Label(root, text = "Password: ", font=('arial', 10, 'bold'),
                 fg = 'blue').place(x=120, y = 230)
EntryPass = Entry(root, width = 30, font = ('calibri', 12), highlightbackground ='blue',
             highlightthickness = 1)
EntryPass.place(x=200, y=230)
#SUBMIT
submit = Button(root, text = ' Login ',#image = li,
                fg ='white', bg = 'green', activebackground = 'blue',
                width = 15, height =1, command = login, compound = LEFT)
submit.place(x=160, y = 280)

submit = Button(root, text = ' Create an account ',#image = li,
                fg ='white', bg = 'red', activebackground = 'blue',
                width = 15, height =1, command = createAccount, compound = LEFT)
submit.place(x=290, y = 280)

#close looop
root.mainloop()