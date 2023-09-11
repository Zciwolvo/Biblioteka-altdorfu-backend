from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from routes import auth, user, character
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['JWT_SECRET_KEY'] = secrets.token_hex(32)
CORS(app)
jwt = JWTManager(app)

bcrypt = Bcrypt(app)

# Register blueprints
app.register_blueprint(auth.auth_blueprint)
app.register_blueprint(user.user_blueprint)
app.register_blueprint(character.character_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
