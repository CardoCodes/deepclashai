class Card:
    def __init__(self, name):
        self.name = name
        self.stats = []
    
    def add_stat(self, name, value):
        self.stats.append({
            'name': name,
            'value': value
        })
    
    def to_dict(self):
        return {
            'name': self.name,
            'stats': self.stats
        }
