import npyscreen


class CustomersList(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(CustomersList, self).__init__(*args, **keywords)
        self.add_handlers({
            "^A": self.when_add_record,
            "^D": self.when_delete_record
        })

    def display_value(self, vl):
        return "Name:%s Birthday:%s" % (vl.name, vl.birth)

    def actionHighlighted(self, act_on_this, keypress):
        self.parent.parentApp.getForm('EDITCUSTOMER').value = act_on_this.id
        self.parent.parentApp.switchForm('EDITCUSTOMER')

    def when_add_record(self, *args, **keywords):
        self.parent.parentApp.getForm('EDITCUSTOMER').value = None
        self.parent.parentApp.switchForm('EDITCUSTOMER')

    def when_delete_record(self, *args, **keywords):
        self.parent.parentApp.database.delete_customer(self.values[self.cursor_line].id)
        self.parent.update_list()


class CustomersListDisplay(npyscreen.FormMutt):
    MAIN_WIDGET_CLASS = CustomersList

    def __init__(self, *args, **keywords):
        super().__init__(*args, **keywords)
        self.add_handlers({
            "^Q": self.when_exit
        })

    def beforeEditing(self):
        self.update_list()

    def update_list(self):
        self.wMain.values = self.parentApp.database.get_customers()
        self.wMain.display()

    def when_exit(self, *args, **keywords):
        self.parentApp.switchFormPrevious()
