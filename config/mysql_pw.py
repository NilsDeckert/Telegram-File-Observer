import mysql.connector
from mysql.connector import errorcode
login = mysql.connector.connect(         #MySQL login details
        host="HOST_ADDRESS", #eg localhost
        port="3306",
        user="MYSQL_USER",
        passwd="USERS_PASSWORD",
        database="DATABASE_NAME"
)
