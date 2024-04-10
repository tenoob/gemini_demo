#code for db data for sql_chatbot
import sqlite3

connection = sqlite3.connect("demo.db")

#create a cusrsor object 
cursor = connection.cursor()

#create table
table_info = """
Create table Employee(NAME VARCHAR(25),DEPARTMENT VARCHAR(25),
ROLE VARCHAR(25),SALARY INT);
"""

cursor.execute(table_info)

#insert records

cursor.execute('''Insert Into Employee values('Raj','Sales','Manager',20000)''')
cursor.execute('''Insert Into Employee values('Sam','Research','Scientist',25000)''')
cursor.execute('''Insert Into Employee values('Vivek','Manufacture','Engineer',12000)''')
cursor.execute('''Insert Into Employee values('Smite','Sales','Worker',12400)''')
cursor.execute('''Insert Into Employee values('Jinho','Sales','SalesMen',15000)''')

#display all records
print("Inserted records:")
data = cursor.execute('''Select * from Employee''')
for row in data:
    print(row)


#close connection
connection.commit()
connection.close()