import npyscreen


class EntityList(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(EntityList, self).__init__(*args, **keywords)

    def actionHighlighted(self, act_on_this, keypress):
        if 'Full' in act_on_this:
            self.parent.parentApp.switchForm('TEXTSEARCH')
        elif 'Advanced' in act_on_this:
            self.parent.parentApp.switchForm('ADVANCEDSEARCH')
        else:
            self.parent.parentApp.switchForm('{0}LIST'.format(act_on_this.upper()))


class EntityListDisplay(npyscreen.FormMutt):
    MAIN_WIDGET_CLASS = EntityList

    def __init__(self, *args, **keywords):
        super().__init__(*args, **keywords)
        self.add_handlers({
            "^Q": self.when_exit
        })

    def beforeEditing(self):
        self.wMain.values = ['Sales', 'Teams', 'Customers', 'Advanced sales search', 'Full text search team' ]
        self.wMain.display()

    def when_exit(self, *args, **keywords):
        self.parentApp.switchForm(None)
