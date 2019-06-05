from flask import Flask, request
from flask_restplus import Api, Resource, fields

from entity_type_storage import EntityTypeStorage

app = Flask(__name__)
api = Api(app)
storage = EntityTypeStorage()

entityModel = api.model('EntityType', {
    'name': fields.String,
    'mechanism': fields.String
})


@api.route('/entitytypes')
class EntitiesApi(Resource):
    def get(self):
        return storage.findAll()

    def post(self):
        entity_type = api.payload
        try:
            storage.create(entity_type)
        except Exception as e:
            return str(e), 422
        return entity_type, 201


@api.route('/entitytypes/<string:entity_type_name>')
class EntityApi(Resource):
    def get(self, entity_type_name):
        entity_type = storage.find(entity_type_name)
        return entity_type


if __name__ == '__main__':
    app.run(debug=True)
