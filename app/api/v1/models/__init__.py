class Base:
    """contained shared attributes for models"""
    def __init__(self, db):
        self.db = db

    def generate_id(self):
        """gets id to use for new entries in database"""
        if not self.db:
            return 1
        return self.db[-1].get('_id') + 1

    def get(self, value_map):
        """finds an item based on the dictionary given"""
        if not self.db:
            return {}
        key = list(value_map.keys())[0]
        value = value_map.get(key)

        if key and value:
            found_value = [item for item in self.db if item.get(key) == value]
            if found_value:
                return found_value[0]
        return {}
