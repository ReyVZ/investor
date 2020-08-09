from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user import (
    User, UserRegister, UserLogin, UserLogout, TokenRefresh
)
from resources.asset import Asset, AssetNew, AssetList
from blacklist import BLACKLIST
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SECRET_KEY'] = 'FUCK'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)


@jwt.token_in_blacklist_loader
def check(token):
    return token['jti'] in BLACKLIST


api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(Asset, '/asset/<int:id>')
api.add_resource(AssetNew, '/asset')
api.add_resource(AssetList, '/assets')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=8080, debug=True)
