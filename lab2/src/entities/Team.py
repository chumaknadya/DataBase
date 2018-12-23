from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, event, DDL, Index, Text
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import TSVECTOR
from src.entities.Base import Base
from src.entities.CountryTeam import countries_teams


class Team(Base):
    __tablename__ = 'teams'
    id = Column('team_id', Integer, Sequence('team_id_seq'), primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(Text, nullable=False)
    tsv = Column(TSVECTOR, nullable=False)
    __table_args__ = (Index('text_search_idx', tsv, postgresql_using="gin"),)

    countries = relationship('Country', secondary=countries_teams, back_populates='teams')


    def add(self, session: Session) -> None:
        session.add(self)

    def update(self, session: Session) -> None:
        session.query(Team).filter(Team.id == self.id).update({
            'id': self.id,
            'name': self.name,
            'description': self.description
        })

    @staticmethod
    def delete(session: Session, team_id: int) -> None:
        session.query(Team).filter(Team.id == team_id).delete()

    @staticmethod
    def get(session: Session, team_id: int):
        return session.query(Team).filter(Team.id == team_id).first()

    @staticmethod
    def getAll(session: Session) -> list:
        return session.query(Team).all()

    def __repr__(self):
        return "<Team(id='%s', name='%s', description='%s >" % \
               (self.id, self.name, self.description)

event.listen(Team.__table__, 'after_create', DDL("""
            CREATE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE
            ON teams
            FOR EACH ROW EXECUTE PROCEDURE
            tsvector_update_trigger(tsv, 'pg_catalog.english', description);
"""))