import sqlite3

#TO_DO
#Check for possibelities of sql injections!
#Make try except statement
#Check for data validity
#Add 'where' statements in CRUD
#Probably function for cleaning table_name and such from possible sql injection
#END_TO_DO

#region Work_with_connection

def create_or_connect_to_db(db_name: str):
    db = sqlite3.connect(db_name)
    return db

def close_connection(db: sqlite3.Connection):
    db.close()
    # try:
    #     db.close()
    # except Exception as e:
    #     print("Something went wrong"+'\n'+str(e))

def update_db(db: sqlite3.Connection):
    db.commit()

def create_cursor(db: sqlite3.Connection):
    cur = db.cursor()
    return cur

def delete_cursor(cur: sqlite3.Cursor):
    cur.close()

#endregion


#region Work_with_tables

#CREATE IF NOT EXISTS?
def create_table(db: sqlite3.Connection, cur: sqlite3.Cursor, table_name: str, fields:list):
    cur.execute("""CREATE TABLE IF NOT EXISTS {} (
                    id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
                    awaited_request text NOT NULL,
                    module text NOT NULL,
                    command text NOT NULL,
                    last_modified date NOT NULL
                    )
                    """.format(table_name))
    update_db(db)

def delete_table(db: sqlite3.Connection, cur: sqlite3.Cursor, table_name: str):
    cur.execute("""DROP TABLE IF EXISTS {};""".format(table_name))
    update_db(db)

#endregion


#region CRUD

#Create
def insert_into(db: sqlite3.Connection, cur: sqlite3.Cursor, table_name: str, values: list):
    #request, module, command, last_mod
    cur.execute(
                """INSERT INTO {} VALUES (?,?,?,?,?);""".format(table_name),
                (None, values[0], values[1], values[2], values[3])
                )
    update_db(db)

#Read (all)
def read_from(db: sqlite3.Connection, cur: sqlite3.Cursor, table_name: str):
    cur.execute("""SELECT * FROM {};""".format(table_name))
    items = cur.fetchall()
    return items

#Update (by id)
def update_in(db: sqlite3.Connection, cur: sqlite3.Cursor, table_name: str, values: list):
    cur.execute(
    """UPDATE {} SET {} = ? WHERE id = ?;""".format(table_name, values[0]),
    (values[1], values[2]))
    update_db(db)

#Delete
def delete_from(db: sqlite3.Connection, cur: sqlite3.Cursor, table_name: str, values:list):
    cur.execute(
    """ DELETE FROM {}
    WHERE id = {} ;
    """.format(table_name, values[0]))
    update_db(db)

#endregion


