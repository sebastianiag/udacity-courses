from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from setup_database import Base, Restaurants, MenuItem

engine = create_engine('postgresql://vagrant:glue@localhost/restaurant_db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

rests = ["Kolulu's Kitchen", "Qamqunapah", "Carnaval Cubano", "Cafe Florida", "La Revolucion"]

for rest in rests:
    session.add(Restaurants(name=rest))
session.commit()    
myRest = session.query(Restaurants).filter_by(name="Kolulu's Kitchen").first()
dish = MenuItem(name="Lagartija con salsa Miso", description="Gallina de Palo marinada en salsa Miso", course="Main", price=3.99, restaurants=myRest)
session.add(dish)
session.commit()
