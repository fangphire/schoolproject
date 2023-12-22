import mysql.connector as sqltor

print("------------MyDrug Store-----------")


mydb = sqltor.connect(host="localhost", user="root", passwd = "1234" )
mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS db1")
mycursor.execute("USE db1")
mycursor.execute("CREATE TABLE IF NOT EXISTS login(Username varchar(25) NOT NULL, password varchar(20) NOT NULL)")
mycursor.execute("CREATE TABLE IF NOT EXISTS purchase(CustName varchar(25) NOT NULL, ProdName varchar(25), Amount int NOT NULL, Quantity int NOT NULL)")
mycursor.execute("CREATE TABLE IF NOT EXISTS inventory(Name varchar(25) NOT NULL, Price INT NOT NULL, Quantity INT NOT NULL, ExpDate DATE NOT NULL)")
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

    userInp =int(input("Enter your choice: "))


# Making a function to display the page when the owner logs in    
    def OwnerPage():
        print('''1. Add \n2. Update \n3. Delete \n4. Display all \n5. Change password \n6. Log out \n
                 ''')
        ownerInp = int(input("Enter your choice: "))

        if ownerInp == 1:
            loop = "y"
            while loop == 'y':
                name = input("Enter product name: ")
                price = int(input("Enter price of product: "))
                quantity = int(input("Enter quantity of product: "))
                expdate = input("Enter expiry date of product: ")
                sql = "INSERT INTO inventory (Name, Price, Quantity, ExpDate) VALUES (%s, %s, %s, %s)"
                values = (name, price, quantity, expdate)

#Using a placeholder to insert values into the table as other methods would result in a error
            
                mycursor.execute(sql, values)
                mydb.commit()
                print("Record successfully updated")
                loop = input("Do you want to continue adding products? (y/n): ")

        elif ownerInp == 2: 
            loop = "y"
            while loop == 'y':
                    name = input("Enter product name: ")
                    newPrice = int(input("Enter new price: "))
                    sql = "UPDATE inventory SET Price = %s where Name = %s"
                    values = (str(newPrice), name)
                    mycursor.execute(sql ,values)
                    mydb.commit()
                    loop = input("Do you want to continue updating products? (y/n): ")

        elif ownerInp == 3:
            loop = "y"
            while loop == 'y':
                name = input("Enter name of product you want to delete: ")
                sql = ("DELETE FROM inventory WHERE name = %s")
                values = (name)
                mycursor.execute(sql, values)
                mydb.commit()
                loop = input("Do you want to continue deleting products? (y/n): ")

        elif ownerInp == 4:

            mycursor.execute("SELECT * FROM inventory")
            print("Name || Price || Quantity || Expiry Date")
            for i in mycursor:
                name, price, quant, exp = i
                print(f"{name} || {price} || {quant} || {exp}")


        elif ownerInp == 5:
            newPass = input("Enter new password: ")
            mycursor.execute("UPDATE login SET password ='"+newPass+"'")
            mydb.commit()
        
        elif ownerInp == 6:
            pass



#Making a function to store the customer page

    def CustPage():
        print("1. Purchase \n2. Payment \n3. Shop\n4. Cart \n5. Exit")
        custInp = input("Enter your choice: ")

        if custInp == "1":
            loop = "y"
            while loop == "y":
                amount = 0
                custName = input("Enter your name: ")
                prodName = input("Enter product name: ")
                quant = int(input("Enter quantity: "))
                mycursor.execute("SELECT * FROM inventory")
                for i in mycursor:
                    name, price, quanti, exp = i
                    if prodName == name:
                        amount = quant * price

                    sql = "INSERT INTO purchase values(%s, %s, %s, %s)"
                    values = (custName, prodName, amount, quant)
                    mycursor.execute(sql, values)
                    mydb.commit()

                loop = input("Do you want to continue shopping for products? (y/n): ")


        

        elif custInp == '2':
            purCon = input("Confirm this payment: (y/n)")

            mycursor.execute("SELECT * FROM purchase")
            for i in mycursor:
                name, prod, amount, quanti = i

                mycursor.execute("SELECT * FROM inventory")

                for m in mycursor:
                    pname, price, quant, exp = m

                    if pname == prod:
                        sql = "UPDATE inventory SET quantity = %s WHERE name = %s"
                        values = ((quant - quanti), prod)
                        mycursor.execute(sql, values)
                        mydb.commit()

        elif custInp == '3':
            
            mycursor.execute("SELECT * FROM inventory")
            print("Name || Price || Quantity || Expiry Date")
            for i in mycursor:
                name, price, quant, exp = i
                print(f"{name} || {price} || {quant} || {exp}")


        elif custInp == '4':
            mycursor.execute("SELECT * FROM purchase")
            print("Username || Product Name || Amount || Quantity")
            for i in mycursor:
                uname, prod, amt, qua = i
                print(f"{uname} || {prod} || {amt} || {qua}")


        elif custInp == '5':
            pass



# If admin logging in, matching password in login table with input credentials
            
    if userInp == 1:
        mainLoop = "y"
        userN = input("Enter username: ")
        userPass = input("Enter password: ")
        mycursor.execute("SELECT * FROM login")
        for i in mycursor:
            username, password = i
        if userN == username and userPass == password:
            while mainLoop == "y":
                print("Welcome Owner")
                OwnerPage()

#using a while loop to stay logged in 

                mainLoop = input("Do you wish to stay logged in? (y/n): ")
        else:
            print("Wrong credentials")
    
#For the customer

    elif userInp == 2:
        mainLoop = "y"
        while mainLoop == "y":
            CustPage()
            mainLoop = input("Do you wish to stay logged in? (y/n): ")

#Exiting
        

    elif userInp == 3:
        break