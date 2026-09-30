# =============================================================================
# CENTAUR : MOS — Middle East Oil Security
# Prithwis Mukerjee | 2026
#
# Simulation Module
# =============================================================================

from dataclasses import dataclass, field
import json
from mos import *


@dataclass
class WorldVariable:
    name: str
    description: str
    direction: str

    index: float = 100
    status: str = ""
    conditions: list[str] = field(default_factory=list)


@dataclass
class WorldState:
    state_id: str
    variables: list[WorldVariable] = field(default_factory=list)

    def to_json(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            indent=2
        )