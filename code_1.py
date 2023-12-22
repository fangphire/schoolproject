import mysql.connector as sqltor

print("------------MyDrug Store-----------")


mydb = sqltor.connect(host="localhost", user="root", passwd = "1234" )
mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS db1")
mycursor.execute("USE db1")
mycursor.execute("CREATE TABLE IF NOT EXISTS login(Username varchar(25) NOT NULL, password varchar(20) NOT NULL)")
mycursor.execute("CREATE TABLE IF NOT EXISTS purchase(Name varchar(25) NOT NULL, Amount int NOT NULL)")
mycursor.execute("CREATE TABLE IF NOT EXISTS inventory(Name varchar(25) NOT NULL, Price INT NOT NULL, Quantity INT NOT NULL)")
mydb.commit()

#Checking if login table is empty and inserting the valid credentials we want for admin into it if empty

cred = 0
mycursor.execute("SELECT * FROM login")
for i in mycursor:
    cred = cred + 1

if cred == 0:
    mycursor.execute("INSERT INTO login VALUES('owner', '123')")
    mydb.commit()

#Making a while loop to give user the option to select what window to open
    
while True:
    print("1. Admin \n2. Client \n3. Exit")

    userInp = int(input("Enter your choice: "))

#If admin logging in, matching password in login table with input credentials

    if userInp == 1:
        userN = input("Enter username: ")
        userPass = input("Enter password: ")
        mycursor.execute("SELECT * FROM login")
        for i in mycursor:
            username, password = i
        if userN == username and userPass == password:
            print("Welcome Owner")
            print("1. Add \n2. Update Price \n3. Delete \n4. Display \n5. Change password \n6. Log Out ")

            ownerInp = int(input("Enter your choice: "))
        else:
            print("Wrong credentials")

