import datetime

from src.entities.DBEntity import DbEntity


class Sales(DbEntity):
    def __init__(self, date: datetime=None, done: bool=None, customer_id: int=None, team_id: int=None, site_id: int=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.date = date
        self.done = done
        self.customer_id = customer_id
        self.team_id = team_id
        self.site_id = site_id

    def __str__(self):
        return '(<{0}>: {1}, {2}, {3}, {4}, {5})'.format(self.id, self.date, self.customer_id, self.team_id, self.site_id, self.done)
