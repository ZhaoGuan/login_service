from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

LOCAL = False
ENV = "MYSQL"

# local MYSQL
MYSQL_HOST = "localhost"
MYSQL_PORT = "3306"
MYSQL_USER = "root"
MYSQL_PASSWORD = "12345678"
MYSQL_DB = "qa_login"
SECRET = "good good study day day up"
FULL_REDIRECT_PATH = "http://localhost:8000/oauth"
