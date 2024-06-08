import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

# load environment variables from a .env file
load_dotenv()

# instantiate the extensions
db = SQLAlchemy() # initialize the SQLAlchemy extension
migrate = Migrate() # initialize the Flask-Migrate extension

# function to create and configure the Flask application
def create_app(script_info=None):

    # instantiate the Flask app
    app = Flask(__name__)
    cors = CORS(app) # enable cross-origin resource sharing (CORS) for the app

    # set configurations from environment variables
    app_settings = os.getenv('APP_SETTINGS') # get the app settings from environment variables
    app.config.from_object(app_settings) # load the configuration into the app
    app.config['CORS_HEADERS'] = 'Content-Type' # set the CORS headers

    # set up extensions
    db.init_app(app) # initialize SQLAlchemy with the app
    migrate.init_app(app, db) # initialize Flask-Migration with the app and database

    # register blueprints for the application
    from .views.views import views
    from .api.api import api

    app.register_blueprint(views) # register the views blueprint
    app.register_blueprint(api) # register the api blueprint

    # error handler for 400 bad request
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({
            "status":"error",
            "error":e.description
        }), 400

    # error handler for 404 not found
    @app.errorhandler(404)
    def not_found_error(e):
        return jsonify({
            "status":"error",
            "error":e.description
        }), 404

    # error handler for 500 internal server error
    @app.errorhandler(500)
    def server_error(e):
        return jsonify({
            "status":"error",
            "error":"this wasn't suppose to happen"
        })

    # shell context for Flask CLI
    @app.shell_context_processor
    def ctx():
        # return the application and database to the shell context
        return {'app': app, 'db': db}
    
    return app # return the configured Flask application