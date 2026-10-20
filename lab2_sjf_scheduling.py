# ============================================================
#   Non-Preemptive SJF (Shortest Job First) CPU Scheduler
# ============================================================

# --- ANSI Color Codes ---
C_TITLE  = "\033[1;95m"
C_HEADER = "\033[1;96m"
C_PROC   = "\033[92m"
C_AVG    = "\033[1;93m"
RESET    = "\033[0m"

print(f"{C_TITLE}{'='*52}")
print(f"   Non-Preemptive SJF CPU Scheduling Simulator")
print(f"{'='*52}{RESET}\n")

# --- Input ---
n = int(input("Enter number of processes: "))
processes = []

for i in range(n):
    print(f"\n  Process P{i+1}:")
    at = int(input(f"    Arrival Time : "))
    bt = int(input(f"    Burst Time   : "))
    # [ID, ArrivalTime, BurstTime, CompletionTime, TAT, WT, isDone]
    processes.append([i + 1, at, bt, 0, 0, 0, False])

# --- Sort by Arrival Time initially ---
processes.sort(key=lambda x: (x[1], x[2]))

# --- SJF Scheduling Logic ---
current_time    = 0
completed_count = 0
total_wt        = 0
total_tat       = 0
final_data      = []

while completed_count < n:
    # Get all arrived & unfinished processes
    available = [p for p in processes if p[1] <= current_time and not p[6]]

    if not available:
        # No process available yet — jump to next arrival
        next_arrival = min(p[1] for p in processes if not p[6])
        current_time = next_arrival
        continue

    # Pick shortest burst time; tie-break by arrival time
    available.sort(key=lambda x: (x[2], x[1]))
    current_p = available[0]

    # Execute the process
    current_time   += current_p[2]           # Advance time by burst time
    current_p[3]    = current_time            # Completion Time
    current_p[4]    = current_p[3] - current_p[1]  # TAT = CT - AT
    current_p[5]    = current_p[4] - current_p[2]  # WT  = TAT - BT
    current_p[6]    = True                    # Mark done

    total_tat       += current_p[4]
    total_wt        += current_p[5]
    completed_count += 1
    final_data.append(current_p)

# --- Execution Order ---
execution_order = " → ".join([f"P{p[0]}" for p in final_data])
print(f"\n{C_TITLE}Execution Order : {execution_order}{RESET}")

# --- Output Table ---
print(f"\n{C_HEADER}{'='*62}")
print(f"{'Process':<10}{'Arrival':<12}{'Burst':<12}{'Completion':<14}{'TAT':<10}{'WT'}")
print(f"{'='*62}{RESET}")

for p in sorted(final_data, key=lambda x: x[0]):
    print(f"{C_PROC}P{p[0]:<9}{RESET}"
          f"{p[1]:<12}{p[2]:<12}{p[3]:<14}{p[4]:<10}{p[5]}")

print(f"{C_HEADER}{'='*62}{RESET}")
print(f"{C_AVG}Average Waiting Time    : {total_wt  / n:.2f}{RESET}")
print(f"{C_AVG}Average Turnaround Time : {total_tat / n:.2f}{RESET}")
print(f"{C_HEADER}{'='*62}{RESET}\n")