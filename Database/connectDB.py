from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql+psycopg2://qsdvkddswlfqtv:96d99b02146e6bdc0fd37a512f99731bda1e05a6706e87ba42bfbcd3c5a0b21f@ec2-23-23-111-171.compute-1.amazonaws.com:5432/d6uif7boiuj4gc')
Session = sessionmaker(bind=engine)

