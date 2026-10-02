# ============================================================
# mos3.py
# Chanakya Strategic Agent
# ============================================================

import json

from mos import callLLM
from mos2 import Event


class Chanakya_Agent:
    """
    Strategic option-generation agent for MOS.

    Each Chanakya instance is configured by three role strings:

        generic_role
            Defines what Chanakya is and the general rules
            governing its strategic reasoning.

        specific_role
            Defines the geopolitical actor represented by
            this Chanakya: interests, objectives, constraints,
            vulnerabilities, capabilities, red lines, etc.

        strategy
            Defines the strategy for generating candidate
            reactions: number of candidates, their orientation,
            degree of contrast, or any other option-generation
            rule.

    At each Turn, propose() receives:

        trigger
            The Event to which the actor is responding.

        world
            The current WorldState resulting from that Trigger.

    Chanakya returns a list of candidate Event objects.

    Candidate Events are possibilities only.

    Chanakya does NOT:
        - choose among candidates
        - rank candidates
        - assign probabilities
        - assign event IDs
        - append candidates to E
        - update the WorldState
    """


    # --------------------------------------------------------
    # Initialise Chanakya
    # --------------------------------------------------------

    def __init__(
        self,
        agent_id,
        actor,
        generic_role,
        specific_role,
        strategy
    ):

        self.agent_id = agent_id
        self.actor = actor

        self.generic_role = generic_role
        self.specific_role = specific_role
        self.strategy = strategy


    # --------------------------------------------------------
    # Display Chanakya identity
    # --------------------------------------------------------

    def show(self):

        print(f"Chanakya : {self.agent_id}")
        print(f"Actor    : {self.actor}")


    # --------------------------------------------------------
    # Convert Trigger Event to text
    # --------------------------------------------------------

    def _event_to_text(self, event):

        return f"""
Event ID  : {event.event_id}
Actor     : {event.actor}
Action    : {event.action}
Rationale : {event.rationale}
""".strip()


    # --------------------------------------------------------
    # Convert WorldState to text
    # --------------------------------------------------------

    def _world_to_text(self, world):
        """
        Convert the current WorldState into compact text
        suitable for strategic reasoning.

        Chanakya receives:
            - variable name
            - index
            - status
            - surviving conditions

        ZeitWorld's transition rationale is deliberately
        excluded.
        """

        lines = [
            f"WorldState: {world.state_id}",
            ""
        ]

        for v in world.variables:

            lines.append(f"VARIABLE: {v.name}")
            lines.append(f"Index: {v.index}")
            lines.append(f"Status: {v.status}")

            if v.conditions:

                lines.append("Conditions:")

                for condition in v.conditions:
                    lines.append(f"- {condition}")

            lines.append("")

        return "\n".join(lines)


    # --------------------------------------------------------
    # Generate candidate Reaction Events
    # --------------------------------------------------------

    def propose(self, trigger, world):
        """
        Generate candidate Reaction Events.

        Parameters
        ----------
        trigger : Event
            Event to which this Chanakya is responding.

        world : WorldState
            Current WorldState resulting from the Trigger.

        Returns
        -------
        list[Event]
            Candidate Reaction Events.

        The number and nature of candidates are determined
        entirely by self.strategy.

        Candidate Events:
            - have actor, action and rationale
            - have no event_id
            - are not appended to E
        """


        # ----------------------------------------------------
        # Prepare dynamic simulation context
        # ----------------------------------------------------

        trigger_text = self._event_to_text(trigger)
        world_text = self._world_to_text(world)


        # ----------------------------------------------------
        # System Prompt
        #
        # Generic Role  : how Chanakya reasons
        # Specific Role : actor-specific strategic perspective
        # ----------------------------------------------------

        system_prompt = f"""
============================================================
GENERIC CHANAKYA ROLE
============================================================

{self.generic_role}


============================================================
SPECIFIC ACTOR ROLE
============================================================

CHANAKYA AGENT : {self.agent_id}
ACTOR          : {self.actor}

{self.specific_role}
""".strip()


        # ----------------------------------------------------
        # User Prompt
        #
        # Strategy determines HOW candidate options are
        # generated.
        #
        # Trigger + WorldState provide the current situation.
        # ----------------------------------------------------

        user_prompt = f"""
============================================================
TRIGGER EVENT
============================================================

{trigger_text}


============================================================
CURRENT WORLDSTATE
============================================================

{world_text}


============================================================
STRATEGY
============================================================

{self.strategy}


============================================================
TASK
============================================================

Generate candidate strategic reactions available to
{self.actor} in response to the Trigger Event and given
the Current WorldState.

Follow the STRATEGY instructions above when determining
the number, nature and strategic orientation of the
candidate reactions.

For each candidate provide:

- action
- rationale

The rationale must explain why that action could make
strategic sense for {self.actor} in the current situation.

Do NOT choose among the candidates.
Do NOT rank the candidates.
Do NOT assign probabilities.
Do NOT update the WorldState.
Do NOT predict numerical changes to WorldState variables.


============================================================
OUTPUT FORMAT
============================================================

Return ONLY valid JSON as a list.

Each element of the list must have this structure:

{{
    "action": "...",
    "rationale": "..."
}}
""".strip()


        # ----------------------------------------------------
        # Call LLM
        # ----------------------------------------------------

        response = callLLM(
            system_prompt,
            user_prompt
        )


        # ----------------------------------------------------
        # Parse LLM response
        # ----------------------------------------------------

        if isinstance(response, str):
            data = json.loads(response)
        else:
            data = response


        # ----------------------------------------------------
        # Convert output into candidate Event objects
        # ----------------------------------------------------

        candidates = []

        for item in data:

            candidate = Event(
                actor=self.actor,
                action=item["action"],
                rationale=item["rationale"]
            )

            candidates.append(candidate)


        # ----------------------------------------------------
        # Return candidate Events only.
        #
        # No event_id.
        # Nothing appended to E.
        # ----------------------------------------------------

        return candidates