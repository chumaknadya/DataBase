import npyscreen

from src.entities.Sales import Sales


class EditSale(npyscreen.ActionFormV2):
    def create(self):
        self.value = None
       # all_customers = self.parentApp.database.get_customers()
       # all_teams = self.parentApp.database.get_teams()
       # all_sites = self.parentApp.database.get_sites()
        self.wgDate = self.add(npyscreen.TitleDateCombo, name="Date of ordering")
        self.wgDone = self.add(npyscreen.TitleSelectOne,
                                      max_height=2,
                                      value=[0, ],
                                      name='Done:',
                                      values=['False', 'True'],
                                      scroll_exit=True)
        self.wgTeam = self.add(npyscreen.TitleSelectOne,
                                   max_height=4,
                                   name="Teams:",
                                  # values=[(t.name, t.id) for t in all_teams],
                                   scroll_exit=True,
                                   default=0)

        self.wgCustomers = self.add(npyscreen.TitleSelectOne,
                               name="Customers:",
                               max_height=4,
                              # values=[(c.name, c.id) for c in all_customers],
                               scroll_exit=True)

        self.wgSite = self.add(npyscreen.TitleSelectOne,
                               name="Sites:",
                               max_height=4,
                               #values=[(c.name, c.id) for c in all_sites],
                               scroll_exit=True)

    def beforeEditing(self):
        if self.value:
            all_customers = self.parentApp.database.get_customers()
            all_teams = self.parentApp.database.get_teams()
            all_sites = self.parentApp.database.get_sites()
            sale = self.parentApp.database.get_sale(self.value)
            self.wgSite.values = [(c.name, c.id) for c in all_sites]
            if sale.site_id:
                self.wgSite.value = [x[1] for x in self.wgSite.values].index(sale.site_id)
            else:
                self.wgSite.value = ''
            self.wgCustomers.values = [(c.name, c.id) for c in all_customers]
            if sale.customer_id:
                self.wgCustomers.value = [x[1] for x in self.wgCustomers.values].index(sale.customer_id)
            else:
                self.wgCustomers.value = ''
            self.wgTeam.values = [(t.name, t.id) for t in all_teams]
            if sale.team_id:
                self.wgTeam.value = [x[1] for x in self.wgTeam.values].index(sale.team_id)
            else:
                self.wgTeam.value = ''
            self.name = "Sale id : %s" % sale.id
            self.sale_id = sale.id
            self.wgDate.value = sale.date
            self.wgDone.value = sale.done
        else:
            self.name = "New Sale"
            self.wgCustomers.value = ''
            self.wgTeam.value = ''
            self.sale_id = ''
            self.wgDate.value = ''
            self.wgDone.value = 0
            self.wgSite.value = ''

    def on_ok(self):
        sale = Sales(date=self.wgDate.value,
                     done=bool(self.wgDone.value[0]))
        if isinstance(self.wgCustomers.value[0], int):
            sale.customer_id = self.wgCustomers.values[self.wgCustomers.value[0]][1]
        if isinstance(self.wgTeam.value[0], int):
            sale.team_id = self.wgTeam.values[self.wgTeam.value[0]][1]
        if isinstance(self.wgSite.value[0], int):
            sale.site_id = self.wgSite.values[self.wgSite.value[0]][1]

        if self.sale_id:
            sale.id = self.sale_id
            self.parentApp.database.update_sale(sale)
        else:
            self.parentApp.database.add_sale(sale)
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()
