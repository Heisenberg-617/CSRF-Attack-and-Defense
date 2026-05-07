import os
import mysql.connector
from mysql.connector import pooling


def get_db_config():
    return {
        "host": os.environ.get("DATABASE_HOST", "db"),
        "database": os.environ.get("DATABASE_NAME", "csrf_project"),
        "user": os.environ.get("DATABASE_USER", "csrf_user"),
        "password": os.environ.get("DATABASE_PASSWORD", "csrf_pass"),
        "autocommit": True,
    }

_db_pool = None


def init_db_pool(pool_name="csrf_pool", pool_size=5):
    global _db_pool
    if _db_pool is None:
        _db_pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name=pool_name,
            pool_size=pool_size,
            **get_db_config()
        )
    return _db_pool


def get_db_connection():
    pool = init_db_pool()
    return pool.get_connection()
