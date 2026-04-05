import os
from typing import Any, cast

from google.cloud import firestore
from google.cloud.firestore_v1 import DocumentSnapshot


class Configuration:
    mail: list[str] = []
    country: list[str] = []

    def __init__(self):
        db = firestore.Client(project=os.environ["GOOGLE_CLOUD_PROJECT"])

        mail_docs = db.collection("mail").where(filter=firestore.FieldFilter("is_active", "==", True)).stream()
        country_docs = db.collection("country").where(filter=firestore.FieldFilter("is_active", "==", True)).stream()
        param_doc = cast(DocumentSnapshot, db.collection("parameter").document("param_1").get())

        self.mail = [d["mail"] for i in mail_docs if (d := i.to_dict()) is not None]
        self.country = [d["code_2"] for i in country_docs if (d := i.to_dict()) is not None]

        config = param_doc.to_dict()
        if config is None:
            raise ValueError("param_1 document not found or has no data")
        self.__config__: dict[str, Any] = config

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
    def access_key(self):
        return self.__config__['access_key']

    @property
    def concurrency_number(self):
        return self.__config__['concurrency_number']
