# ==================================================
#  C E N T A U R  ::  MOS
#  Middle East Oil Security Simulator
#
#  Prithwis Mukerjee | 2026
#  Action -> Consequence -> Reaction -> ...
# ==================================================

from mos import *


class PressReporter_Agent:

    # ========================================================
    # Initialise PressReporter
    # ========================================================

    def __init__(
        self,
        client,
        model,
        agent_id,
        generic_role
    ):
        self.client = client
        self.model = model
        self.agent_id = agent_id
        self.generic_role = generic_role


    # ========================================================
    # Convert one WorldState into text
    # ========================================================

    def _worldStateText(self, world):

        text = []

        text.append(f"WORLDSTATE: {world.state_id}")
        text.append("-" * 60)

        for variable in world.variables:

            text.append(f"\nVariable: {variable.name}")
            text.append(f"Index: {variable.index}")
            text.append(f"Description: {variable.description}")
            text.append(f"Direction: {variable.direction}")
            text.append(f"Status: {variable.status}")
            text.append(f"Rationale: {variable.rationale}")

            if variable.conditions:
                text.append("Conditions:")

                for condition in variable.conditions:
                    text.append(f"- {condition}")

        return "\n".join(text)


    # ========================================================
    # Convert one Event into text
    # ========================================================

    def _eventText(self, event):

        text = []

        text.append(f"EVENT: {event.event_id}")
        text.append("-" * 60)

        text.append(f"Actor: {event.actor}")
        text.append(f"Action: {event.action}")
        text.append(f"Rationale: {event.rationale}")
        text.append(
            f"Selection Weight: {event.selection_weight}"
        )

        return "\n".join(text)


    # ========================================================
    # Convert complete Scenario into text
    #
    # W0 -> E0 -> W1 -> E1 -> ... -> En -> W(n+1)
    # ========================================================

    def _scenarioText(self, W, E):

        # A completed Scenario must have one more WorldState
        # than Events.
        if len(W) != len(E) + 1:
            raise ValueError(
                "Incomplete Scenario: "
                "len(W) must equal len(E) + 1."
            )

        text = []

        text.append("MOS SIMULATION SCENARIO")
        text.append("=" * 60)

        text.append(f"Events: {len(E)}")
        text.append(f"WorldStates: {len(W)}")

        # ----------------------------------------------------
        # Initial WorldState
        # ----------------------------------------------------

        text.append("\n\nINITIAL WORLDSTATE")
        text.append("=" * 60)
        text.append(self._worldStateText(W[0]))

        # ----------------------------------------------------
        # Event / resulting WorldState sequence
        # ----------------------------------------------------

        for i, event in enumerate(E):

            text.append("\n\n")
            text.append(self._eventText(event))

            text.append("\n\nRESULTING WORLDSTATE")
            text.append("=" * 60)
            text.append(self._worldStateText(W[i + 1]))

        return "\n".join(text)


    # ========================================================
    # Build Reporting Role
    #
    # Combines the generic PressReporter role with the
    # report-specific Narrative or Structured prompt.
    # ========================================================

    def _buildRole(self, prompt):

        return f"""
{self.generic_role}

{prompt}

Use only the supplied MOS simulation Scenario.

Do not introduce external facts, events or assumptions.
Do not alter Event IDs, WorldState IDs, numerical indices
or selection weights.
"""


    # ========================================================
    # Narrative Report
    #
    # Produces a flowing human-readable account of the Scenario,
    # explaining Events, consequences and major turning points.
    # ========================================================

    def narrative(self, W, E, prompt):

        scenario = self._scenarioText(W, E)
        role = self._buildRole(prompt)

        print(
            f"PressReporter working ---------- "
            f"{self.agent_id} | Narrative"
        )

        return callLLM(
            self.client,
            role,
            scenario,
            self.model
        )


    # ========================================================
    # Structured Report
    #
    # Produces a structured Markdown representation suitable
    # for subsequent machine-based analysis.
    # ========================================================

    def structured(self, W, E, prompt):

        scenario = self._scenarioText(W, E)
        role = self._buildRole(prompt)

        print(
            f"PressReporter working ---------- "
            f"{self.agent_id} | Structured"
        )

        return callLLM(
            self.client,
            role,
            scenario,
            self.model
        )


