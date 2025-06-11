from flask import Flask
from api.routes.auth import auth_bp 
from api.routes.user import user_bp

app = Flask(__name__)

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(user_bp, url_prefix="/users")


@app.route("/")
def index():
    return "API online"