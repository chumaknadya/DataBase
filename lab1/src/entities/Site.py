from src.entities.DBEntity import DbEntity


class Site(DbEntity):
    def __init__(self, name: str=None, site_category_id: int=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.site_category_id = site_category_id

    def __str__(self):
        return '(<{0}>:<{1}> - {2})'.format(self.id, self.name, self.site_category_id)
