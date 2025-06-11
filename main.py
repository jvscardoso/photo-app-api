from flask import Flask
from api.routes.auth import auth_bp 
from api.routes.user import user_bp
from api.routes.photos import photo_bp

app = Flask(__name__)

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(user_bp, url_prefix="/users")
app.register_blueprint(photo_bp, url_prefix="/photos")

@app.route("/")
def index():
    return "API online"