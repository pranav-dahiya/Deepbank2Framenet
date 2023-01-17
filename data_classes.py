from dataclasses import dataclass
from delphin.eds import EDS


@dataclass()
class DeepbankSentence:
    id: int
    sentence: str
    tokens: list[tuple[str, str]]
    eds: EDS


@dataclass()
class SemlinkInstance:
    id: int
    token: str
    verb: str
    frame: str
    args: dict[str: str]


@dataclass()
class Sentence:
    id: int
    deepbank: DeepbankSentence
    semlink: list[SemlinkInstance]
