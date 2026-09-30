# =============================================================================
# CENTAUR : MOS — Middle East Oil Security
# Prithwis Mukerjee | 2026
#
# Simulation Module
# =============================================================================

from dataclasses import dataclass, field
import json
from mos import *

# =============================================================================
@dataclass
class WorldVariable:
    name: str
    description: str
    direction: str

    index: float = 100
    status: str = ""
    conditions: list[str] = field(default_factory=list)

# =============================================================================

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

    @classmethod
    def from_dict(cls, data):
        variables = [
            WorldVariable(**v)
            for v in data["variables"]
        ]

        return cls(
            state_id=data["state_id"],
            variables=variables
        )
# =============================================================================      
class ZeitWorld:

    def __init__(self, client, model, role):
        self.client = client
        self.model = model
        self.role = role
        self.initialised = False


    def initialise(self, world_state, world_facts, init_input):
        """
        Create Z0 from real-world evidence.

        This method may be called only once.
        All WorldVariable indices remain at 100.
        ZeitWorld populates status and conditions.
        """

        if self.initialised:
            raise RuntimeError("ZeitWorld has already been initialised.")

        full_input = f"""
        {init_input}

        WORLDSTATE TEMPLATE
        ===================
        {world_state.to_json()}

        WORLD FACTS
        ===========
        {world_facts}
        """

        response = callLLM(
            self.client,
            self.role,
            full_input,
            self.model,
            _effort="medium"
        )

        data = json.loads(response)

        new_state = WorldState.from_dict(data)

        self.initialised = True

        return new_state


    def update(self, current_state, action):
        """
        Generate the next WorldState from the current state
        and an executed action.

        No external real-world information is available here.
        """

        if not self.initialised:
            raise RuntimeError("ZeitWorld must be initialised before update.")

        # LLM processing will go here

        return current_state
# =============================================================================