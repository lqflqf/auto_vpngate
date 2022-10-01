import os
from google.cloud import firestore


class Configuration:
    mail = []
    country = []

    def __init__(self):
        db = firestore.Client(project=os.environ["GOOGLE_CLOUD_PROJECT"])

        mail_docs = db.collection("mail").where("is_active", "==", True).stream()

        country_docs = db.collection("country").where("is_active", "==", True).stream()

        param_doc = db.collection("parameter").document("param_1").get()

        self.mail = [(i.to_dict())["mail"] for i in mail_docs]

        self.country = [(i.to_dict())["code_2"] for i in country_docs]

        self.__config__ = param_doc.to_dict()

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

    @property
    def trigger(self):
        return self.__config__['trigger']

    @property
    def day_of_week(self):
        return self.__config__['day_of_week']

    @property
    def hour(self):
        return self.__config__['hour']

    @property
    def timezone(self):
        return self.__config__['timezone']

    @property
    def access_key(self):
        return self.__config__['access_key']
