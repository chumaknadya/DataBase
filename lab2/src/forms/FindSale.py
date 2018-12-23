import npyscreen


class FindSale(npyscreen.ActionFormV2):
    def create(self):
        self.value = None
        self.wgDone = self.add(npyscreen.TitleSelectOne,
                                max_height=2,
                                value=[0, ],
                                name='Done',
                                values=['False', 'True'],
                                scroll_exit=True)
        self.wgMinDateOfBirth = self.add(npyscreen.TitleDateCombo, name="Min date of birth:")
        self.wgMaxDateOfBirth = self.add(npyscreen.TitleDateCombo, name="Max date of birth")

        self.gdSales = self.add(npyscreen.MultiLineEdit, name="Results:")

    def beforeEditing(self):
        self.name = "Advanced customer search"
        self.wgDone.value = ''
        self.wgMinDateOfBirth.value = ''
        self.wgMaxDateOfBirth.value = ''


    def on_ok(self):
        search_results = self.parentApp.database.advanced_sales_search(
            self.wgMinDateOfBirth.value,
            self.wgMaxDateOfBirth.value,
            bool(self.wgDone.value[0])
        )
        self.gdSales.values = []
        str_res = ''
        for x in range(len(search_results)):
            customer = search_results[x][0]
            sales = search_results[x][1]
            str_res += ' '.join(("Customer_name: "+str(customer.name), "Customer_birth: "+str(customer.birth), "Sales_ordering_date: "+str(sales.date),
                                 "Sales_order_status: "+str(sales.done)))
            str_res += '\n'

        self.gdSales.value = str_res

    def on_cancel(self):
        self.parentApp.switchFormPrevious()