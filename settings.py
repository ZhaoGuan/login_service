from pathlib import Path
from common.utils import make_dir

BASE_DIR = Path(__file__).resolve().parent
TEMP_DIR = BASE_DIR / "temp"
TEMPLATES = BASE_DIR / "templates"
make_dir(TEMP_DIR)

LOCAL = False
ENV = "MYSQL"

# local MYSQL
# MYSQL_HOST = "localhost"
# MYSQL_PORT = "3306"
# MYSQL_USER = "root"
# MYSQL_PASSWORD = "gz19891020"
# MYSQL_DB = "qa_login"
SECRET = "good good study day day up"
FULL_REDIRECT_PATH = "https://login.qa.lingo-ace.com/oauth"
# FULL_REDIRECT_PATH = "http://localhost:8001/oauth"
