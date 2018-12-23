from src.entities.DBEntity import DbEntity
import datetime

class Customer(DbEntity):
    def __init__(self, name: str=None, birth: datetime=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.birth = birth

    def __str__(self):
        return '(<{0}>:<{1}> <{3}>)'.format(self.id, self.name, self.birth)
