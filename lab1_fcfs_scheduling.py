# Ask the user to enter the number of processes
n = int(input("Enter number of processes: "))

# Create an empty list to store burst times
burst = []

# Loop to input burst time for each process
for i in range(n):
    bt = int(input(f"Enter burst time for P{i+1}: "))
    burst.append(bt)  # Add burst time to the list

# Create a list to store completion times, initialized with 0
completion = [0] * n

# Completion time of first process = its burst time
completion[0] = burst[0]

# Calculate completion time for remaining processes
for i in range(1, n):
    completion[i] = completion[i-1] + burst[i]
    # Completion time = previous completion time + current burst time

# Print table header with formatting
print(f"\n{'Process':<10}{'Burst':<10}{'Completion':<14}{'TAT':<10}{'WT'}")

# Initialize total Turnaround Time and Waiting Time
total_tat = total_wt = 0

# Loop to calculate Turnaround Time (TAT) and Waiting Time (WT)
for i in range(n):
    tat = completion[i]        # Since arrival time = 0, TAT = Completion Time
    wt  = tat - burst[i]       # Waiting Time = TAT - Burst Time
    
    # Add to totals for average calculation
    total_tat += tat
    total_wt  += wt
    
    # Print process details in table format
    print(f"P{i+1:<9}{burst[i]:<10}{completion[i]:<14}{tat:<10}{wt}")

# Calculate and print average Turnaround Time
print(f"\nAverage TAT = {total_tat/n:.2f}")

# Calculate and print average Waiting Time
print(f"Average WT  = {total_wt/n:.2f}")