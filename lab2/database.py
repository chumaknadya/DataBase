import math
import os
from random import random

import datetime
import psycopg2
import psycopg2.extras
from config import config, get_url_connection
from faker import Faker
import sqlalchemy
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from src.entities.CustomerAudit import customers_audit
from session_scope import session_scope
from src.entities.Base import Base
from src.entities.Customer import Customer
from src.entities.Country import Country
from src.entities.CountryTeam import countries_teams
from src.entities.Sale import Sale
from src.entities.Site import Site
from src.entities.Site_category import Site_category
from src.entities.Team import Team

class Database(object):
    def __init__(self):
        url = get_url_connection()
        self.engine = create_engine(url)
        Base.metadata.drop_all(bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
        self.sessionMaker = sessionmaker()

    def get_session(self) -> Session:
        return self.sessionMaker()

    def connect(self):
        try:
            self.sessionMaker.configure(bind=self.engine)
        except Exception as error:
            print(error)

    def close_connection(self) -> None:
        if self.sessionMaker is not None:
            self.sessionMaker.close_all()
            print('Database connection closed.')

    def execute_sql(self, script_file_name: str) -> None:
        script_file = open('{0}/src/sql/{1}'.format(os.path.dirname(__file__), script_file_name), 'r', encoding="utf8")
        with self.engine.connect() as con:
            con.execute(sqlalchemy.text(script_file.read()))

# generate functions
    def generate_site_categories(self) -> None:
        with session_scope(self.get_session) as session:
            Site_category(name='blockchain').add(session)
            Site_category(name='animal').add(session)
            Site_category(name='serial').add(session)
            Site_category(name='filmora').add(session)

    def generate_sites(self) -> None:
        with session_scope(self.get_session) as session:
            Site(name='SBA', site_category_id=session.query(Site_category.id).order_by(func.random()).first()).add(session)
            Site(name='BlockchainIo', site_category_id=session.query(Site_category.id).order_by(func.random()).first()).add(session)
            Site(name='JDAX', site_category_id=session.query(Site_category.id).order_by(func.random()).first()).add(session)
            Site(name='EXQ365', site_category_id=session.query(Site_category.id).order_by(func.random()).first()).add(session)

    def generate_sales(self, sales_count) -> None:
        fake = Faker()
        with session_scope(self.get_session) as session:
            for i in range(sales_count):
                Sale(name=fake.first_name_male(),date=fake.date_between(start_date="-10y", end_date="today"),
                     done=random() > 0.5, customer_id=session.query(Customer.id).order_by(func.random()).first(),
                     team_id=session.query(Team.id).order_by(func.random()).first(),
                     site_id=session.query(Site.id).order_by(func.random()).first()).add(session)

    def generate_countries(self) -> None:
        with session_scope(self.get_session) as session:
            Country(name='America').add(session)
            Country(name='French').add(session)
            Country(name='Avstralia').add(session)
            Country(name='Ukraine').add(session)

    def generate_random_teams(self, team_count: int) -> None:
        fake = Faker()
        with session_scope(self.get_session) as session:
            for i in range(team_count):
                Team(name=fake.first_name_male(),
                     description=fake.word()).add(session)

    def generate_random_customers(self, customer_count: int) -> None:
        fake = Faker()
        with session_scope(self.get_session) as session:
            for i in range(customer_count):
                Customer(name=fake.first_name_male(),birth=fake.date_of_birth(tzinfo=None, minimum_age=0, maximum_age=1)).add(session)
# Searching
    def text_search_by_word(self, word) -> list:
        with session_scope(self.get_session) as session:
            results = session.query(Team).filter(Team.tsv.match(word, postgresql_regconfig='english')).all()
            return [Team(id=t.id, name=t.name,
               description=session.query(func.ts_headline('english', t.description,
               func.to_tsquery(word, postgresql_regconfig='english'))).first()) for t in results]

    def text_search_by_word_not_belong(self, word):
        with session_scope(self.get_session) as session:
            results = session.query(Team).filter(sqlalchemy.not_(Team.tsv.match(word, postgresql_regconfig='english'))).all()
            return [Team(id=t.id, name=t.name, description=t.description) for t in results]

# Customer
    def get_customer(self, customer_id: int) -> Customer:
        return Customer.get(self.get_session(), customer_id)

    def get_customers(self) -> list:
        return Customer.getAll(self.get_session())

    def delete_customer(self, customer_id: int) -> None:
        with session_scope(self.get_session) as session:
            Customer.delete(session, customer_id)

    def upsert_customer(self,  customer_id: int, customer: Customer) -> None:
        with session_scope(self.get_session) as session:
            if customer_id:
                customer.id = customer_id
                customer.update(session)
            else:
                customer.add(session)
# Team
    def get_team(self, team_id: int) -> Team:
        return Team.get(self.get_session(), team_id)

    def get_teams(self) -> list:
        return Team.getAll(self.get_session())

    def delete_team(self, team_id: int) -> None:
        with session_scope(self.get_session) as session:
            Team.delete(session, team_id)


    def upsert_team(self, team_id: int, team: Team, countries: list) -> None:
        with session_scope(self.get_session) as session:
            if team_id:
                team.id = team_id
                team.update(session)
            else:
                team.add(session)
            for country_id in countries:
                statement = countries_teams.insert().values(country_id=country_id, team_id=team.id)
                session.execute(statement)

#Country
    def get_countries(self) -> list:
        return Country.getAll(self.get_session())

#Sale
    def get_sale(self, sale_id: int) -> Team:
        return Sale.get(self.get_session(), sale_id)

    def get_sales(self) -> list:
        return Sale.getAll(self.get_session())

    def delete_sale(self, sale_id: int) -> None:
        with session_scope(self.get_session) as session:
            Sale.delete(session, sale_id)

    def upsert_sale(self,  sale_id: int, sale: Sale) -> None:
        with session_scope(self.get_session) as session:
            if sale_id:
                sale.id = sale_id
                sale.update(session)
            else:
                sale.add(session)
#Sites
    def get_sites(self) -> list:
        return Site.getAll(self.get_session())

#Advanced search
    def advanced_sales_search(self, min_birth, max_birth, done: bool) -> list:
        with session_scope(self.get_session) as session:
            results = session.query(Customer, Sale).filter(Customer.birth.between(min_birth, max_birth)) \
                .join(Sale, Sale.customer_id == Customer.id).filter(Sale.done == done).all()
            session.expunge_all()
            return results

