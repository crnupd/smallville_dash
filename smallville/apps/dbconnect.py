import pandas as pd
import psycopg2

def getdblocation():
    db = psycopg2.connect(
        host='localhost', 
        database='smallville', 
        user='postgres', 
        port=5432, 
        password='ie172', 
    )
    return db

def modifyDB(sql, values):
    db = getdblocation()
    cursor = db.cursor()
    cursor.execute(sql, values)
    db.commit()
    db.close()

def getDataFromDB(sql, values, dfcolumns):
    # ARGUMENTS
    # sql -- sql query with placeholders (%s)
    # values -- values for the placeholders

    db = getdblocation()
    cur = db.cursor()
    cur.execute(sql, values)
    rows = pd.DataFrame(cur.fetchall(), columns=dfcolumns)
    db.close()
    return rows

    
    try:
        cur.execute(sql, values)
        rows = pd.DataFrame(cur.fetchall(), columns=[desc[0] for desc in cur.description])
        
        # Print all elements of the DataFrame
        print("Fetched Data:")
        print(rows.to_string(index=False))  # Print DataFrame without index for cleaner output
        
    finally:
        db.close()  # Ensure the database connection is closed even if an error occurs
    
    return rows

# Example usage
if __name__ == "__main__":
    sql_query = "SELECT * FROM student WHERE NOT stud_delete_ind"  # Select all columns
    values = []  # Add any parameters needed for your query

    # Fetch and print data
    data = getDataFromDB(sql_query, values)
