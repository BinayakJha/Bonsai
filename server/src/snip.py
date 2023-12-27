import dataclasses
import typing as t


@dataclasses.dataclass
class Snip:
    email: str
    summary: str
    link: str

    def to_json(self) -> str:
        return dataclasses.asdict(self)

    def from_json(self, data) -> t.Self:
        return Snip(**data)
