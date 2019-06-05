from flask import Flask
from flask_restplus import Api, Resource, fields

from entity_type_storage import entity_types as storage

app = Flask(__name__)
api = Api(app)

entityModel = api.model('EntityType', {
    'name': fields.String,
    'mechanism': fields.String
})


def extract(key, value, elements):
    for element in elements:
        if element[key] == value:
            return element
    return None

@api.route('/entitytypes')
class EntityListApi(Resource):
    def get(self):
        return storage

    def post(self):
        pass


@api.route('/entitytypes/<string:entity_type_name>')
class EntityApi(Resource):
    def get(self, entity_type_name):
        entity_type = extract("name", entity_type_name, storage)
        return entity_type


if __name__ == '__main__':
    app.run(debug=True)
