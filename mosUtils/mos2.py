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
    rationale: str = ""
    conditions: list[str] = field(default_factory=list)

# =============================================================================

@dataclass
class WorldState:
    state_id: str
    variables: list[WorldVariable] = field(default_factory=list)

# -------------------   
    def to_json(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            indent=2
        )
# -------------------   
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
# -------------------        
    def show(self, n=-1):
        """
        Display a WorldState at different levels of detail.

        n = -2       : vector values only
        n = -1       : vector names and values (default)
        0 <= n < N   : complete details of vector n
        n >= N       : complete details of all vectors
        """

        variables = self.variables
        N = len(variables)

        # ---------------------------------------------------------
        # -2 : Values only
        # ---------------------------------------------------------
        if n == -2:
            print([v.index for v in variables])
            return


        # ---------------------------------------------------------
        # -1 : Names and values (default)
        # ---------------------------------------------------------
        if n == -1:

            print(f"\nWorld State : {self.state_id}")
            print("-" * 55)

            for i, v in enumerate(variables):
                print(f"{i:2d}  {v.name:<32} {v.index:8.2f}")

            return


        # ---------------------------------------------------------
        # Helper for detailed display
        # ---------------------------------------------------------
        def show_variable(i):

            v = variables[i]

            print(f"\nVector {i} : {v.name}")
            print("-" * 70)

            print(f"Index       : {v.index}")
            print(f"Description : {v.description}")
            print(f"Direction   : {v.direction}")
            print(f"Status      : {v.status}")
            print(f"Rationale   : {v.rationale}")
            print("Conditions  :")

            if v.conditions:
                for condition in v.conditions:
                    print(f"  - {condition}")
            else:
                print("  - None")


        # ---------------------------------------------------------
        # 0 ... N-1 : Complete details of one vector
        # ---------------------------------------------------------
        if 0 <= n < N:

            print(f"\nWorld State : {self.state_id}")
            show_variable(n)
            return


        # ---------------------------------------------------------
        # N or greater : Complete details of all vectors
        # ---------------------------------------------------------
        if n >= N:

            print(f"\nWorld State : {self.state_id}")
            print("=" * 70)

            for i in range(N):
                show_variable(i)

            return


        # ---------------------------------------------------------
        # Less than -2 : invalid
        # ---------------------------------------------------------
        print(f"Invalid show parameter: {n}")

# =============================================================================      

from pathlib import Path

def getWorldFactBase(WORLDFACTS):
    MD_PATH   = Path(WORLDFACTS) / "MD"
    NEWS_PATH = Path(WORLDFACTS) / "NEWS"

    parts = []

    # Static sources
    for file in sorted(MD_PATH.glob("*.md")):
        text = file.read_text(encoding="utf-8")

        parts.append(
            f"\n===== STATIC SOURCE: {file.name} =====\n{text}"
        )

    # Dynamic news source
    for file in sorted(NEWS_PATH.glob("*.txt")):
        text = file.read_text(encoding="utf-8")

        parts.append(
            f"\n===== LIVE SOURCE: {file.name} =====\n{text}"
        )

    WorldFactBase = "\n".join(parts)
    
    print("Static sources :", len(list(MD_PATH.glob("*.md"))))
    print("Live sources   :", len(list(NEWS_PATH.glob("*.txt"))))
    print("Characters     :", f"{len(WorldFactBase):,}")
    print("Words          :", f"{len(WorldFactBase.split()):,}")

    return WorldFactBase

# =============================================================================     

def getPrompt(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read().strip() 
        
# =============================================================================     

class ZeitWorld_Agent:

    def __init__(self, client, model, role):
        self.client = client
        self.model = model
        self.role = role
        self.initialised = False

# -------------      

    def initialise(self, world_list, world_template, world_facts, init_prompt):
        """
        Create W0 from real-world evidence.

        This method may be called only once.
        All WorldVariable indices remain at 100.
        ZeitWorld populates status and conditions.
        """

        if self.initialised:
            raise RuntimeError("ZeitWorld has already been initialised.")

        print("Initialising WorldState ... ")

        full_input = f"""
        {init_prompt}

        WORLDSTATE TEMPLATE
        ===================
        {world_template.to_json()}

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
        
        # Python controls identity
        new_state.state_id = "W0"

        # W0 immediately becomes part of world history
        world_list.append(new_state)
        self.initialised = True

        return new_state

# -------------            

    def update(self, world_list, event, update_prompt):
        """
        Apply an executed Event to the current WorldState,
        create W[t+1], append it to world_list,
        and return the new WorldState.
        """

        if not self.initialised:
            raise RuntimeError(
                "ZeitWorld must be initialised before update."
            )

        current_state = world_list[-1]
        print("Updating WorldState ----------", current_state.state_id)
        
        current_number = int(current_state.state_id[1:])
        next_state_id = f"W{current_number + 1}"

        # Build complete runtime input
        full_input = f"""
        {update_prompt}

        CURRENT WORLDSTATE
        ==================
        {current_state.to_json()}


        EXECUTED EVENT
        ==============
        Event ID : {event.event_id}
        Actor    : {event.actor}
        Action   : {event.action}
        """

        # Ask ZeitWorld to calculate the new state
        response = callLLM(
            self.client,
            self.role,
            full_input,
            self.model,
            _effort="medium"
        )

        data = json.loads(response)

        new_state = WorldState.from_dict(data)

        # Python controls state identity
        new_state.state_id = next_state_id

        # A successfully generated state immediately becomes history
        world_list.append(new_state)
        print("Appended  WorldState ----------", new_state.state_id)
        return new_state
# =============================================================================

@dataclass
class Event:
    actor: str
    action: str
    rationale: str = ""
    event_id: str = ""

    def show(self):
        print(f"Event     : {self.event_id}")
        print(f"Actor     : {self.actor}")
        print(f"Action    : {self.action}")
        print(f"Rationale : {self.rationale}")