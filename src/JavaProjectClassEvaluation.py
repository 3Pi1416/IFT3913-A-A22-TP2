import dataclasses
from dataclasses import dataclass
from typing import List


@dataclass
class JavaProjectClassEvaluation:
    public_classes: List = dataclasses.field(default_factory=list)
    interface: List = dataclasses.field(default_factory=list)
    abstract_classes: List = dataclasses.field(default_factory=list)
    private_classes: List = dataclasses.field(default_factory=list)
    other: List = dataclasses.field(default_factory=list)
