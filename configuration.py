import json
import os
import sqlalchemy
import sqlalchemy.orm
from .db_model import *


class Configuration:
    mail = []
    country = []

    def __init__(self):
        self.__db_url__ = os.environ['DATABASE_URL']
        self.__engine__ = create_engine(self.__db_url__)
        session = sqlalchemy.orm.Session(self.__engine__)

        self.mail = [i[0] for i in session.query(Mail.mail).filter(Mail.is_active == 'true').all()]

        self.country = [i[0] for i in session.query(Country.code_2).filter(Country.is_active == 'true').all()]

        self.__config__ = json.loads(session.query(Parameter.param_value).filter(Parameter.param_id == 'PARAM_1').one()[0])

    @property
    def url(self):
        return self.__config__['url']

    @property
    def protocol(self):
        return self.__config__['protocol']

    @property
    def session_number(self):
        return self.__config__['session number']

    @property
    def bandwidth(self):
        return self.__config__['bandwidth']

    @property
    def timeout(self):
        return self.__config__['timeout']

    @property
    def smtp_server(self):
        return self.__config__['smtp_server']

    @property
    def smtp_user(self):
        return self.__config__['smtp_user']

    @property
    def smtp_pwd(self):
        return self.__config__['smtp_pwd']

