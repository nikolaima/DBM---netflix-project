import mysql.connector as mysql
from tkinter import *
import tkinter.messagebox as MessageBox
import hashlib

#connect to db
def connect():
    global db
    db = mysql.connect(host="localhost", user="root", passwd="1fcn", database='dbm_netflix_project', auth_plugin='mysql_native_password', charset='utf8')
    return db

User = ""
def getUser():
    return User

def login():
    global User
    try:
        connection = connect()
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

#function to create a new account
def createAccount():
    global User
    login = False
    try:
        connection = connect()
    except:
        print("You are not connected to server(localhost)")
    else:
        User = EntryUser.get()
        Password = EntryPass.get()
        cur = connection.cursor()
        #checks minimum length password
        if (len(User) == 0 ):
            MessageBox.showinfo("Invalid Username",
                                "Please try it again.")
        elif (len(Password)<5):
            MessageBox.showinfo("Invalid Password",
                                "Please try it again. Password need to have more than 5 characters")
        else:
            try:
                #hash the password and insert into db
                query = "INSERT into users VALUES ('{}', sha1('{}'), NOW());".format(User, Password)
                cur.execute(query)
                connection.commit()
                connection.close()
                login = True
                MessageBox.showinfo("Registration succesfull", "Hello " + User + "! \n\nYou are now a new user of our website. Have fun and we are hoping that you will find your perfect Netflix show")
            except mysql.connection.errors.IntegrityError:
                print("username already exists")
                MessageBox.showinfo("Warning", "The username already exists. Please use a different username")

        if login == True:
            print("Logged in succesfully as", User)
            newWindow()

#open the front_end file and window
def newWindow():
    print("X")
    root.destroy()
    import front_end
    front_end.front_end_window.mainloop()



#=======================================GUI==================================
#root window
root = Tk()
root.config(bg = 'blue')
root.title('Login Window')
root.geometry('520x380')
root.resizable(0,0)
image = PhotoImage(file='bg.png')
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
             highlightthickness = 1, show = '*')
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