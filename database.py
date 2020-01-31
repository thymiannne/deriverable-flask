from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///goods_db.sqlite3', echo=True)
Base = declarative_base()


class Goods(Base):
    __tablename__ = 'goods'
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(8))
    amount = Column(Integer)

    def __repr__(self):
        return f'{self.name}: {self.amount}\n'


Base.metadata.create_all(engine)

SessionMaker = sessionmaker(bind=engine)
session = SessionMaker()
session.query(Goods).delete()
sales = Goods(name="sales", amount='0')
session.add(sales)
session.commit()
