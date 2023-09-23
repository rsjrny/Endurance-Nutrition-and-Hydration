import sqlite3
import os
import pandas as pd

dbfields = ['Quanity', 'Product', 'Carbs', 'Sodium', 'Calories', 'Caffeine',
            'Water', 'Servings', 'Serving Size', 'Comments']


def empty_table(prod):
    con = connect()
    cur = con.cursor()
    cur.execute("DELETE FROM Product ")
    cur.close()
    con.commit()
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
    return sqlite3.connect(os.getcwd() + r'/Datafiles/RunningNutrition.db')


def ins_rep(inquant=0, inprod='', insod=0, incarb=0, incal=0, inwat=0, inserv=0, insrvt=' ', incaf=0, incom=''):
    # INSERT OR REPLACE INTO data VALUES (NULL, 1, 2, 3);
    con = connect()
    cur = con.cursor()
    cur.execute("INSERT OR REPLACE INTO Product VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                (inquant, inprod, incarb, insod, incal, incaf, inwat, inserv, insrvt, incom))
    cur.close()
    con.commit()
    con.close()


def reset_quantity():
    # INSERT OR REPLACE INTO data VALUES (NULL, 1, 2, 3);
    con = connect()
    cur = con.cursor()
    cur.execute("UPDATE Product SET Quantity = 0")
    cur.close()
    con.commit()
    con.close()


def update_quantity(inprod, inquan):
    con = connect()
    cur = con.cursor()
    cur.execute("UPDATE Product SET Quantity = ? WHERE Product = ?", (inquan, inprod))
    cur.close()
    con.commit()
    con.close()


def searchdb(query):
    # print(query)
    con = connect()
    cur = con.cursor()
    cur.execute(query)
    output = cur.fetchall()
    cur.close()
    con.close()

    return output


def printDB():
    con = connect()
    cur = con.cursor()
    cur.execute("""select * from Product""")
    output = cur.fetchall()
    # print(output)
    for row in output:
        print(row)
    cur.close()
    con.close()


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

