# Operating Systems Lab Simulations

Python simulations of core operating system concepts: CPU scheduling, file allocation, memory management, deadlock avoidance, page replacement, and process synchronisation.

Completed for **WIA2004 Operating Systems**, Faculty of Computer Science & Information Technology, Universiti Malaya (Session 2025/2026, Semester 2).

## Labs

| # | Topic | File | What it does |
|---|-------|------|--------------|
| 1 | CPU Scheduling: FCFS | `lab1_fcfs_scheduling.py` | Runs processes in arrival order and computes completion, turnaround and waiting time for each, plus averages. |
| 2 | CPU Scheduling: SJF | `lab2_sjf_scheduling.py` | Non-preemptive Shortest Job First with arrival times. Picks the shortest available job, breaks ties by arrival time, and shows the execution order. |
| 3 | File Allocation: Sequential | `lab3_sequential_file_allocation.py` | Interactive disk simulator. Allocates files to the first block of contiguous free space, deletes files, and displays the directory and a block map. |
| 4 | Memory Allocation: Best Fit | `lab4_best_fit_memory.py` | Assigns each process to the smallest free partition large enough to hold it. |
| 5 | Memory Allocation: First Fit | `lab5_first_fit_memory.py` | Assigns each process to the first free partition large enough to hold it and reports internal fragmentation. |
| 6 | Deadlock Avoidance: Banker's Algorithm | `lab6_bankers_algorithm.py` | Computes the Need matrix, runs the safety algorithm to find a safe sequence, and decides whether a resource request can be granted safely. |
| 7 | Page Replacement: FIFO | `lab7_fifo_page_replacement.py` | Replaces the oldest page in memory on each page fault and shows the frame contents step by step. |
| 8 | Synchronisation: Dining Philosophers | `lab8_dining_philosophers.py` | Multithreaded simulation using locks. Deadlock is prevented by asymmetric ordering: even-numbered philosophers pick up the right chopstick first, odd-numbered ones the left. |

## Requirements

- Python 3.8 or later
- No external libraries (standard library only)

## How to run

```bash
python lab1_fcfs_scheduling.py
```

Each program asks for its input interactively in the terminal.

Some programs use ANSI colour codes in their output. These display correctly in most Linux and macOS terminals and in Windows Terminal. In the older Windows Command Prompt, you may see escape characters instead of colours.

## Example (Lab 1: FCFS)

```
Enter number of processes: 3
Enter burst time for P1: 5
Enter burst time for P2: 3
Enter burst time for P3: 8

Process   Burst     Completion    TAT       WT
P1        5         5             5         0
P2        3         8             8         5
P3        8         16            16        8

Average TAT = 9.67
Average WT  = 4.33
```

## Concepts covered

- **CPU scheduling:** turnaround time, waiting time, non-preemptive scheduling
- **File systems:** contiguous allocation, directory management, external fragmentation
- **Memory management:** fixed partitioning, best fit, first fit, internal fragmentation
- **Deadlock:** Banker's algorithm, safe state, safety algorithm, resource request handling
- **Virtual memory:** demand paging, FIFO page replacement, page faults
- **Concurrency:** threads, mutual exclusion locks, deadlock prevention
