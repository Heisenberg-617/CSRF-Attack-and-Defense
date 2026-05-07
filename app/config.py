import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "replace_with_a_long_random_value")
    DATABASE_HOST = os.environ.get("DATABASE_HOST", "db")
    DATABASE_NAME = os.environ.get("DATABASE_NAME", "csrf_project")
    DATABASE_USER = os.environ.get("DATABASE_USER", "csrf_user")
    DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD", "csrf_pass")
