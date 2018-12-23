# !/usr/bin/env python
# encoding: utf-8

import npyscreen

from database import Database
from src.forms.FindSale import FindSale
from src.forms.FullTextSearch import FullTextSearch
from src.forms.EditSale import EditSale
from src.forms.EditTeam import EditTeam
from src.forms.EditCustomer import EditCustomer
from src.forms.CustomerList import CustomersListDisplay
from src.forms.EntityList import EntityListDisplay
from src.forms.SalesList import SalesListDisplay
from src.forms.TeamList import TeamsListDisplay


class DBApplication(npyscreen.NPSAppManaged):
    def onStart(self):
        self.database = Database()
        self.database.connect()
        self.database.generate_countries()
        self.database.generate_random_customers(10)
        self.database.generate_random_teams(10)
        self.database.generate_site_categories()
        self.database.generate_sites()
        self.database.generate_sales(10)
        self.database.execute_sql('triggerAndProcedure.sql')
        self.addForm("MAIN", EntityListDisplay)
        self.addForm("SALESLIST", SalesListDisplay)
        self.addForm("TEAMSLIST", TeamsListDisplay)
        self.addForm("EDITTEAM", EditTeam)
        self.addForm("CUSTOMERSLIST",CustomersListDisplay)
        self.addForm("EDITCUSTOMER", EditCustomer)
        self.addForm("EDITSALE", EditSale)
        self.addForm("TEXTSEARCH", FullTextSearch)
        self.addForm("ADVANCEDSEARCH", FindSale)


    def onCleanExit(self):
        self.database.close_connection()


if __name__ == '__main__':
     myApp = DBApplication()
     myApp.run()
