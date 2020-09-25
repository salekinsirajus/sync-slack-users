"""
Description: initialize/update users manually with this script

Can be used with Celery/crontab to run this on the background

"""

import os

from dotenv import load_dotenv, find_dotenv

from wsgi import create_app
from util import sync_users

load_dotenv(find_dotenv())

cli_app = create_app(os.getenv('APP_SETTINGS'))

from models import User, db
from util import create_user_in_database


access_token = os.getenv('SLACK_ACCESS_TOKEN')
with cli_app.app_context():
    sync_users(cli_app, db, User, access_token)
