import npyscreen


class SalesList(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(SalesList, self).__init__(*args, **keywords)
        self.add_handlers({
            "^A": self.when_add_record,
            "^D": self.when_delete_record
        })

    def display_value(self, vl):
        return "Date:%s, Done:%s, Customer_id:%s, Team_id:%s, Site_id:%s" % (vl.date, vl.done, vl.customer_id, vl.team_id, vl.site_id)

    def actionHighlighted(self, act_on_this, keypress):
        self.parent.parentApp.getForm('EDITSALE').value = act_on_this.id
        self.parent.parentApp.switchForm('EDITSALE')

    def when_add_record(self, *args, **keywords):
        self.parent.parentApp.getForm('EDITSALE').value = None
        self.parent.parentApp.switchForm('EDITSALE')

    def when_delete_record(self, *args, **keywords):
        self.parent.parentApp.database.delete_sale(self.values[self.cursor_line].id)
        self.parent.update_list()


class SalesListDisplay(npyscreen.FormMutt):
    MAIN_WIDGET_CLASS = SalesList

    def __init__(self, *args, **keywords):
        super().__init__(*args, **keywords)
        self.add_handlers({
            "^Q": self.when_exit
        })

    def beforeEditing(self):
        self.update_list()

    def update_list(self):
        self.wMain.values = self.parentApp.database.get_sales()
        self.wMain.display()

    def when_exit(self, *args, **keywords):
        self.parentApp.switchFormPrevious()
