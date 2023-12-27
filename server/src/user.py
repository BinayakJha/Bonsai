from __future__ import annotations

import dataclasses
import typing as t
import json

from google.oauth2.credentials import Credentials
from server.src.safe_create_task import create_task
from server.src.email_poll import EmailPoll

_USERS = {}
_STATE_TO_EMAILS = {}


@dataclasses.dataclass
class User:
    email: str

    phone_number: str | None = None
    cred: Credentials | None = None

    # User provided catagories that they want to see.
    whitelist: str | None = None
    # User provided catagories that they don't want to see.
    blacklist: str | None = None

    language: str | None = None

    def __post_init__(self):
        _USERS[self.email] = self

    def to_json(self) -> dict[str, t.Any]:
        return {
            "email": self.email,
            "cred": self.cred.to_json(),
            "phone_number": self.phone_number,
            "whitelist": self.whitelist,
            "blacklist": self.blacklist,
            "language": self.language,
        }

    @classmethod
    def from_json(cls, data: dict[str, t.Any]) -> t.Self:
        u = cls(
            email=data.get("email"),
            phone_number=data.get("phone_number"),
            cred=Credentials.from_authorized_user_info(json.loads(data.get("cred"))),
            whitelist=data.get("whitelist"),
            blacklist=data.get("blacklist"),
            language=data.get("language"),
        )
        _USERS[u.email] = u
        create_task(EmailPoll(u).start())
        return u

    @staticmethod
    def from_state(state: str, email: str | None = None) -> User:
        if email is None:
            return User.from_email(_STATE_TO_EMAILS[state])
        u = User(email=email)
        create_task(EmailPoll(u).start())
        _STATE_TO_EMAILS[state] = email
        _USERS[email] = u
        return u

    @staticmethod
    def from_email(email: str) -> User:
        if email in _USERS:
            return _USERS[email]
        raise Exception("User does not have an email.")


def set_user_email(user: User, email: str) -> None:
    user.email = email
    _STATE_TO_EMAILS[user.state] = email
