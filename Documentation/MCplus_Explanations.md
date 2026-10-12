# Monte Carlo++ — Architecture and Methodology

## 1. Concept

**Monte Carlo++ (MC++)** extends traditional Monte Carlo simulation by introducing LLM-based reasoning into the generation and evaluation of uncertain events.

Traditional Monte Carlo relies on predefined mathematical models and probability distributions. This is effective for numerical systems but less straightforward for strategic environments where decisions depend on context, objectives and the actions of other participants.

MC++ uses LLM agents to generate context-dependent strategic alternatives, assign relative probability weights and simulate their consequences.

The objective is not to predict the future but to **explore multiple plausible futures and understand how they emerge**.

## 2. Architecture

MC++ separates the simulation into five functional components.

| Component | Responsibility |
|---|---|
| **ZeitWorld** | Constructs and updates a structured representation of the world |
| **Chanakya** | Generates alternative strategic actions for each actor |
| **Centaur** | Evaluates alternatives and assigns probability weights |
| **Shakuni** | Randomly selects an action using the assigned weights |
| **Analyst** | Examines simulated histories and identifies recurring outcomes |

The first four components constitute the simulation engine. Analyst operates downstream on the resulting histories.

Each LLM-based component uses dedicated role instructions to separate world modelling, strategic reasoning and adjudication.

## 3. Simulation Methodology

A simulation begins with an initial world-state and a triggering event.

Each subsequent **epoch** consists of the following steps:

1. **World Update:** ZeitWorld applies the latest event to the world-state.
2. **Actor Selection:** The turn controller identifies the next actor.
3. **Strategy Generation:** Chanakya proposes alternative actions.
4. **Adjudication:** Centaur assigns probability weights to the alternatives.
5. **Stochastic Selection:** Shakuni selects one action using weighted random sampling.
6. **Event Recording:** The selected action is recorded and becomes the trigger for the next epoch.

The process repeats for a specified number of epochs.

*[Insert Epoch Workflow Diagram]*

## 4. From Individual Runs to Monte Carlo++

A single simulation generates one sequence of events and evolving world-states — one **alternative history**.

Repeated simulations, starting from the same initial conditions, generate an ensemble of alternative histories because stochastic selection can produce different sequences of decisions.

The histories can then be examined at two levels:

- **Statistical analysis:** How frequently do different categories of outcomes occur?
- **LLM-based interpretation:** What decisions, interactions and turning points explain these outcomes?

This combination of stochastic experimentation and narrative interpretation is the distinguishing feature of MC++.

## 5. Implementation: Middle East Oil Security

The first implementation, **MOS (Middle East Oil Security)**, simulates strategic interactions between the United States and Iran in a crisis affecting Persian Gulf oil security.

The world is represented through eight indexed variables covering oil prices, maritime flows, Indian oil imports, sanctions enforcement, political cohesion, geopolitical tension and armed conflict.

Each simulation produces a structured machine-readable report. Human-readable narratives can be generated separately.

In an initial experiment involving 40 simulations per trigger, the following outcomes were observed:

| Outcome | Iran-initiated crisis | US-initiated de-escalation |
|---|---:|---:|
| Escalation | 90% | 5% |
| Stalemate | 7.5% | 45% |
| De-escalation | 2.5% | 50% |

These results demonstrate how different triggering conditions can produce substantially different distributions of simulated outcomes. They are properties of the experimental model, not estimates of real-world geopolitical probabilities.

## 6. Limitations

MC++ remains an experimental framework.

- LLM-generated probability weights are subjective and are not necessarily calibrated against observed data.
- Outcomes depend on role instructions, world-state definitions, model selection and initial conditions.
- Repeated simulations explore uncertainty within the constructed model; they do not establish the likelihood of real-world events.
- Statistical frequencies describe the simulated ensemble, not external reality.

These limitations are important when interpreting results.

## 7. Beyond Geopolitics

The architecture is not restricted to geopolitical simulations.

Potential applications include competitive business strategy, supply-chain disruptions, market-entry decisions, regulatory scenarios and other environments involving interacting actors and evolving circumstances.

The domain-specific world model, actor roles and decision criteria can be changed without fundamentally altering the simulation engine.

---

## The Central Idea

**Traditional Monte Carlo explores uncertainty within predefined mathematical models.**

**Monte Carlo++ uses LLMs to introduce context-dependent strategic decisions into stochastic simulations.**

The result is not a forecast of what *will* happen, but a structured exploration of what *could* happen — and why.