
#database setup
import pymysql
import pymysql.cursors

# create connection object
connection = pymysql.connect(host='localhost',
                            user='user',
                            password='passwd',
                            dbname='dbtest',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)

try:
    # creating new database
    with connection.cursor() as cursor:
        sql = "CREATE DATABASE dbtest"
        cursor.execute(sql)

    # writing to existing database
    with connection.cursor() as cursor:
        # creating new record
        sql = "INSERT INTO 'users' ('email','password') VALUES (%s, %s)"
        cursor.execute(sql, ('webmaster@python.org','very-secret'))

    # commit changes
    connection.commit()

#    with connection.cursor() as cursor:
        # read
#        pass
finally:

    connection.close()

#name,type(psychologist/psychiatrist/therapist),male/female,street_address,city,state,phone,email,hours,remote(y/n),

#better to do columns for each thing? anxiety etc, or one giant text field for all?
