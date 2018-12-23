from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm.session import Session
from src.entities.Base import Base
from src.entities.CountryTeam import countries_teams
from sqlalchemy.orm import relationship

class Country(Base):
    __tablename__ = 'countries'
    id = Column('country_id', Integer, Sequence('country_id_seq'), primary_key=True)
    name = Column(String(80), nullable=False)
    teams = relationship('Team', secondary=countries_teams, back_populates='countries')

    def add(self, session: Session):
        session.add(self)

    @staticmethod
    def getAll(session: Session):
        return session.query(Country)

    def __repr__(self):
        return "<Country(id='%s', name='%s'>" % \
               (self.id, self.name)
