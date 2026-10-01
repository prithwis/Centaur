# ============================================================
# mos3.py
# Chanakya Strategic Agent
# ============================================================

import json

from mos import callLLM
from mos2 import Event


class Chanakya_Agent:
    """
    Strategic option generator for a geopolitical actor.

    Each instance has:
        - agent_id      : identity of this Chanakya
        - actor         : geopolitical actor represented
        - generic_role  : common Chanakya instructions
        - actor_role    : actor-specific strategic role

    Given:
        - Trigger Event
        - Current WorldState

    Chanakya generates candidate Reaction Events.

    Chanakya does NOT:
        - select among candidates
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
        actor_role
    ):

        self.agent_id = agent_id
        self.actor = actor
        self.generic_role = generic_role
        self.actor_role = actor_role


    # --------------------------------------------------------
    # Display agent identity
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
        Convert current WorldState into compact text
        for strategic reasoning.

        Chanakya receives:
            - variable name
            - index
            - status
            - surviving conditions

        ZeitWorld transition rationale is deliberately
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
            Event to which this actor is responding.

        world : WorldState
            WorldState resulting from the Trigger Event.

        Returns
        -------
        list[Event]
            Candidate Reaction Events.

        Candidate Events have no event_id and are not
        appended to E.
        """

        trigger_text = self._event_to_text(trigger)
        world_text = self._world_to_text(world)


        # ----------------------------------------------------
        # System prompt
        # ----------------------------------------------------

        system_prompt = f"""
{self.generic_role}

============================================================
ACTOR-SPECIFIC ROLE
============================================================

CHANAKYA AGENT : {self.agent_id}
ACTOR          : {self.actor}

{self.actor_role}
""".strip()


        # ----------------------------------------------------
        # User prompt
        #
        # Exactly TWO candidates is a current prompt rule,
        # not a structural restriction of Chanakya_Agent.
        # ----------------------------------------------------

        user_prompt = f"""
You are generating strategic reaction options for:

ACTOR: {self.actor}

============================================================
TRIGGER EVENT
============================================================

{trigger_text}

============================================================
CURRENT WORLDSTATE
============================================================

{world_text}

============================================================
TASK
============================================================

Generate exactly TWO distinct and contrasting strategic
reactions available to {self.actor} in response to the
Trigger Event and given the Current WorldState.

The alternatives must represent meaningfully different
strategic choices rather than minor variations of the
same action.

For each candidate provide:

- action
- rationale

The rationale must explain why that action could make
strategic sense for {self.actor} in the current situation.

Do NOT choose between the candidates.
Do NOT rank the candidates.
Do NOT assign probabilities.
Do NOT update the WorldState.
Do NOT predict numerical changes to WorldState variables.

Return ONLY valid JSON as a list in exactly this structure:

[
    {{
        "action": "...",
        "rationale": "..."
    }},
    {{
        "action": "...",
        "rationale": "..."
    }}
]
""".strip()


        # ----------------------------------------------------
        # LLM call
        # ----------------------------------------------------

        response = callLLM(
            system_prompt,
            user_prompt
        )


        # ----------------------------------------------------
        # Parse response
        # ----------------------------------------------------

        if isinstance(response, str):
            data = json.loads(response)
        else:
            data = response


        # ----------------------------------------------------
        # Create candidate Event objects
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
        # Candidate Events are returned only.
        # They are NOT appended to E.
        # ----------------------------------------------------

        return candidates