import pandas as pd
import sqlite3

# Replace these with your file and database names
excel_file = "ex.xlsx"
database_file = "db.sqlite3"

# Load data from Excel into a DataFrame
df = pd.read_excel(excel_file)

# Establish a connection to the SQLite database
conn = sqlite3.connect(database_file)

# Create a cursor object to interact with the database
cursor = conn.cursor()
i = 1-1

# Insert data into the SQLite database
for index, row in df.iterrows():
    fname = str(row['Nom']) if row['Nom'] != 'None' else ""
    lname = str(row['Prenom']) if row['Prenom'] != 'None' else ""
    cin = str(row["CIN"]) if row["CIN"] != 'None' else ""
    cne = str(row['CNE']) if row['CNE'] != 'None' else ""
    info = str(row['INFO']) if row['INFO'] != 'None' else ""
    email = str(row['email']) if row['email'] != 'None' else ""
    if '@' in email:
        pass
    else:
        email=''
    
    insert_query = "INSERT INTO myapp_person (fname,lname,cin,cen,info, email,ismale,bday,phone) VALUES (?, ?,?,?,?,?,?,?,?)"
    try:
        cursor.execute(insert_query, (fname, lname,cin,cne,info,email,1,"",""))
    except Exception:
        i += 1
    print(fname,' saved successfully')

print(i)
# Commit the changes and close the connection
conn.commit()
conn.close()

print("Data transferred to SQLite database successfully.")
