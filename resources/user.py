from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required, get_jwt_identity,
    jwt_refresh_token_required, get_raw_jwt, fresh_jwt_required
)
from models.user import UserModel
from blacklist import BLACKLIST

_parser = reqparse.RequestParser()
_parser.add_argument('username', type=str, required=True)
_parser.add_argument('password', type=str, required=True)


class UserRegister(Resource):
    def post(self):
        _parser.add_argument('email', type=str, required=True)
        data = _parser.parse_args()
        _parser.remove_argument('email')
        if UserModel.find_by_username(data['username']):
            return {'msg': 'Username already in use'}, 400
        if UserModel.find_by_email(data['email']):
            return {'msg': 'Email already in use'}, 400
        user = UserModel(**data)
        user.save()
        return {'msg': 'User created successfully'}, 201


class User(Resource):
    @fresh_jwt_required
    def get(self):
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'msg': 'User not found'}, 404
        return user.json()

    @fresh_jwt_required
    def delete(self):
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'msg': 'User not found'}, 404
        user.delete()
        return {'msg': 'User deleted'}, 200


class UserLogin(Resource):
    def post(self):
        data = _parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        return {'msg': 'Invalid credentials'}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {'msg': 'Successfully logged out'}, 200


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        user_id = get_jwt_identity()
        access_token = create_access_token(identity=user_id, fresh=False)
        return {'access_token': access_token}, 200
