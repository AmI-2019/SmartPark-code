#   Structure of the table "table"
#
#   username: varchar(255)
#   password: varchar(255)
#   plate: varchar(7)  PRIMARY KEY
#   preference: integer
#
#File that contains the functions that interact with the database

import pymysql
import re

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
    #result is a tuple of tuples
    return result[0]

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

# Insertion of a new user
# Return values:
#  0 -> Successful insertion
#  1 -> Plate already taken
#  2 -> Username already taken
#  3 -> Plate field empty
#  4 -> Username field empty
#  5 -> Password field empty
# Preference is an integer
def newUser(username, password, plate, preference):
    #Error if the plate field is empty
    if(plate==""):
        return 3

    #Error if the username field is empty
    if (username == ""):
        return 4

    #Error if the password field is empty
    if (password == ""):
        return 5

    #Error if the palte is already taken
    if(showUserFromPlate(plate)!=-1):
        return 1

    # Error if the username is already taken
    if (showUserFromUsername(username) != -1):
        return 2

    conn = openConnection()
    cursor=conn.cursor()
    sql="insert into " + table + "(username, password, plate, preference) values(%s, %s, %s, %s)"
    cursor.execute(sql, (username, password, plate, preference))
    conn.commit()
    cursor.close()
    conn.close()

    #Successful insertion
    return 0