import os 
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_API = f"https://api.github.com/users/{GITHUB_USERNAME}/repos"

DOWNLOAD_DIR = "repo_all_branches"
CHECKSUM_FILE = "checksums.json"


START_DATE = datetime(2023, 1, 1)
END_DATE = datetime.today()