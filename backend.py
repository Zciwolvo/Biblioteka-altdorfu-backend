from flask import Flask, render_template
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from routes import auth, user, character
import secrets
import json

app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_hex(16)
app.config["JWT_SECRET_KEY"] = secrets.token_hex(32)
CORS(app)
jwt = JWTManager(app)

bcrypt = Bcrypt(app)

# Register blueprints
app.register_blueprint(auth.auth_blueprint)
app.register_blueprint(user.user_blueprint)
app.register_blueprint(character.character_blueprint)


@app.route("/classes")
def display_json():
    try:
        with open("./src/data/classes_mod.json", "r", encoding="utf-8") as json_file:
            classes = json.load(json_file)
        with open("./src/data/data_bkp.json", "r", encoding="utf-8") as json_file:
            spells = json.load(json_file)
        with open("./src/data/weapons_mod.json", "r", encoding="utf-8") as json_file:
            weapons = json.load(json_file)
    except FileNotFoundError:
        classes, spells, weapons = [], [], []

    return render_template(
        "dataset.html", classes=classes, spells=spells, weapons=weapons
    )


if __name__ == "__main__":
    app.run(debug=True)
