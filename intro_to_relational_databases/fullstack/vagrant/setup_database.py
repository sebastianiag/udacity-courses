from sqlalchemy import create_engine, Column, ForeignKey
from sqlalchemy.dialects.postgresql import TEXT, NUMERIC, INTEGER, REAL
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Restaurants(Base):
    __tablename__ = "restaurants"
    id = Column(INTEGER, primary_key=True)
    name = Column(TEXT, nullable=False)

class MenuItem(Base):
    __tablename__ = "menu_item"
    item_id = Column(INTEGER, primary_key=True)
    name = Column(TEXT, nullable=False)
    description = Column(TEXT)
    course = Column(TEXT)
    price = Column(REAL, nullable=False)
    restaurant_id = Column(INTEGER, ForeignKey("restaurants.id"))
    restaurants = relationship(Restaurants)

engine = create_engine('postgresql://vagrant:glue@localhost/restaurant_db')
Base.metadata.create_all(engine)
