from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm.session import Session
from src.entities.Base import Base



class Site_category(Base):
    __tablename__ = 'site_categories'
    id = Column('site_category_id', Integer, Sequence('site_category_id_seq'), primary_key=True)
    name = Column(String(80), nullable=False)


    def add(self, session: Session):
        session.add(self)

    @staticmethod
    def getAll(session: Session):
        return session.query(Site_category)

    def __repr__(self):
        return "<SiteCategory(id='%s', name='%s', site_category_id='%s')>" % (self.id, self.name)
