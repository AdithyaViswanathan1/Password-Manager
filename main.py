import mysql.connector
import getpass
import cryptography
from cryptography.fernet import Fernet
import os
import clipboard
import random
from random import randint
import string

def connect_to_db():
    global key
    key = b'JPpBRq-SzOEW_qi1dnIrR6NdiT0kuKJRjuRpzpiLkeo='
    #print(key)
    return mysql.connector.connect(
    host="localhost",
    user="root",
    password="database4thewin",
    database="sys"
    )

def auto_generate_password():
    length = randint(8, 15)
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    result_str += str(random.randint(0,1000))
    print("Password of length", len(result_str), "is:", result_str)
    return result_str

def new_password():
    site = input("Enter site name: ")
    username = input("Enter username: ")

    auto_gen = input("Would you like a password to be auto-generated for you? (Y/N) ")
    if auto_gen.lower() == "y" or auto_gen.lower() == "yes":
        # auto-generate a password
        password = auto_generate_password()
    else:
        password = getpass.getpass(prompt = "Choose a password: ")


    save_to_database(site, username, password)

def get_password():
    site = input("Enter site name: ")
    username,password = get_from_database(site)
    print("Username: ", username)
    print("Password: ", password)
    clipboard.copy(password)
    print("Password copied to clipboard!")

def remove_password():
    site = input("For which site would you like to remove your password for? ")
    deleted = delete_from_database(site)
    if deleted > 0:
        print("Password for", site, "deleted")
    else:
        print("Site not found in database. Try again!")

def save_to_database(site, username, password):
    mydb = connect_to_db()
    cipher_suite = Fernet(key)
    ciphered_text = cipher_suite.encrypt(str.encode(password))   #required to be bytes
    #print(ciphered_text)
    #print(site, username, ciphered_text)
    mycursor = mydb.cursor()

    sql = "INSERT INTO passwords (site, username, password) VALUES (%s, %s, %s)"
    val = (site, username, ciphered_text)
    mycursor.execute(sql, val)

    mydb.commit()

    print(mycursor.rowcount, "record inserted.")

def get_from_database(site):
    mydb = connect_to_db()
    #print(site)

    mycursor = mydb.cursor()

    sql = "SELECT username, password FROM passwords WHERE site = %(site)s"
    mycursor.execute(sql, { 'site': site })

    myresult = mycursor.fetchall()

    cipher_suite = Fernet(key)
    ciphered_text = myresult[0][1]
    unciphered_text = (cipher_suite.decrypt(bytes(ciphered_text, 'utf-8')))
    #print(unciphered_text)

    return myresult[0][0],unciphered_text.decode()

def delete_from_database(site):
    mydb = connect_to_db()

    mycursor = mydb.cursor()

    sql = "DELETE FROM passwords WHERE site = %(site)s"
    mycursor.execute(sql, { 'site': site })
    mydb.commit()

    return mycursor.rowcount

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
        print("1. New password")
        print("2. Get password")
        print("3. Remove password")
        print("4. Clear Terminal")
        print("5. Exit")

        i = input("What would you like to do? ")
        if i == "1":
            new_password()
        elif i == "2":
            get_password()
        elif i == "3":
            remove_password()
        elif i == "4":
            os.system('clear')
        elif i == "5":
            done = True
            print("Goodbye")
        else:
            print("Invalid input")

main()
