import os
from app import create_app


config = os.getenv('APP_SETTINGS')

application = create_app(config)

if __name__ == '__main__':
    application.run()
