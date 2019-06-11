
DATA = {
    "room": {
        "name": "room",
        "description": "closed set of rooms in a house",
        "mechanism": {
            "type": "list", 
            "restricted": True,
            "items": [
                {
                    "value": "bathroom",
                    "synonyms": [
                        "bath", "ensuite"
                    ]
                },
                {
                    "value": "hall"
                },
                {
                    "value": "living room",
                    "synonyms": [
                        "lounge", "sitting room", "good room", "good good room"
                    ]
                }
            ]
        }
    }
}

class EntityTypeStorage:


    def __init__(self):
        self._data = DATA

    def find(self, key):
        if self._data[key] is not None:
            return self._data[key]
        return None

    def findAll(self):
        return self._data

    def create(self, value):
        if self._data.get(value['name']):
            raise Exception('Element already present')
        self._data[value['name']] = value
