entity_types = [
    {
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
]
