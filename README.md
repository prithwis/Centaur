# Centaur / Vikram

![Centaur Concept](images/logo-L.jpg)

## Overview

**Centaur** is an experimental framework for building **LLM-assisted adjudication and judgment systems**.  
At its core is **Vikram**, an LLM-based expert that evaluates proposed actions within complex geopolitical, strategic, or economic scenarios.

The project explores how **human judgment and machine reasoning** can be combined—rather than substituted—to assess plausibility, consequences, and trade-offs in situations where outcomes are uncertain and rules are incomplete.

Centaur is explicitly **not** a prediction engine, optimizer, or simulator.  
It is an **adjudicator**.

---

## Rationale

Many real-world decisions—geopolitical crises, industrial strategy, national security, corporate strategy—do not have:

- complete information
- stable rules
- guaranteed outcomes
- a single “correct” answer

Instead, decision-makers evaluate **proposed actions** against:
- structural constraints
- second-order effects
- proportionality
- uncertainty

Centaur is designed to support this mode of reasoning.

The system treats LLMs as **expert judges**, not as oracles.

---

## The Centaur Idea

The name *Centaur* symbolizes a **hybrid intelligence**:
- **Human**: intent, values, override authority
- **Machine**: consistency, breadth of recall, disciplined reasoning

The logo -- a **female centaur** -- represents balance rather than dominance:  
neither human nor machine alone, but a joint effort.

Human control is always retained.

---

## Vikram: The Adjudicator

**Vikram** is the first implemented adjudicator within the Centaur framework.

### Core characteristics

- Evaluates **plausibility**, not success
- Does **not** assume actions work as intended
- Avoids inventing hidden mechanics or rules
- Assesses second-order and systemic effects conservatively
- Explicitly states uncertainty when information is insufficient

Vikram operates within a **Matrix Strategy Game** context.

---

## Matrix Strategy Game

A **Matrix Strategy Game** evaluates actions across multiple interacting dimensions, such as:

- Political
- Military
- Economic
- Technological
- Environmental
- Reputational

Key principles:

- Player moves are **proposals**, not outcomes
- The adjudicator does not optimize or simulate perfectly
- The goal is disciplined reasoning under uncertainty

Centaur provides the adjudication layer for such games.

---

## Input Structure

Scenarios are intentionally layered to reflect real decision contexts:

1. **Background**  
   Structural, slow-moving context (industry structure, geopolitics, history)

2. **Trigger Event**  
   A discrete shock or perturbation (sanctions, embargoes, accidents)

3. **Proposed Response**  
   A policy or strategic action to be evaluated

This separation prevents narrative collapse and retroactive justification.

---

## Human Override

Centaur is **human-supervised by design**.

- LLM adjudication provides structured reasoning
- Humans may override, reinterpret, or reject rulings
- The system is a decision aid, not an authority

This is a core principle, not an optional feature.

---

## Use Cases

### Geopolitical & Strategic Analysis
- Sanctions and trade disruptions
- Industrial policy decisions
- Supply-chain shocks
- Escalation and de-escalation choices

### Management & Business School Case Studies
- Strategy evaluation under uncertainty
- Competing response options to the same crisis
- Classroom debate supported by consistent adjudication
- Comparing short-term vs long-term decision doctrines

### Scenario Stress-Testing
- Testing “tempting but flawed” responses
- Comparing different adjudication philosophies
- Exploring second-order consequences

---

## LLM Strategy

- Initial implementation uses **OpenAI models**
- The architecture is intentionally simple
- Model identity is explicit to allow future comparison
- The framework is designed to extend to **multiple LLMs** or ensembles if required

No commitment is made to any single provider.

---

## Project Status

**Early-stage / exploratory**

- Actively evolving
- Focused on conceptual clarity over feature breadth
- APIs, roles, and adjudication doctrines may change

---

## Philosophy

Centaur is built on a simple idea:

> In complex systems, judgment matters more than prediction.

This project explores how machines can **support** judgment  
without pretending to replace it.

---

## License

See the `LICENSE` file for details.



