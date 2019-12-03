from flask_restful import reqparse, request, Resource
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', required=True, type=float,
                        help='price field cannot be left blank')

    parser.add_argument('store_id', required=True, type=int,
                        help='store_id  field cannot be left blank')

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()

        return {'mesaage': 'Item not found'}, 404

    def post(self, name):

        if ItemModel.find_by_name(name):
            return {'message': 'An item with name {} already exist'.format(name)}, 400

        request_data = Item.parser.parse_args()

        item = ItemModel(name, **request_data)

        try:
            item.save_to_db()
        except:
            return {'message': 'An error occured during item insertion'}, 500

        return item.json(), 201

    def delete(self, name):

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'item was deleted'}

    def put(self, name):

        request_data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            try:

                item = ItemModel(name, **request_data)
                item.save_to_db()

            except:
                return {'message': 'error occured while inserting the item'}, 500

        else:
            item.price = request_data['price']
            item.store_id = request_data['store_id']

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
