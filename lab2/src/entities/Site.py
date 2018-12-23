from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm.session import Session
from src.entities.Base import Base


class Site(Base):
    __tablename__ = 'sites'
    id = Column('site_id', Integer, Sequence('site_id_seq'), primary_key=True)
    name = Column(String(80), nullable=False)
    site_category_id = Column(Integer, ForeignKey('site_categories.site_category_id'))

    def add(self, session: Session):
        session.add(self)

    @staticmethod
    def getAll(session: Session):
        return session.query(Site)

    def __repr__(self):
        return "<Site(id='%s', name='%s', site_category_id='%s')>" % (self.id, self.name, self.site_category_id)
