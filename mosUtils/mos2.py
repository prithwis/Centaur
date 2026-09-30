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

# -------------      

    def show(self, world_state, n=-1):
        """
        Display a WorldState at different levels of detail.

        n = -2       : vector values only
        n = -1       : vector names and values (default)
        0 <= n < N   : complete details of vector n
        n >= N       : complete details of all vectors
        """

        variables = world_state.variables
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

            print(f"\nWorld State : {world_state.state_id}")
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

            print(f"\nWorld State : {world_state.state_id}")
            show_variable(n)
            return


        # ---------------------------------------------------------
        # N or greater : Complete details of all vectors
        # ---------------------------------------------------------
        if n >= N:

            print(f"\nWorld State : {world_state.state_id}")
            print("=" * 70)

            for i in range(N):
                show_variable(i)

            return


        # ---------------------------------------------------------
        # Less than -2 : invalid
        # ---------------------------------------------------------
        print(f"Invalid show parameter: {n}")

# -------------      

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