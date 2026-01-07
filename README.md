# Thread-Pulse
Thread Pulse is a privacy preserving interaction analysis instrument for measuring stability, volatility, and regime transitions in long-form conversational exchanges.
Rather than evaluating individual responses in insolation, Thread Pulse treats conversation as a temporal system. It analyzes turn-level behavioral signals, specifically response length and variance, across time to reveal how interaction dynamics evolve, stabilize, or fail under extended context. 

Thread Pulse does not analyze semantic content, sentiment, or meaning. All measurements are derived from non-semantic structural properties of the interaction itself, making the instrument suitable for sensitive or private conversational data.

# What Thread-Pulse Measures
Thread Pulse computes rolling statistics over conversational turns to identify:

*Interaction volatility (response length variance)
*Boundedneess (whether variability remains constrained) 
*Persistence (whether stability is sustained across time)
*Time-to-Stability (the point as which a stable regime emerges, if at all)

Stability is defined operationally as a period in which rolling variance remains below a configurable threshold for a minimum duration. This allows interaction regimes to be deteceted without assumptions about model internals, task correctness, or semantic coherence. 

# What Thread-Pulse Is and Is Not
Thread Pulse is an instrument, not a benchmark or evaluation score. It is designed to:

*Observe interaction level behavior across scale
*Detect regime transitions (exploratory - convergent - unstable)
*Compare interaction dynamics across threads or models using a shared metric space

It does not claim to measure: understanding, alignment, intelligence, intent or agency.

# Current Scope
This repository contains Thread Pulse v0.1, demonstrated on curated example datasets. Support for external dataset ingestion and streaming analysis is intentionally exluded from this release to preserve scope clarity and privacy boundaries. Thread Pulse is a part of a broader suite of interaction anaylsis instruments focused on understanding how stability forms and persist in Human-AI exchanges.

Notes: This project was developed by Threadbourne. AI-assisted coding tools were used during implementation, consistent with modern software development practice. All conceptual framing, measurement logic, and evaluation criteria are human-directed.
