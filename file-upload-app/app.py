from flask import Flask
from routes.fileRoutes import fileApi;
from database import db
import logging

application = Flask(__name__)

application.register_blueprint(fileApi,
                               url_prefix="/file")  ### Registers a blueprint. All /file  requests will be routed to  fileApi

application.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/fileStores.db"  ## fileStore is SQLITE DB name

application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(application)

with application.app_context():
    db.create_all()

##### Configure Logging ########
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    application.logger.handlers = gunicorn_logger.handlers
    application.logger.setLevel(gunicorn_logger.level)

# Only for development server . will never executes when ran via gunicorn #
if __name__ == "__main__":
    application.run()
