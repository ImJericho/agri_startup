from flask import Blueprint
from controllers.read_controller import readers
from controllers.write_controller import writers
# main blueprint to be registered with application
api = Blueprint('api', __name__)

# register user with api blueprint
api.register_blueprint(readers, url_prefix="/reader")
api.register_blueprint(writers, url_prefix="/writer")
