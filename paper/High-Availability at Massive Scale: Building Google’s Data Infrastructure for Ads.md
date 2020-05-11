
High-Availability at Massive Scale: Building Google’s Data Infrastructure for Ads

What is this paper about?
* stream processing
* high availability multi-homed systems
* common challenges and solutions
* lessons learned in building and running these large-scale systems

What are availability and consistency?
* avialability will be measure based on overall delay in the streamming system
* consistency
    * exactly once processing
    * observing state repeatedly should see the state moving forward

Typical failure scenarios
* machine
* netword connectivity
* underlying infrastructure

Availability tiers
* singly-homed systems: run in a single datacenter
* failover-based systems
    * failover usually as an add-on feature
* multi-homed systems
    * designed to run in multiple datacenters as a core design property

Synchronous global state
* Paxos-based commit to update metadata synchronously
    * Spanner
* typically use some form of batching to reduce round trips (10ms) to global state.

What to checkpoint?
* typically, initial checkpointing at the input state of the pipeline

Repeatable Input?
* logs are copied to two datacentors.
    * Why two?
* when a lookup cannot be made repeatable, store the result of the lookup

Exactly once output
* idempotent output
* two-phase commit

Resource cost:
* multiple-homed systems cost les than the failover design

Multi-homed systems at Google
* F1 / Spanner: Relational database
* Photon: joining continuous data streams
* Mesa: data warehousing