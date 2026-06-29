from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from courses.routes import courses_bp
from courses import models
from courses.models import db

migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(courses_bp)

    @app.errorhandler(400)
    def bad_request(error):
        return {"error": "Bad Request"}, 400

    @app.errorhandler(404)
    def not_found(error):
        return {"error": "Resource not found"}, 404

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)