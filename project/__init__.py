from flask import Flask
from flask_mongoengine import MongoEngine
from flask_login import LoginManager

db = MongoEngine()


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "some secret keys"
    app.config["MONGODB_SETTINGS"] = {
        "db": "FLASK_APPLICATION",
        "host": "mongodb://localhost:27017/FLASK_APPLICATION",
    }

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.objects(id=user_id).first()

    from .auth import auth as auth_template

    app.register_blueprint(auth_template)

    from .main import main as main_template

    app.register_blueprint(main_template)

    return app


if __name__ == "__main__":
    create_app().run()
