import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from routes.offer_routes import offer_blueprint
from routes.lead_routes import lead_blueprint
from routes.score_routes import score_blueprint
from config import Config
from database_manager import DatabaseManager



def CreateServer():
    #creating a flask server
    app = Flask(__name__)
    
    app.logger.setLevel(logging.DEBUG)
    app.logger.info("flask application created")

    #loading configuration
    app.config.from_object(Config)
    app.logger.info("app configuration loaded")


    #initializing database
    db_manager = DatabaseManager(app.config['DATABASE_URL'])
    db_manager.initialize_database()

    #registering routes to the server
    app.register_blueprint(offer_blueprint)
    app.register_blueprint(lead_blueprint)
    app.register_blueprint(score_blueprint)
    app.logger.info("routes registered with the server")

    return app


if __name__=="__main__":
    app = CreateServer()
    port = int(os.environ.get("PORT", 5000))  # fallback to 5000 for local dev
    app.run(debug=False, host="0.0.0.0", port=port)
