from sqlalchemy import Column, ForeignKey, Integer, Table

from src.entities.Base import Base

countries_teams = Table('countries_teams', Base.metadata,
                          Column('country_id', Integer, ForeignKey('countries.country_id', onupdate='cascade', ondelete='cascade'),
                                 primary_key=True),
                          Column('team_id', Integer, ForeignKey('teams.team_id', onupdate='cascade', ondelete='cascade'),
                                 primary_key=True))