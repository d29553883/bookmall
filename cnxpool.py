
from mysql.connector import pooling
import os
from dotenv import load_dotenv

load_dotenv()

password = os.getenv("PASSWORD")
host = os.getenv("ENDPOINT")

dbconfig={
    "host" : host,
    "user" : "admin",
    "password" : password ,                                            
    "database" : "website",
}

cnxpool=pooling.MySQLConnectionPool(
    pool_name = "mypool",
    pool_size = 30,
    **dbconfig
)