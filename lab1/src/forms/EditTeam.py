import npyscreen

from src.entities.Team import Team


class EditTeam(npyscreen.ActionFormV2):
    def create(self):
        self.value = None

        self.wgName = self.add(npyscreen.TitleText, name="Name:")
        self.wgDescription = self.add(npyscreen.TitleText, name="Description:")
        self.wgCountry = self.add(npyscreen.TitleFixedText, name="Country:")
        self.wgAvaliableCountries = self.add(npyscreen.TitleSelectOne,
                                      name="Avaliable country:",
                                      max_height=-7,
                                      scroll_exit=True)

    def beforeEditing(self):
        if self.value:
            team = self.parentApp.database.get_team(self.value)
            countries = self.parentApp.database.get_country_by_team(team.id)
            available_country = self.parentApp.database.get_country_not_in_team(team.id)
            self.name = "Team id : %s" % team.id
            self.team_id = team.id
            self.wgName.value = team.name
            self.wgDescription.value = team.team_description
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
        team = Team(name=self.wgName.value, team_description=self.wgDescription.value)
        country_id = None
        if isinstance(self.wgAvaliableCountries.value[0], int):
            country_id = self.wgAvaliableCountries.values[self.wgAvaliableCountries.value[0]][1]
        else:
            country_id = self.country_id
        if self.team_id:
            team.id = self.team_id
            self.parentApp.database.update_team(team)
        else:
            team.id = self.parentApp.database.add_team(team)
        self.parentApp.database.add_country_to_team(team.id, country_id)
        self.parentApp.switchFormPrevious()


    def on_cancel(self):
        self.parentApp.switchFormPrevious()
