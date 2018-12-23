from src.entities.DBEntity import DbEntity


class Country(DbEntity):
    def __init__(self, name: str=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name

    def __str__(self):
        return '(<{0}>:<{1}>)'.format(self.id, self.name)
