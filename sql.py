import sqlite3
import os
import pandas as pd


def save_db_loc(dbloc):
    # dbloc = os.path.dirname(dbloc)

    os.environ['RHN_DBLOC'] = dbloc


def get_db_loc():
    return os.path.join(os.getcwd(), 'DataFiles/RunningNutrition.db')


def empty_table(prod):
    con = connect()
    cur = con.cursor()
    cur.execute("DELETE FROM Product ")
    cur.close()
    con.commit()
    con.close()


def create_products_table():
    con = connect()
    crtb = '''CREATE TABLE "Product" ("Quantity" INTEGER, "Product" TEXT NOT NULL UNIQUE, 
    "Carbs" INTEGER, "Sodium" INTEGER,  "Calories"	INTEGER, "Caffeine"	INTEGER, 
    "Water" INTEGER, "Servings" INTEGER, "Serving Size"	TEXT, 
    "Total Carbs"	INTEGER GENERATED ALWAYS AS ("Quantity" * "Carbs") STORED, 	
    "Total Sodium"	INTEGER GENERATED ALWAYS AS ("Quantity" * "Sodium") STORED,
    "Total Calories"	INTEGER GENERATED ALWAYS AS ("Quantity" * "Calories") STORED, 
    "Comments"	TEXT, 	PRIMARY KEY("Product") ;
    '''
    con.close()


def del_like():
    con = connect()
    cur = con.cursor()
    cur.execute("DELETE FROM Product WHERE Product LIKE 'That%'")
    cur.close()
    con.commit()
    con.close()


def listToString(s):
    str1 = ""
    for ele in s:
        str1 += ele
    return str1


def tableToDF(query):
    con = connect()
    df = pd.read_sql(query, con)
    con.close()
    return df


def dftoSQL(df, table):
    con = connect()
    df.to_sql(table, con, if_exists='replace', index=False)
    con.commit()
    con.close()
    return


def connect():
    db = get_db_loc()

    return sqlite3.connect(db)


def ins_rep(inquant=0, inprod='', insod=0, incarb=0, incal=0, inwat=0, inserv=0, insrvt=' ', incaf=0, incom=''):
    con = connect()
    con.execute("INSERT OR REPLACE INTO Product VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                (inquant, inprod, incarb, insod, incal, incaf, inwat, inserv, insrvt, incom))
    con.commit()
    con.close()


def reset_quantity():
    """
    clear the quantity column for all products

    """
    # INSERT OR REPLACE INTO data VALUES (NULL, 1, 2, 3);
    con = connect()
    con.execute("UPDATE Product SET Quantity = 0")
    con.commit()
    con.close()


def update_quantity(inprod, inquan):
    """
    Update the pruduct with the supplied quantity
    :param inprod: Product name
    :param inquan: desired quantity
    :return:
    """
    # print(datetime.datetime.now(), 'updating table: ', inprod, inquan)
    con = connect()
    con.execute("UPDATE Product SET Quantity = ? WHERE Product = ?", (inquan, inprod))
    con.commit()
    # print("update quan commit done")
    con.close()


def delete_row(inprod):
    """
    Delete a product from the table
    :param inprod: Product name
    :return:
    """
    # print('inprod=', inprod)
    con = connect()
    con.execute("DELETE FROM Product WHERE Product = '" + inprod + "'")
    con.commit()
    # print("update quan commit done")
    con.close()


def searchdb(query):
    """
    search the database using the supplied query
    :param query: ex. SELECT Sodium FROM Product WHERE Product = 'GU Gel'
    :return: list of returned results
    """
    # print(query)
    con = connect()
    cur = con.cursor()
    cur.execute(query)
    output = cur.fetchall()
    cur.close()
    con.close()

    return output


def printDB():
    """
    Print the contents of the Product table
    :return:
    """
    con = connect()
    cur = con.cursor()
    cur.execute("""select * from Product""")
    output = cur.fetchall()
    # print(output)
    for row in output:
        print(row)
    cur.close()
    con.close()


def sum_column(column, query=''):
    con = connect()
    cur = con.cursor()
    if query =='':
        cur.execute("SELECT SUM("+column+") FROM Product")
    else:
        cur.execute(query)
    sum = cur.fetchone()
    cur.close()
    con.close()

    return sum[0]


def sum_water():
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT SUM(Quantity*Water) FROM Product WHERE Water > 0")
    sum = cur.fetchone()
    cur.close()
    con.close()

    return sum[0]


def sum_calories():
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT SUM(Quantity*Calories) FROM Product WHERE Quantity > 0")
    sum = cur.fetchone()
    cur.close()
    con.close()

    return sum[0]


def sum_sodium():
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT SUM(Quantity*Sodium) FROM Product WHERE Quantity > 0")
    sum = cur.fetchone()
    cur.close()
    con.close()

    return sum[0]


# reset_quantity()
# del_like()
# con = connect()
# print(searchdb(con, 'SELECT product from Product'))
# sel = tableToDF("""SELECT * FROM Product""")
# dftoSQL(sel, 'Product2')
# print(sel)
# insert(con, '1', 'test46', 200, 24, 45, 0, 0, 1, '10oz','test one')
# update(con, 22, 180, 'test45')
# printDB(con, 'r')
# con.close()

