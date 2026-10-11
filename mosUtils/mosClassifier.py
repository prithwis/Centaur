# =============================================================================
# MOS — Monte Carlo++ (MC++)
# An LLM-Based Geopolitical Simulation Framework
# Part of the Centaur Architecture
# Post-Simulation Classification Agent
# Designed and Developed by Prithwis Mukerjee | 2026
# =============================================================================

from mos import *


class Classifier_Agent:

    # ========================================================
    # Initialise Classifier
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
    # Build Classification Role
    #
    # Combines the generic Classifier role with the
    # classification-specific prompt.
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
    # Classify one completed Scenario
    #
    # Input  : Structured Scenario Report (text)
    #          Classification-specific prompt
    #
    # Output : LLM-generated classification
    # ========================================================

    def ClassifyScenario(self, scenario, prompt):

        role = self._buildRole(prompt)

        print(
            f"Classifier working ---------- "
            f"{self.agent_id} "
        )

        return callLLM(
            self.client,
            role,
            scenario,
            self.model
        )
        
# ---------------------------------------------------------------------------

from pathlib import Path

# ---------------------------------------------------------
# Read one Role File
# ---------------------------------------------------------

def readRoleFile(filepath):
    return Path(filepath).read_text(encoding="utf-8")


# ---------------------------------------------------------
# Read all Markdown files from a folder
# ---------------------------------------------------------

def readMarkdownFiles(folder):
    reports = {}

    for file in sorted(Path(folder).glob("*.md")):
        reports[file.name] = file.read_text(encoding="utf-8")

    return reports