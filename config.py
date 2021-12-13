import os

from dotenv import load_dotenv

# App config
PROJ_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(PROJ_DIR, 'logs')
ERROR_LOG_FILENAME = os.path.join(LOGS_DIR, 'errors.log')
INFO_LOG_FILENAME = os.path.join(LOGS_DIR, 'info.log')

_ENV_FILE = os.path.join(PROJ_DIR, '.env')

if os.path.exists(_ENV_FILE):
    load_dotenv(_ENV_FILE)

# YaConfig
DISK_TOKEN = os.environ.get('DISK_TOKEN', None)
DISK_FOLDER_PATH = os.environ.get('DISK_FOLDER_PATH', None)

# VK configs
GROUP_ID = os.environ.get('GROUP_ID', None)
API_TOKEN = os.environ.get('API_TOKEN', None)
STANDARD_HEADER_IMG_WIDTH = 1590
STANDARD_HEADER_IMG_HEIGHT = 530
