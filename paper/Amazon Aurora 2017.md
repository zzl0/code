Amazon Aurora, Verbitski et al., SIGMOD 2017.

Why are we reading the Aurora paper?
    * successful recent cloud service, solves serious problems for customers
    * big payoff for good design (Table 1)
    * shows limits of general-purpose storage abstraction
    * many tidbits about what's import in real-world cloud infrastructure

Here's my understanding of the story that led to Aurora.

Amazon EC2 -- clould computing, aimed at we sites

Amazon EBS (Elastic Block Store)

DB-on-EBS shortcomings

Paper assumes you know how DB works, how it uses storage.

Next idea: Figure 2

Aurora big picture

Aurora use two big ideas

Table 1 summarizes results -- 35x throughput increase!

What's Aurora's storage fault tolerance goal?

Failure of the database server is a separate issue

Quorum read/write technique

What is the benefit of quorum read/write storage systems?

What N,W,R does Aurora need?

What does an Aurora quorum write look like?

What do storage servers do with incoming log entries ("writes")?

What does an ordinary Aurora read look like?

When does Aurora use read quorums?

What if the database is too big for a replica to fit into one storage server?

How is the *log* stored w.r.t. PGs?

How to restore replication if a storage server permanently dies?

What about the read-only replicas ("Replica Instance") in Figure 3?

What are the take-away lessons?

