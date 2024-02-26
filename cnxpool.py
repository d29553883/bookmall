
from mysql.connector import pooling
import os
from dotenv import load_dotenv

load_dotenv()

password = os.getenv("PASSWORD")
host = os.getenv("Endpoint")

dbconfig={
    "host" : host,
    "user" : "root",
    "password" : password ,                                            
    "database" : "bookmall",
}

cnxpool=pooling.MySQLConnectionPool(
    pool_name = "mypool",
    pool_size = 30,
    **dbconfig
)