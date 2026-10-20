C_RESET  = "\033[0m"
C_TITLE  = "\033[1;95m"
C_INPUT  = "\033[96m"
C_ALLOC  = "\033[92m"
C_FAIL   = "\033[91m"
C_HEADER = "\033[1;94m"

# np = number of processes
# nb = number of blocks
nb = int(input(f"{C_INPUT}Enter number of memory blocks: {C_RESET}"))
blocks = list(map(int, input(f"{C_INPUT}Enter sizes of blocks: {C_RESET}").split()))

if len(blocks) != nb:
    print("Error: Number of block sizes does not match input.")
    exit()

np = int(input(f"{C_INPUT}Enter number of processes: {C_RESET}"))
processes = list(map(int, input(f"{C_INPUT}Enter sizes of processes: {C_RESET}").split()))

if len(processes) != np:
    print("Error: Number of process sizes does not match input.")
    exit()

allocated = [False] * nb
allocation = [-1] * np

for i in range(np):
    best_index = -1

    for j in range(nb):
        if not allocated[j] and blocks[j] >= processes[i]:
            if best_index == -1 or blocks[j] < blocks[best_index]:
                best_index = j

    if best_index != -1:
        allocation[i] = best_index
        allocated[best_index] = True

print(f"\n{C_TITLE}===== Best Fit Allocation ====={C_RESET}")
print(f"{C_HEADER}Process No.\tProcess Size\tBlock No.{C_RESET}")

for i in range(np):
    if allocation[i] != -1:
        print(f"{C_ALLOC}{i+1}\t\t{processes[i]}\t\t{allocation[i]+1}{C_RESET}")
    else:
        print(f"{C_FAIL}{i+1}\t\t{processes[i]}\t\tNot Allocated{C_RESET}")