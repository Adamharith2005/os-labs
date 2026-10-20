# --- ANSI Color Codes ---
C_TITLE  = "\033[1;95m"
C_HEADER = "\033[1;96m"
C_SUCCESS= "\033[92m"
C_ERROR  = "\033[91m"
C_WARN   = "\033[93m"
C_WASTE  = "\033[91m" 
RESET    = "\033[0m"

# Function to allocate processes into blocks by first fit
def first_fit():
    print(f"{C_TITLE}=== FIRST-FIT MEMORY ALLOCATION ==={RESET}")
    
    try:
        # Input partitions
        raw_blocks = input("Enter partition sizes (e.g. 100 500 200 300): ")
        # Structure: [Size, IsOccupied, ProcessName, WastageAmount]
        partitions = [[int(x), False, None, 0] for x in raw_blocks.split()]
        
        # Input processes
        raw_procs = input("Enter process sizes (e.g. 50 212 110): ")
        proc_sizes = [int(x) for x in raw_procs.split()]
        
        max_system_block = max([p[0] for p in partitions])
    except ValueError:
        print(f"{C_ERROR}Error: Please enter valid positive integers.{RESET}")
        return

    print(f"\n{C_HEADER}--- Allocation Log ---{RESET}")
    
    for i, p_size in enumerate(proc_sizes):
        p_name = f"P{i+1}"
        allocated = False # By default, all processes have not been allocated
        
        # If process size is negative or zero of size
        if p_size <= 0:
            print(f"{C_ERROR}[INVALID] {p_name}: Size {p_size} is impossible.{RESET}")
            continue # Skip this process
            
        # If process size is larger than any block
        if p_size > max_system_block:
            print(f"{C_ERROR}[REJECTED] {p_name}: {p_size}K exceeds max block {max_system_block}K.{RESET}")
            continue

        # Else, search a block to allocate the process
        for j in range(len(partitions)):
            block_size = partitions[j][0]
            is_occupied = partitions[j][1]
            # If block size is larger than process size and is empty
            if not is_occupied and block_size >= p_size:
                # Allocate process to the block
                partitions[j][1] = True
                partitions[j][2] = p_name
                # Calculate waste of space (Internal Fragmentation)
                partitions[j][3] = block_size - p_size
                
                print(f"{C_SUCCESS}[SUCCESS] {p_name} ({p_size}K) -> Block {j}{RESET}")
                allocated = True
                break
        
        if not allocated:
            print(f"{C_WARN}[WAITING] {p_name} ({p_size}K): No suitable free block available.{RESET}")

    # Final Output
    print(f"\n{C_HEADER}{'Block':<8} | {'Block Size':<12} | {'Status':<12} | {'Process':<10} | {'Wastage'}{RESET}")
    print("-" * 65)
    
    total_wastage = 0
    for idx, (b_size, occupied, p_name, waste) in enumerate(partitions):
        status = f"{C_SUCCESS}Occupied{RESET}" if occupied else f"{C_WARN}Free{RESET}"
        disp_name = p_name if p_name else "-"
        # Only show wastage if the block is actually occupied
        disp_waste = f"{C_WASTE}{waste}K{RESET}" if occupied else "0K"
        total_wastage += waste if occupied else 0
        
        print(f"{idx:<8} | {b_size:<12} | {status:<21} | {disp_name:<10} | {disp_waste}")
    
    print("-" * 65)
    print(f"{C_TITLE}Total Internal Fragmentation (Wastage): {total_wastage}K{RESET}\n")

if __name__ == "__main__":
    first_fit()