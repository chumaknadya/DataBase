
from sqlalchemy import Column, Integer, String, Sequence, Date, Boolean, ForeignKey, BOOLEAN
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import Session

from src.entities.Base import Base

class Sale(Base):
    __tablename__ = 'sales'
    id = Column('sale_id', Integer, Sequence('sale_id_seq'), primary_key=True)
    name = Column(String(80), nullable=False)
    date = Column(Date, nullable=False)
    done = Column(Boolean, nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.customer_id', ondelete='set null'))
    team_id = Column(Integer, ForeignKey('teams.team_id', ondelete='set null'))
    site_id = Column(Integer, ForeignKey('sites.site_id'))


    def add(self, session: Session) -> None:
        session.add(self)

    def update(self, session: Session) -> None:
        session.query(Sale).filter(Sale.id == self.id).update({
            'id': self.id,
            'name': self.name,
            'date': self.date,
            'done': self.done,
            'customer_id': self.customer_id,
            'team_id': self.team_id,
            'site_id': self.site_id
        })

    @staticmethod
    def delete(session: Session, player_id: int) -> None:
        session.query(Sale).filter(Sale.id == player_id).delete()

    @staticmethod
    def get(session: Session, player_id: int):
        return session.query(Sale).filter(Sale.id == player_id).first()

    @staticmethod
    def getAll(session: Session) -> list:
        return session.query(Sale).all()

    def __repr__(self):
        return "<Sale(id='%s', name='%s', date='%s', done='%s', customer_id='%s'>" % \
               (self.id, self.name, self.date, self.done, self.customer_id)
