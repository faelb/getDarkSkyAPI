import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="faelb",
    passwd="faelb",
    database="smaroo_db"
)

print(mydb)

myCursor = mydb.cursor()

myCursor.execute("SELECT * FROM temperatur")

fetchresult = myCursor.fetchall()

for x in fetchresult:
    print(x)
