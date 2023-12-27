from __future__ import annotations

import json
import datetime
import typing as t
import dataclasses
import base64
import functools

import asyncio

from bs4 import BeautifulSoup
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email",
    "openid",
]
REDIRECT_URL = "http://localhost:3000/profile"

with open("server/client_secret.json") as f:
    CLIENT_SECRETS = json.load(f)


flows: dict[str, Flow] = {}


def new_auth_url():
    flow = Flow.from_client_config(CLIENT_SECRETS, SCOPES, redirect_uri=REDIRECT_URL)
    url, client_state = flow.authorization_url()
    flows[client_state] = flow
    return url


async def authenticate(state: str, code: str) -> Credentials:
    flow = flows[state]

    token = await asyncio.get_event_loop().run_in_executor(
        None, functools.partial(flow.fetch_token, code=code)
    )
    return Credentials.from_authorized_user_info(flow.client_config | token)


def get_user_email(creds: Credentials) -> str:
    service = build("oauth2", "v2", credentials=creds)
    info = service.userinfo().get().execute()
    print(info)
    return info["email"]


def get_emails(creds: Credentials, *, after: datetime.datetime) -> list[Email]:
    creds.refresh(Request())

    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)
    results = service.users().messages().list(userId="me", maxResults=5).execute()
    messages = results.get("messages")

    emails = []

    for msg in messages:
        txt = service.users().messages().get(userId="me", id=msg["id"]).execute()

        time: int = datetime.datetime.fromtimestamp(int(txt["internalDate"][:-3]))

        if time < after:
            return emails

        emails.append(Email.from_json(msg["id"], txt))

    return emails


@dataclasses.dataclass
class Email:
    uid: str
    sender: str
    subject: str
    body: str
    url: str

    @classmethod
    def from_json(cls, uid: str, email: dict) -> t.Self:
        def get_header(name: str) -> str:
            for d in email["payload"]["headers"]:
                if d["name"] == name:
                    return d["value"]

        uid = str(uid)
        sender = get_header("From")
        subject = get_header("Subject")

        if "parts" in email["payload"]:
            parts = email["payload"]["parts"][0]
            data = parts["body"]["data"]
            data = data.replace("-", "+").replace("_", "/")
            decoded_data = base64.b64decode(data)

            # Now, the data obtained is in lxml. So, we will parse
            # it with BeautifulSoup library
            soup = BeautifulSoup(decoded_data, "lxml")
            if soup.body:
                body = soup.body()
            else:
                body = ""
        else:
            body = ""

        return Email(
            uid=uid,
            sender=sender,
            subject=subject,
            body=body,
            url=f"https://mail.google.com/mail/u/0/#inbox/{uid}",
        )

    def __hash__(self) -> int:
        return hash(self.uid)
