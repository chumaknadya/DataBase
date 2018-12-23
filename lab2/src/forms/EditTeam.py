import npyscreen

from src.entities.Team import Team


class EditTeam(npyscreen.ActionFormV2):
    def create(self):
        self.value = None
        self.wgName = self.add(npyscreen.TitleText, name="Name:")
        self.wgDescription = self.add(npyscreen.TitleText, name="Description:")
        self.wgCountry = self.add(npyscreen.TitleFixedText, name="Country:")
        self.wgAvaliableCountries = self.add(npyscreen.TitleMultiSelect,
                                      name="Avaliable country:",
                                      max_height=-7,
                                      scroll_exit=True)

    def beforeEditing(self):
        if self.value:
            team = self.parentApp.database.get_team(self.value)
            countries = team.countries
            available_country =  [country for country in self.parentApp.database.get_countries() if country.id not in [c.id for c in countries]]
            self.name = "Team id : %s" % team.id
            self.team_id = team.id
            self.wgName.value = team.name
            self.wgDescription.value = team.description
            self.country_id = ''
            string_country = ''
            for c in countries:
                string_country += '{0} '.format(c.name)
                self.country_id = c.id
            self.wgCountry.value = string_country
            self.wgAvaliableCountries.values = [(c.name, c.id) for c in available_country]
            if self.wgCountry.value:
                 self.wgAvaliableCountries.value = ''
        else:
            all_country = self.parentApp.database.get_countries()
            self.name = "New Team"
            self.team_id = ''
            self.wgName.value = ''
            self.wgDescription.value = ''
            self.wgCountry.value = ''
            self.wgAvaliableCountries.values = [(c.name, c.id) for c in all_country]
            self.wgAvaliableCountries.value = ''

    def on_ok(self):
        team = Team(name=self.wgName.value, description=self.wgDescription.value)
        country_indexes = filter(lambda el: isinstance(el, int), self.wgAvaliableCountries.value)
        country_ids = []
        if country_indexes:
            country_ids = [self.wgAvaliableCountries.values[i][1] for i in country_indexes]
        self.parentApp.database.upsert_team(self.team_id, team, country_ids)
        self.parentApp.switchFormPrevious()


    def on_cancel(self):
        self.parentApp.switchFormPrevious()
