from pathlib import Path
import ast
from dotenv import load_dotenv

load_dotenv()
import os

cwd = Path().cwd()

user = os.getenv('user')
password = os.getenv('password')
