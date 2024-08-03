## Caching Concepts

# Introduction
- Cache stores key-value pairs
- It enables fast read-write using in-memory access

# Capacity Management
- How many keys can be stored, any limit ?

# Eviction Policy
- How to remove data when capacity is reached ?

# Expiration 
- Do cache entries have expiration ? Different for each key ?
- How frequently to clean up expired entries ?

# Thread Safety [Required]
- When shared variables are updated concurrently by different processes, data inconsistencies may occur (race condition)
- This happens due to Critical Section Problem i.e. multiple processes are allowed to enter their critical section where they update the shared variable. 3 criteria to solve this
    - Mutual Exclusion - If P1 is updating the shared variable, then P2 should wait
    - Progress - If P1 and P2 want to update the variable, they should not be executing remainder section and both be entering their critical section. The decision on which one should update should not postpone indefinitely
    - Bounded Waiting/Starvation - If P1 is updating shared variable, P2 requests to enter critical section but keeps waiting then P3 also requests but P1 releases and P3 acquires it before P2. If this happens multiple times, it leads to P2 starvation
- Process synchronization is the technique used to avoid race conditions. Can be achieved by
    - Using Locks, Semaphores and mutexes
    - Using immutable objects
    - Using Atomic operations
    - Thread-local storage
    - Concurrent data structures like Queue, deque in Collections module
- Implementations
    - Using Test-and-Set Lock (Hardware based solution)
        - Solves Mutual Exclusion
        - (-) Can't solve Bounded Waiting
    - Using Semaphores (Software based Solution)
        - Proposed by Djikstra
        - It is a technique to manage concurrent processes using an integer
        - It is a non-negative integer value which is shared between threads
        - After getting initializedm, it can only be accessed through two atomic operations
            ```def wait(S):
                    # Blocks other processes by sending in a while loop
                    while S<=0:continue
                    # Acquires the lock for the process
                    S-=1

            ```def signal(S):
                    # Releases the lock
                    S+=1
        - Two Types:
            - Binary Semaphore: 0(locked) and 1(unlocked)
            - Counting Semaphore: 0(locked), >=1(unlocked)
        - Cons: 
            - Busy Waiting
                - CPU cycles wasted while process is waiting; could be used to run other processes
            - Deadlocks - Threads waiting indefinitely for each other's resources
                - P1 updating semaphore S, P2 updating semaphore Q
                - P1 requests Q but waiting for P2 to release Q
                - P2 requests S but waiting for P1 to release S
                - This ends up in Deadlock

# Support Multiple Data Types [Optional]
- String
- Int
- Float
- Boolean

# Persistance [Optional]
- Cache is cleared once power goes which can be a problem sometimes
- So, we can include persistance mechanisms to save data to disk and load it once power back
- Json File 
    - It is a text serialization format
        - key-values can be serialized into json file and saved to disk 
        - can be deserialized to load back the data
    - (+) It is human-readable and a widely used format
    - (+) It is iter-operable outside of the Python ecosystem
    - (-) It can only represent a subset of the Python built-in types, and no custom classes
- Append-Only File (AOF)
    - new data or operations are always added to the end of the file, rather than modifying existing content.
    - this file acts as a log of all operations performed on the cache
    - (+) Durability: Every operation is recorded, minimizing data loss
    - (+) Easier to understand and debug: The file is a sequence of operations.
    - (+) Supports point-in-time recovery: You can replay operations up to any point
    - (-) File size growth: Addressed by periodic compaction.
    - (-) Potential for slower recovery with very large files.
- Redis Database (RDB)
    - Takes point-in-time snapshots of the entire dataset.
    - Faster than AOF for large datasets but may lose recent data in case of a crash.
- Combined AOF and RDB
    - for better performance and durability
- B-Tree and LSM Trees
    - many databases use these for faster access