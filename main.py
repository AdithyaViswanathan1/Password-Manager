import mysql.connector

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
    password = input("Enter password: ")
    save_to_database(site, username, password)

def get_password():
    site = input("Enter site name: ")
    get_from_database(site)

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
    print(site)



def main():
    connect_to_db()
    print("Hello, welcome to password manager")
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
