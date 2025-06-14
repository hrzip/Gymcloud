from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from skripta_za_bazu import Base

engine = create_engine("sqlite:///Gymcloud.db", echo=False)

Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)

# Ovako se pozove da mozemo loadati i spremiti data:
# from db_setup import SessionLocal
# session = SessionLocal()
