from datetime import datetime
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    get_jwt_identity, jwt_required
)
from models.asset import AssetModel

_parser = reqparse.RequestParser()
_parser.add_argument('ticker', type=str, required=True)
_parser.add_argument('price', type=float, required=True)
_parser.add_argument('count', type=int, required=True)


class Asset(Resource):
    @jwt_required
    def get(self, id):
        asset = AssetModel.find_by_id(id)
        user_id = get_jwt_identity()
        if asset and asset.user_id == user_id:
            return asset.json()
        return {'msg': 'Asset not found'}, 404

    @jwt_required
    def put(self, id):
        asset = AssetModel.find_by_id(id)
        user_id = get_jwt_identity()
        if not asset or asset.user_id != user_id:
            return {'msg': 'Asset not found.'}, 400
        data = _parser.parse_args()
        asset.ticker = data['ticker']
        asset.price = data['price']
        asset.count = data['count']
        try:
            asset.save()
        except:
            return {'msg': 'An error occured while updating asset.'}, 500
        return {'msg': 'Asset updated successfully.'}, 201

    @jwt_required
    def delete(self, id):
        asset = AssetModel.find_by_id(id)
        user_id = get_jwt_identity()
        if asset and asset.user_id == user_id:
            asset.delete()
            return {'msg': 'Asset deleted'}, 200
        return {'msg': 'Asset not found'}, 404


class AssetNew(Resource):
    @jwt_required
    def post(self):
        data = _parser.parse_args()
        user_id = get_jwt_identity()
        asset = AssetModel(user_id=user_id, **data)
        try:
            asset.save()
        except:
            return {'msg': 'An error occured while creating asset.'}, 500
        return {'msg': 'Asset created successfully.'}, 201


class AssetList(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        if user_id:
            data = AssetModel.find_by_user_id(user_id)
            if data:
                assets = [a.json() for a in data]
                return {'assets': assets}, 200
        return {'msg': 'Assets not found.'}, 404
