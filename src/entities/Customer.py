from src.entities.DBEntity import DbEntity


class Customer(DbEntity):
    def __init__(self, name: str=None, description: str=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.description = description

    def __str__(self):
        return '(<{0}>:<{1}> - {2})'.format(self.id, self.name, self.description)