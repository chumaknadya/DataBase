import math
import os
from random import random

import datetime
import psycopg2
import psycopg2.extras
from config import config
from faker import Faker

from src.entities.Customer import Customer
from src.entities.Country import Country
from src.entities.Sales import Sales
from src.entities.Site import Site
from src.entities.Site_category import Site_category
from src.entities.Team import Team

class Database(object):
    def __init__(self):
        self.conn = None

    def connect(self) -> None:
        try:
            # read connection parameters
            params = config()
            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            self.conn = psycopg2.connect(**params)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def close_connection(self) -> None:
        if self.conn is not None:
            self.conn.close()
            print('Database connection closed.')

    def exec_sql(self, sql: str) -> None:
        script_file = open('{0}/src/sql/{1}'.format(os.path.dirname(__file__), sql), 'r')
        with self.get_cursor() as cur:
            cur.execute(script_file.read())
            self.conn.commit()

    def get_cursor(self):
        return self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


    def generate_random_teams(self):
        fake = Faker()
        script = """INSERT INTO team(team_name, team_description, team_country_id)
                    VALUES(%s, %s, (SELECT country_id FROM country ORDER BY random() LIMIT 1));"""
        with self.get_cursor() as cur:
            for i in range(1000):
                cur.execute(script, [fake.first_name_male(), fake.date_of_birth(tzinfo=None, minimum_age=1, maximum_age=5)])

    def generate_random_customers(self):
        fake = Faker()
        script = """INSERT INTO customer(customer_name) VALUES(%s);"""
        with self.get_cursor() as cur:
            for i in range(1000):
                cur.execute(script, [fake.first_name_male()])
# Site
    def get_sites(self):
        script = """ SELECT site_id, site_name FROM site"""
        with self.get_cursor() as cur:
            cur.execute(script)
            sites = cur.fetchall()
        return [Site(id=s['site_id'], name=s['site_name']) for s in sites]

# Country
    def get_countries(self):
        script = """
            SELECT country_id, name
            FROM country"""
        with self.get_cursor() as cur:
            cur.execute(script)
            countries = cur.fetchall()
        return [Country(id=c['country_id'], name=c['name']) for c in countries]

    def get_country_by_team(self, team_id: int):
        script = """
                    SELECT c.country_id, c.name FROM country c
                    JOIN team t
                    ON t.team_country_id = c.country_id
                    WHERE t.team_id = %s"""
        with self.get_cursor() as cur:
            cur.execute(script, [team_id])
            countries = cur.fetchall()
            self.conn.commit()
        return [Country(id=c['country_id'], name=c['name']) for c in countries]

    def get_country_not_in_team(self, team_id: int):
        script = """
                   SELECT c.country_id, c.name FROM country c
                   WHERE c.country_id NOT IN(
                       SELECT c.country_id FROM country c 
                       JOIN team t
                       ON t.team_country_id = c.country_id
                       WHERE t.team_country_id = %s)"""
        with self.get_cursor() as cur:
            cur.execute(script, [team_id])
            countries = cur.fetchall()
        return [Country(id=c['country_id'], name=c['name']) for c in countries]

    def add_country_to_team(self, team_id: int, country_id: int) -> None:
        update_script = """
                            UPDATE team
                            SET (team_country_id) = (%s)
                            WHERE team_id = %s;"""
        update_data = (country_id, team_id)
        with self.get_cursor() as cur:
            cur.execute(update_script, update_data)
            self.conn.commit()

# Sales
    def get_sale(self, sale_id: int) -> Sales:
        script = """
            SELECT * FROM sales
            WHERE sales_id = %s"""
        with self.get_cursor() as cur:
            cur.execute(script, [sale_id])
            sales = cur.fetchone()
        return Sales(id=sales['sales_id'], date=sales['date'], done=sales['done'], customer_id=sales['customer_id'],
                      team_id=sales['team_id'], site_id=sales['site_id'])

    def get_sales(self) -> list:
        with self.get_cursor() as cur:
            cur.execute('SELECT * FROM sales')
            sales = cur.fetchall()
        return [Sales(id=p['sales_id'], date=p['date'], done=p['done'], customer_id=p['customer_id'],
                      team_id=p['team_id'], site_id=p['site_id']) for p in sales]


    def get_sales_by_customer(self, customer_id) -> list:
        script = """
                    SELECT *
                    FROM sales AS s
                    WHERE s.customer_id = %s"""
        with self.get_cursor() as cur:
            cur.execute(script, [customer_id])
            sales = cur.fetchall()
        return Sales(id=sales['sales_id'], date=sales['date'], done=sales['done'], customer_id=sales['customer_id'],
                      team_id=sales['team_id'], site_id=sales['site_id'])

    def add_sale(self, sale: Sales) -> None:
        insert_script = """
            INSERT INTO sales (date, done, customer_id, team_id, site_id)
            VALUES (%s, %s, %s, %s, %s)"""
        insert_data = (sale.date,
                       sale.done,
                       sale.customer_id,
                       sale.team_id,
                       sale.site_id)
        with self.get_cursor() as cur:
            cur.execute(insert_script, insert_data)
            self.conn.commit()

    def update_sale(self, sale: Sales) -> None:
        update_script = """
                    UPDATE sales
                    SET (date, done, customer_id, team_id, site_id) =
                        (%s, %s, %s, %s, %s)
                    WHERE sales_id = %s;"""
        update_data =(sale.date,
                       sale.done,
                       sale.customer_id,
                       sale.team_id,
                       sale.site_id,
                       sale.id)
        with self.get_cursor() as cur:
            cur.execute(update_script, update_data)
            self.conn.commit()

    def update_sales_status(self, status: bool, sales_ids: list):
        update_sale = """
                    UPDATE sales
                    SET done = %s
                    WHERE player_id IN %s"""
        if sales_ids:
            with self.get_cursor() as cur:
                cur.execute(update_sale, (status, tuple(sales_ids),))
                self.conn.commit()

    def delete_sale(self, sale_id: int) -> None:
        delete_script = """DELETE FROM sales WHERE sales_id=%s;"""
        with self.get_cursor()as cur:
            cur.execute(delete_script, [sale_id])
            self.conn.commit()

    def advanced_sales_search(self, min_date_of_birth, max_date_of_birth, status: bool) -> list:
        script = """
            SELECT s.date, s.done, s.team_id, s.site_id, c.date_of_birth, c.customer_name
            FROM sales s 
            JOIN customer c
            ON s.customer_id = c.customer_id
            WHERE (c.date_of_birth BETWEEN %s AND %s) 
                AND (s.done = %s);"""
        with self.get_cursor() as cur:
            cur.execute(script, [min_date_of_birth, max_date_of_birth, status])
            rows = cur.fetchall()
        return [(Customer(name=r['customer_name'], birth=r['date_of_birth']),
                 Sales(date=r['date'], done=r['done'], team_id=r['team_id'], site_id=r['site_id'])) for r in rows]


