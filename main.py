import mysql.connector
import getpass

def connect_to_db():
    return mysql.connector.connect(
    host="localhost",
    user="root",
    password="database4thewin",
    database="sys"
    )

def new_password():
    site = input("Enter site name: ")
    username = input("Enter username: ")
    #password = input("Enter password: ")
    password = getpass.getpass(prompt = "Enter password: ")

    save_to_database(site, username, password)

def get_password():
    site = input("Enter site name: ")
    username,password = get_from_database(site)
    print("Username: ", username)
    print("Password: ", password)

def save_to_database(site, username, password):
    mydb = connect_to_db()
    print(site, username, password)
    mycursor = mydb.cursor()

    sql = "INSERT INTO passwords (site, username, password) VALUES (%s, %s, %s)"
    val = (site, username, password)
    mycursor.execute(sql, val)

    mydb.commit()

    print(mycursor.rowcount, "record inserted.")

def get_from_database(site):
    mydb = connect_to_db()
    print(site)

    mycursor = mydb.cursor()

    sql = "SELECT username, password FROM passwords WHERE site = %(site)s"
    mycursor.execute(sql, { 'site': site })

    myresult = mycursor.fetchall()

    return myresult[0][0],myresult[0][1]


def handle_master_password():
    correct = False
    while not correct:
        try:
            p = getpass.getpass(prompt = "Master Password: ")
        except Exception as error:
            print('ERROR', error)
        else:
            if p == "hello":
                correct = True
            else:
                print("Password Incorrect")

def main():
    connect_to_db()
    print("Hello, welcome to password manager")
    # enter master password
    handle_master_password()

    # options
    # 1. Make new password
    # 2. Get a password
    # 3. Exit
    done = False
    while(not done):
        print("Here are your options: ")
        print("1. Make new password")
        print("2. Get a password")
        print("3. Exit")
        i = input("")
        if i == "1":
            new_password()
        elif i == "2":
            get_password()
        elif i == "3":
            done = True
            print("Goodbye")
        else:
            print("Invalid input")

main()
