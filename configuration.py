import os
from typing import Any, cast

from google.cloud import firestore
from google.cloud.firestore_v1 import DocumentSnapshot


class Configuration:
    def __init__(self):
        self.mail: list[str] = []
        self.country: list[str] = []

        db = firestore.Client(project=os.environ["GOOGLE_CLOUD_PROJECT"])

        mail_docs = db.collection("mail").where(filter=firestore.FieldFilter("is_active", "==", True)).stream()
        country_docs = db.collection("country").where(filter=firestore.FieldFilter("is_active", "==", True)).stream()
        param_doc = cast(DocumentSnapshot, db.collection("parameter").document("param_1").get())

        self.mail = [d["mail"] for i in mail_docs if (d := i.to_dict()) is not None]
        self.country = [d["code_2"] for i in country_docs if (d := i.to_dict()) is not None]

        config = param_doc.to_dict()
        if config is None:
            raise ValueError("param_1 document not found or has no data")
        self._config: dict[str, Any] = config

    def _field(self, key: str) -> Any:
        try:
            return self._config[key]
        except KeyError:
            raise ValueError(f"Missing '{key}' field in Firestore parameter document") from None

    @property
    def url(self) -> str:
        return self._field("url")

    @property
    def protocol(self) -> str:
        return self._field("protocol")

    @property
    def session_number(self) -> int:
        return self._field("session number")

    @property
    def bandwidth(self) -> float:
        return self._field("bandwidth")

    @property
    def timeout(self) -> float:
        return self._field("timeout")

    @property
    def smtp_server(self) -> str:
        return self._field("smtp_server")

    @property
    def smtp_user(self) -> str:
        return self._field("smtp_user")

    @property
    def smtp_pwd(self) -> str:
        return self._field("smtp_pwd")

    @property
    def access_key(self) -> str:
        return self._field("access_key")

    @property
    def concurrency_number(self) -> int:
        return self._field("concurrency_number")