# Team
    def get_team(self, team_id: int) -> Team:
        with self.get_cursor() as cur:
            cur.execute('SELECT * FROM team WHERE team_id = {0}'.format(team_id))
            team = cur.fetchone()
        return Team(id=team['team_id'],
                    name=team['team_name'],
                    team_description=team['team_description'],
                    team_country_id=team['team_country_id'])

    def get_teams(self) -> list:
        with self.get_cursor() as cur:
            cur.execute('SELECT * FROM team')
            teams = cur.fetchall()
        return [Team(id=t['team_id'], name=t['team_name'], team_description=t['team_description'], team_country_id=t['team_country_id']) for t in teams]

    def add_team(self, team: Team) -> int:
        insert_script = """
                    INSERT INTO team (team_name, team_description)
                    VALUES (%s, %s) RETURNING team_id;"""
        insert_data = (team.name, team.team_description)
        with self.get_cursor() as cur:
            cur.execute(insert_script, insert_data)
            new_id = cur.fetchone()[0]
            self.conn.commit()
        return new_id

    def update_team(self, team: Team) -> None:
        update_script = """
                    UPDATE team
                    SET (team_name, team_description) = (%s, %s)
                    WHERE team_id = %s;"""
        update_data = (team.name, team.team_description, team.id)
        with self.get_cursor() as cur:
            cur.execute(update_script, update_data)
            self.conn.commit()

    def delete_team(self, team_id: int) -> None:
        delete_script = """DELETE FROM team WHERE team_id=%s;"""
        with self.get_cursor() as cur:
            cur.execute(delete_script, [team_id])
            self.conn.commit()

    def text_search_by_word(self, word) -> list:
        script = """SELECT team_id, team_name, ts_headline(team_description, to_tsquery(%s)) team_description, team_country_id
                    FROM team
                    WHERE to_tsvector(team_description) @@ to_tsquery(%s);"""
        with self.get_cursor() as cur:
            cur.execute(script, [word, word])
            teams = cur.fetchall()
        return [Team(id=t['team_id'], name=t['team_name'], team_description=t['team_description'], team_country_id=t['team_country_id']) for t in teams]

    def text_search_by_word_not_belong(self, word):
        script = """SELECT team_id, team_name, team_description, team_country_id
                    FROM team 
                    WHERE to_tsvector(team_description) @@ !!to_tsquery(%s);"""
        with self.get_cursor() as cur:
            cur.execute(script, [word])
            teams = cur.fetchall()
        return [Team(id=t['team_id'], name=t['team_name'], team_description=t['team_description'], team_country_id=t['team_country_id']) for t in teams]

# Customer
    def get_customer(self, customer_id: int) -> Customer:
        with self.get_cursor() as cur:
            cur.execute('SELECT * FROM customer WHERE customer_id = {0}'.format(customer_id))
            t = cur.fetchone()
        return Customer(id=t['customer_id'], name=t['customer_name'], birth=t['date_of_birth'])

    def get_customers(self) -> list:
        with self.get_cursor() as cur:
            cur.execute('SELECT customer_id, customer_name, date_of_birth  FROM customer')
            customers = cur.fetchall()
        return [Customer(id=t['customer_id'], name=t['customer_name'], birth=t['date_of_birth']) for t in customers]

    def delete_customer(self, customer_id: int) -> None:
        delete_script = """DELETE FROM customer WHERE customer_id=%s;"""
        with self.get_cursor() as cur:
            cur.execute(delete_script, [customer_id])
            self.conn.commit()

    def add_customer(self, customer: Customer) -> None:
        insert_script = """
                    INSERT INTO customer (customer_name, date_of_birth)
                    VALUES (%s, %s) """
        insert_data = (customer.name, customer.birth)
        with self.get_cursor() as cur:
            cur.execute(insert_script, insert_data)
            self.conn.commit()

    def update_customer(self, customer: Customer) -> None:
        update_script = """
                    UPDATE customer
                    SET (customer_name, date_of_birth) = (%s, %s)
                    WHERE customer_id = %s;"""
        update_data = (customer.name, customer.birth, customer.id)
        with self.get_cursor() as cur:
            cur.execute(update_script, update_data)
            self.conn.commit()

if __name__ == "__main__":
  db = Database()
  db.connect()
  db.exec_sql("drop.sql")
  db.exec_sql("create.sql")
  db.exec_sql("generate.sql")
  #db.generate_random_customers()
  # db.close_connection()
