from flask import Flask, render_template
from app.extensions import init_extensions
from app.webhook.routes import webhook_blueprint


def create_app():
    app = Flask(__name__, template_folder='../templates',
                static_folder='../static')

    @app.route('/')
    def index():
        return render_template('index.html')

    # MongoDB configuration
    app.config["MONGO_URI"] = "mongodb://localhost:27017/github_events"

    # Initialize extensions
    init_extensions(app)

    # Register blueprints
    app.register_blueprint(webhook_blueprint)

    return app
