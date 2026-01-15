from typing import Protocol


class GroundTruthEntryProtocol(Protocol):
    query: str

    ground_truth: str

    context: str | None = None
