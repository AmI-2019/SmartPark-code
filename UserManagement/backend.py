#   Structure of the table "users"
#
#   username: varchar(255) PRIMARY KEY
#   password: varchar(255)
#   plate: varchar(7) [A-Z]{2}[0-9]{3}[A-Z]{2}
#   preference: integer

import pymysql

#Information about the specific system hosting the server
#BEGIN OF MODIFIABLE AREA
def openConnection():
    return pymysql.connect(user='root', password='root',
                           host='localhost', database='')
table = "smartpark_usermanagement.users"
#END OF MODIFIABLE AREA

#Returns plate number and preference of a user, given their username
def showUser(username):
    conn = openConnection()
    cursor=conn.cursor()
    sql="select plate, preference from " + table + " where username=%s"
    cursor.execute(sql, (username,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

"""
    def newUser(new, urgent):
    conn = openConnection()
    sql = "insert into "+table+"(todo, urgent) values (%s, %s)"
    cursor = conn.cursor()
    cursor.execute(sql, (new, urgent))
    conn.commit()
    cursor.close()
    conn.close()
"""