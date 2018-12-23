from sqlalchemy import Column, Integer, Table, CHAR, Sequence, TIMESTAMP, Text

from src.entities.Base import Base

customers_audit = Table('customers_audit', Base.metadata,
                    Column('audit_id', Integer, Sequence('audit_id_seq'), primary_key=True),
                    Column('operation', CHAR(1), nullable=False),
                    Column('stamp', TIMESTAMP, nullable=False),
                    Column('userid', Text, nullable=False),
                    Column('customerid', Integer, nullable=False))