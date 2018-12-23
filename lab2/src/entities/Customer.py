from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, Date, Index
from sqlalchemy.orm.session import Session
from src.entities.Base import Base

import datetime

class Customer(Base):
    __tablename__ = 'customers'
    id = Column('customer_id', Integer, Sequence('customer_id_seq'), primary_key=True)
    name = Column(String(80), nullable=False)
    birth = Column(Date, nullable=False)

    def add(self, session: Session) -> None:
        session.add(self)

    def update(self, session: Session) -> None:
        session.query(Customer).filter(Customer.id == self.id).update({
            'id': self.id,
            'name': self.name,
            'birth': self.birth
        })

    @staticmethod
    def delete(session: Session, customer_id: int) -> None:
        session.query(Customer).filter(Customer.id == customer_id).delete()

    def update(self, session: Session) -> None:
        session.query(Customer).filter(Customer.id == self.id).update({
            'id': self.id,
            'name': self.name,
            'birth': self.birth
        })

    @staticmethod
    def get(session: Session, customer_id: int):
        return session.query(Customer).filter(Customer.id == customer_id).first()

    @staticmethod
    def getAll(session: Session) -> list:
        return session.query(Customer).all()

    def __repr__(self):
        return "<Customer(id='%s', name='%s', birth='%s')>" % (self.id, self.name, self.birth)
