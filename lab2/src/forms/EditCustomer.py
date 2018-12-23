import npyscreen

from src.entities.Customer import Customer


class EditCustomer(npyscreen.ActionFormV2):
    def create(self):
        self.value = None
        self.wgCustomerName = self.add(npyscreen.TitleText, name="Name:")
        self.wgCustomerBirthday = self.add(npyscreen.TitleDateCombo, name="Birthday")

    def beforeEditing(self):
        if self.value:
            customer = self.parentApp.database.get_customer(self.value)
            self.customer_id = customer.id
            self.name = "Customer id : %s" % customer.id
            self.wgCustomerName.value = customer.name
            self.wgCustomerBirthday.value = customer.birth
        else:
            self.name = "New Customer"
            self.customer_id = ''
            self.wgCustomerName.value = ''
            self.wgCustomerBirthday.value = ''

    def on_ok(self):
        customer = Customer(name=self.wgCustomerName.value, birth=self.wgCustomerBirthday.value)
        if self.customer_id:
            customer.id = self.customer_id
            self.parentApp.database.upsert_customer(self.customer_id, customer)
        else:
            self.parentApp.database.upsert_customer(self.customer_id, customer)
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()