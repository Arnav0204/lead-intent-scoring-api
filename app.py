import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from routes.offer_routes import offer_blueprint
from routes.lead_routes import lead_blueprint
from routes.score_routes import score_blueprint



def CreateServer():
    #creating a flask server
    app = Flask(__name__)
    
    app.logger.setLevel(logging.DEBUG)

    app.logger.info("flask application created")

    #registering routes to the server
    app.register_blueprint(offer_blueprint)
    app.register_blueprint(lead_blueprint)
    app.register_blueprint(score_blueprint)
    app.logger.info("routes registered with the server")

    return app


if __name__=="__main__":
    app = CreateServer()
    app.run(debug=True)
