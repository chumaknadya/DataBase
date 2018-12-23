from src.entities.DBEntity import DbEntity


class Team(DbEntity):
    def __init__(self, name: str=None, team_description: str=None, team_country_id: int=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.team_description = team_description
        self.team_country_id = team_country_id

    def __str__(self):
        return '(Id: {0}; Name: {1}; Description: {2};  Country_id: {3})'.format(self.id, self.name, self.team_description, self.team_country_id)
