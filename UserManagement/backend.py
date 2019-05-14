#   Structure of the table "users"
#
#   username: varchar(255) PRIMARY KEY
#   password: varchar(255)
#   plate: varchar(7) [A-Z]{2}[0-9]{3}[A-Z]{2}
#   preference: integer
#
#File that contains the functions that interact with the database


import pymysql

#Information about the specific system hosting the server
#BEGIN OF MODIFIABLE AREA
def openConnection():
    return pymysql.connect(user='root', password='root',
                           host='localhost', database='')
table = "smartpark_usermanagement.users"
#END OF MODIFIABLE AREA

#Returns plate number and preference of a user given their username, -1 if it doesn't exist
def showUserFromUsername(username):
    conn = openConnection()
    cursor=conn.cursor()
    sql="select plate, preference from " + table + " where username=%s"
    cursor.execute(sql, (username,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    if len(result)==0:
        return -1
    return result

#Returns plate number and preference of a user, given their username, -1 if it doesn't exist
def showPassword(username):
    conn = openConnection()
    cursor=conn.cursor()
    sql="select password from " + table + " where username=%s"
    cursor.execute(sql, (username,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    if len(result)==0:
        return -1
    #resut is a tuple of tuples
    return result[0][0]

#Returns username and preference of a user given their plate number, -1 if it doesn't exist
def showUserFromPlate(plate):
    conn = openConnection()
    cursor=conn.cursor()
    sql="select username, preference from " + table + " where plate=%s"
    cursor.execute(sql, (plate,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    if len(result)==0:
        return -1
    # resut is a tuple of tuples
    return result[0]