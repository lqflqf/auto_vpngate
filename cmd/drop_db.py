import os
import sqlalchemy


if __name__ == '__main__':
    engine = sqlalchemy.create_engine(os.environ['DATABASE_URL'].replace("postgres", "postgresql+psycopg2"))
    meta = sqlalchemy.MetaData(bind=engine)
    meta.reflect()
    meta.drop_all()
    print('tables dropped')

