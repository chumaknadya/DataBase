import npyscreen

class TeamsList(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(TeamsList, self).__init__(*args, **keywords)
        self.add_handlers({
            "^A": self.when_add_record,
            "^D": self.when_delete_record
        })

    def display_value(self, vl):
        return "Name:%s, Description:%s, Country_id:%s" % (vl.name, vl.team_description, vl.team_country_id)

    def actionHighlighted(self, act_on_this, keypress):
        self.parent.parentApp.getForm('EDITTEAM').value = act_on_this.id
        self.parent.parentApp.switchForm('EDITTEAM')

    def when_add_record(self, *args, **keywords):
        self.parent.parentApp.getForm('EDITTEAM').value = None
        self.parent.parentApp.switchForm('EDITTEAM')

    def when_delete_record(self, *args, **keywords):
        self.parent.parentApp.database.delete_team(self.values[self.cursor_line].id)
        self.parent.update_list()

class TeamsListDisplay(npyscreen.FormMutt):
    MAIN_WIDGET_CLASS = TeamsList

    def __init__(self, *args, **keywords):
        super().__init__(*args, **keywords)
        self.add_handlers({
            "^Q": self.when_exit
        })

    def beforeEditing(self):
        self.update_list()

    def update_list(self):
        self.wMain.values = self.parentApp.database.get_teams()
        self.wMain.display()

    def when_exit(self, *args, **keywords):
        self.parentApp.switchFormPrevious()
