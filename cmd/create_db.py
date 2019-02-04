import os
import sqlalchemy
import db_model


if __name__ == '__main__':
    engine = sqlalchemy.create_engine(os.environ['DATABASE_URL'])
    db_model.Base.metadata.createall(engine)
    print('tables created')

