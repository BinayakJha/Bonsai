from __future__ import annotations

import pymongo
import time
import asyncio
import typing as t

if t.TYPE_CHECKING:
    from server.src.user import User
    from server.src.snip import Snip

USER = "bonsaidb"
PASSWORD = "7IDyymBnS0B0LUXs"


class Mongo:
    def __init__(self) -> None:
        self.client = pymongo.MongoClient(
            f"mongodb+srv://{USER}:{PASSWORD}@cluster0.bxfgywb.mongodb.net/?retryWrites=true&w=majority"
        )
        self.database = self.client.get_database("database")

        self.users_collection = self.database.get_collection("users")
        self.snippets_collection = self.database.get_collection("snippets")

    async def load_users(self) -> list[User]:
        """Load all of the users that are currently in the database."""
        from server.src.user import User
        return list(
            map(
                User.from_json,
                await asyncio.get_event_loop().run_in_executor(
                    None, lambda: self.users_collection.find({})
                ),
            )
        )

    async def save_user(self, user: User):
        def save_user():
            if self.users_collection.count_documents({"email": user.email}) >= 1:
                self.users_collection.replace_one({"email": user.email}, user.to_json())
            else:
                self.users_collection.insert_one(user.to_json())

        await asyncio.get_event_loop().run_in_executor(
            None,
            save_user,
        )

    async def save_newest_snip(
        self, *, user: User, email: str, summary: str, link: str
    ):
        await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: self.snippets_collection.insert_one(
                {
                    "user": user.email,
                    "email": email,
                    "summary": summary,
                    "link": link,
                    "time": time.time(),
                }
            ),
        )

    async def fetch_snips(self, user: User) -> list[Snip]:
        """Load the top 100 most recent snips for a user"""
        from server.src.snip import Snip

        def snip_to_snip(data):
            return Snip(
                email=data["email"],
                summary=data["summary"],
                link=data["link"],
            )

        return list(
            map(
                snip_to_snip,
                await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: self.snippets_collection.find({"user": user.email})
                    .sort("data", pymongo.ASCENDING)
                    .limit(100),
                ),
            )
        )


MONGO = Mongo()
