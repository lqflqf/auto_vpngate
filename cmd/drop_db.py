import os
import sqlalchemy


if __name__ == '__main__':
    engine = sqlalchemy.create_engine(os.environ['DATABASE_URL'])
    meta = sqlalchemy.MetaData(bind=engine)
    meta.reflect()
    meta.drop_all()
    print('tables dropped')

