from dataclasses import dataclass
from datetime import datetime


@dataclass
class Commit:
    date: datetime
    id: str
    file_change = 0
    insertions = 0
    deletions = 0
