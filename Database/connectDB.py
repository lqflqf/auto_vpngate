from sqlalchemy import *
engine: engine.Engine = create_engine('postgresql://qsdvkddswlfqtv:96d99b02146e6bdc0fd37a512f99731bda1e05a6706e87ba42bfbcd3c5a0b21f@ec2-23-23-111-171.compute-1.amazonaws.com:5432/d6uif7boiuj4gc')

tablist = engine.table_names()



