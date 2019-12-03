
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True,
                        help="username field cannot be left blank")
    parser.add_argument('password', type=str, required=True,
                        help='password field cannot be left blank')

    def post(self):

        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'Message': 'User already exist'}, 400

        else:

            user = UserModel(**data)
            user.save_to_db()
            return {'Message': 'User created successfully!!'}, 201
