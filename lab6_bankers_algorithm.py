C_RESET  = "\033[0m"
C_TITLE  = "\033[1;95m"
C_INPUT  = "\033[96m"
C_ALLOC  = "\033[92m"
C_FAIL   = "\033[91m"
C_HEADER = "\033[1;94m"
C_WARN   = "\033[93m"


# Reads a 2D matrix from the user row by row.
def get_matrix(prompt, rows, cols):
    print(f"{C_INPUT}{prompt}{C_RESET}")
    matrix = []
    for i in range(rows):
        row = list(map(int, input(f"{C_INPUT}  Process {i}: {C_RESET}").split()))
        if len(row) != cols:
            raise ValueError(f"Expected {cols} values for Process {i}, got {len(row)}.")
        matrix.append(row)
    return matrix


# Runs the Safety Algorithm to determine if the system is in a safe state.
def is_safe(processes, avail, max_mat, alloc):
    n = processes
    r = len(avail)

    # Calculate the remaining need for each process
    need = [[max_mat[i][j] - alloc[i][j] for j in range(r)] for i in range(n)]

    work     = avail[:]       
    finish   = [False] * n  
    safe_seq = []              

    while len(safe_seq) < n:
        found = False
        for i in range(n):
            # Check if process i can be satisfied with current work resources
            if not finish[i] and all(need[i][j] <= work[j] for j in range(r)):
                work = [work[j] + alloc[i][j] for j in range(r)]
                finish[i] = True
                safe_seq.append(i)
                found = True
                break                  # Restart search from the beginning
        if not found:
            # No eligible process found — system is in an unsafe state
            return False, safe_seq, need

    return True, safe_seq, need        # All processes finished — safe state


#USER INPUT
# Collect the number of processes, resource types, and the three key matrices:
print(f"\n{C_TITLE}===== Banker's Algorithm Simulator ====={C_RESET}\n")

n = int(input(f"{C_INPUT}Enter number of processes: {C_RESET}"))
r = int(input(f"{C_INPUT}Enter number of resource types: {C_RESET}"))

available = list(map(int, input(f"{C_INPUT}Enter available resources ({r} values): {C_RESET}").split()))

# input_ok acts as a gate — if any input step fails, all following sections are skipped
input_ok = True

if len(available) != r:
    print(f"{C_FAIL}Error: Expected {r} resource values.{C_RESET}")
    input_ok = False

if input_ok:
    try:
        print(f"\n{C_INPUT}Enter Maximum matrix (space-separated per process):{C_RESET}")
        max_matrix = get_matrix("", n, r)       # Maximum demand matrix

        print(f"\n{C_INPUT}Enter Allocation matrix (space-separated per process):{C_RESET}")
        alloc_matrix = get_matrix("", n, r)     # Currently allocated resources matrix
    except ValueError as e:
        print(f"{C_FAIL}Error: {e}{C_RESET}")
        input_ok = False


#COMPUTE NEED MATRIX
# Need[i][j] = Max[i][j] - Allocation[i][j]
# This tells us how many more resources each process may still request
if input_ok:
    need_matrix = [[max_matrix[i][j] - alloc_matrix[i][j] for j in range(r)] for i in range(n)]

    
    print(f"\n{C_TITLE}===== Resource Allocation State ====={C_RESET}")

    col_w      = 12
    res_labels = "  ".join(f"R{j}" for j in range(r))   # e.g. "R0  R1  R2"

    # Print table header with column group labels and resource sub-labels
    print(f"\n{C_HEADER}{'Process':<12}{'Allocation':<{col_w * r}}{'Max':<{col_w * r}}{'Need':<{col_w * r}}{C_RESET}")
    print(f"{C_HEADER}{'':12}{res_labels:<{col_w * r}}{res_labels:<{col_w * r}}{res_labels}{C_RESET}")

    # Print one row per process
    for i in range(n):
        alloc_str = "  ".join(map(str, alloc_matrix[i])).ljust(col_w * r)
        max_str   = "  ".join(map(str, max_matrix[i])).ljust(col_w * r)
        need_str  = "  ".join(map(str, need_matrix[i]))
        print(f"{C_ALLOC}P{i:<11}{alloc_str}{max_str}{need_str}{C_RESET}")

    print(f"\n{C_HEADER}Available Resources: {C_ALLOC}{' '.join(map(str, available))}{C_RESET}")


    #SAFETY ALGORITHM CHECK
    safe, seq, _ = is_safe(n, available, max_matrix, alloc_matrix)

    print(f"\n{C_TITLE}===== Safety Algorithm Result ====={C_RESET}")
    if safe:
        print(f"{C_ALLOC}System is in a SAFE state.{C_RESET}")
        print(f"{C_ALLOC}Safe Sequence: {' -> '.join(f'P{p}' for p in seq)}{C_RESET}")
    else:
        print(f"{C_FAIL}System is in an UNSAFE state! Deadlock may occur.{C_RESET}")


    # RESOURCE REQUEST HANDLING
    print(f"\n{C_TITLE}===== Resource Request ====={C_RESET}")
    req_proc = int(input(f"{C_INPUT}Enter process number making a request (0 to {n-1}): {C_RESET}"))
    request  = list(map(int, input(f"{C_INPUT}Enter request vector ({r} values): {C_RESET}").split()))

    if len(request) != r:
        # Wrong number of values entered — cannot proceed
        print(f"{C_FAIL}Error: Expected {r} values.{C_RESET}")

    else:
        print(f"\n{C_HEADER}Checking request {request} for P{req_proc}...{C_RESET}")

        if any(request[j] > need_matrix[req_proc][j] for j in range(r)):
            print(f"{C_FAIL}Request denied: Exceeds maximum claim (Need).{C_RESET}")
            
        elif any(request[j] > available[j] for j in range(r)):
            print(f"{C_WARN}Process P{req_proc} must wait — resources not currently available.{C_RESET}")

        else:
            new_avail = [available[j] - request[j] for j in range(r)]      # Deduct from available
            new_alloc = [row[:] for row in alloc_matrix]                    # Copy current allocation
            new_max   = [row[:] for row in max_matrix]                      # Max stays the same
            for j in range(r):
                new_alloc[req_proc][j] += request[j]                        # Add request to process

            safe2, seq2, _ = is_safe(n, new_avail, new_max, new_alloc)      # Re-run safety check


            # FINAL DECISION
            # Based on the safety check after tentative allocation:
            #   • GRANTED : new state is safe — request is approved and resources are given
            #   • DENIED  : new state is unsafe — request is rolled back to avoid deadlock
            print(f"\n{C_TITLE}===== Request Decision ====={C_RESET}")
            if safe2:
                print(f"{C_ALLOC}Request GRANTED — system remains in safe state.{C_RESET}")
                print(f"{C_ALLOC}New Safe Sequence: {' -> '.join(f'P{p}' for p in seq2)}{C_RESET}")
                print(f"{C_ALLOC}New Available: {new_avail}{C_RESET}")
            else:
                print(f"{C_FAIL}Request DENIED — granting it would lead to an unsafe state.{C_RESET}")