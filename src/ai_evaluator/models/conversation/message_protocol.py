from typing import Protocol


class MessageProtocol(Protocol):
    role: str

    content: str

    context: str | None
