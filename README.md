# Centaur

**Enter the Centaur.**

Centaur is a human–AI hybrid simulation framework designed to adjudicate complex strategic decisions. It was originally built for a geopolitical matrix strategy game, but it can be used to evaluate any structured decision scenario where the “state of the world” matters.

Centaur is not a chatbot.  
It is a role-structured simulation engine.

---

## What Problem Does This Solve?

Most LLM applications collapse everything into one stream of text:

- Describe the world  
- Propose an action  
- Evaluate the action  
- Anticipate the opponent  

Centaur separates these functions into distinct roles to make reasoning more disciplined and easier to inspect.

It is a small experiment in structured AI-mediated cognition.

---

## Architecture Overview

Centaur consists of three conceptual components:

### 1. ZeitWorld  
Transforms raw geopolitical or narrative text into a structured, faceted world-state representation.

Think of it as a world pre-processor.

### 2. Centaur  
Acts as a neutral adjudicator.  
Given a world-state and a proposed action, it produces a structured evaluation.

It does not pursue interests.

### 3. Chanakya (Optional)  
Represents an incentive-driven actor.  
Given the updated world-state, it generates strategic responses aligned with its own objectives.

It is explicitly not neutral.

---

## Design Principle

Each component has:

- A sharply defined role  
- A dedicated instruction file  
- Stable behavior across turns  

Roles are separated deliberately. The idea is to prevent descriptive, evaluative and strategic reasoning from blending into one undifferentiated prompt.

Human oversight is expected between stages.

This is simulation, not automation.

---

## How It Works (High Level)

1. Construct or ingest a narrative description of the world.
2. ZeitWorld converts it into a faceted representation.
3. A human proposes an action.
4. Centaur evaluates the action relative to the current world-state.
5. Optionally, Chanakya generates a strategic response.
6. The world-state can then be updated and the cycle repeated.

All outputs are text and can be manually modified before proceeding.

---

## Requirements

- A modern browser - Chrome, Edge
- A GMail ID to use the free Google Colab VM platform
- A login ID to access an LLM API (OpenAI, Gemini, Claude, etc.)
- An API key with sufficient credits, stored as a "secret" associated with the the GMail ID

The prototype currently uses `gpt-4o-mini` for cost efficiency, but any compatible model can be substituted.

---

## Running Alpha Centaur

The easiest way to run the prototype is via the provided Google Colab notebook.

### Steps

1. Go to [Alpha Centaur](https://github.com/prithwis/Centaur/blob/main/Alpha_Centaur.ipynb)
2. Open the notebook in Google Colab by pressing the blue button. You need a GMail ID to create the Notebook in your Google Drive
3. Insert your API key in the designated cell.
4. Run cells sequentially.
5. Modify world descriptions, actions and role instructions as needed, by substituting your text files.

No advanced Python knowledge is required. Prompt design and world construction are more important than code complexity.

---

## Customization

You can modify:

- Role definition files (highly encouraged)
- World facets and structure
- Adjudication criteria
- Model selection
- Simulation loop depth

Centaur is intentionally modular and text-driven.

---

## Intended Use Cases

- Geopolitical simulations
- Classroom strategy games
- Corporate scenario analysis
- Structured case study adjudication
- Experiments in human–AI collaborative reasoning

---

## What This Is Not

- A prediction engine  
- A reinforcement learning system  
- A fully autonomous agent  
- A claim of general intelligence  

It is a structured simulation framework built on top of LLM capabilities.

---

## Status

**Alpha.**

Expect rough edges.  
Expect to edit prompts.  
Expect to experiment.

That is the point.

---

## Final Note

Centaur was originally built because one faculty member cannot credibly adjudicate semiconductor geopolitics, rare earth supply chains, nuclear regulation and AI infrastructure policy all at once.

An LLM can help.  
A structured architecture helps more.

Feedback, forks and thoughtful criticism are welcome.


## License

See the `LICENSE` file for details.

---

> Strategy is easy in clean worlds.  
> Centaur exists for the messy ones.


# Centaur

![Centaur Concept](images/logo-L.jpg)




