from __future__ import annotations

import asyncio
import functools
import openai
import typing as t

from twilio.rest import Client

from server.src.google import Email
from server.src.safe_create_task import create_task
from server.src.mongo import MONGO

if t.TYPE_CHECKING:
    from server.src.user import User


ACCOUNT_SID = "AC47543655eaed8d7782356c1f25139c4d"
AUTH_TOKEN = "4d9326a0fa811a41312e2619a3aaed6c"
PHONE_NUMBER = "+18339430488"

MAX_NORMAL_LENGTH = 30

client = Client(ACCOUNT_SID, AUTH_TOKEN)


async def text_email(user: User, email: Email):
    summary = email.body
    if len(summary) >= MAX_NORMAL_LENGTH:
        summary = await summarize(email.subject, email.body)

    if user.whitelist and not await is_in_category(summary, user.whitelist):
        return

    if user.blacklist and await is_in_category(summary, user.blacklist):
        return

    if user.language:
        summary = await translate(summary, user.language)

    create_task(
        MONGO.save_newest_snip(
            user=user, email=email.sender, summary=summary, link=email.url
        )
    )

    await asyncio.get_event_loop().run_in_executor(
        None,
        functools.partial(
            client.messages.create,
            to=user.phone_number,
            from_=PHONE_NUMBER,
            body=f"🪴 Email from {email.sender} - {summary} - 🔗 {email.url}",
        ),
    )


async def ask_ai(prompt) -> str:
    return (
        (
            await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=prompt,
                    max_tokens=300,
                ),
            )
        )
        .choices[0]
        .text.strip()
    )


async def summarize(subject: str, body: str) -> str:
    return await ask_ai(
        "Summarize this email in as few words as possible."
        f"\nSubject: {subject}"
        f"\nBody: {body}."
    )


async def translate(text: str, language: str) -> str:
    return await ask_ai(f"Translate this text into {language}.\n{text}")


async def is_in_category(text: str, categories: list[str]) -> bool:
    if not categories:
        return False

    response = await ask_ai(
        f'Answer the following question with "yes" or "no".'
        "Would it be appropriate to place the following message in any of the"
        f"following categories: {', '.join(categories)}"
        f"\n{text}"
    )

    return "yes" in response.lower()
