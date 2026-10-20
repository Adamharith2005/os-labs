import threading
import time
import random

NUM_PHILOSOPHERS = 7
THINK_TIME       = 2
EAT_TIME         = 2
ROUNDS           = 2

chopstick = [threading.Lock() for _ in range(NUM_PHILOSOPHERS)]
print_lock = threading.Lock()
finished_sequence = []
sequence_lock = threading.Lock()

def print_state(id, action):
    with print_lock:
        print(f"Philosopher {id} is {action}")

def philosopher(id):
    left  = id
    right = (id + 1) % NUM_PHILOSOPHERS

    for round in range(ROUNDS):
        # --- THINKING ---
        print_state(id, "thinking")
        time.sleep(random.randint(1, THINK_TIME))

        # --- HUNGRY ---
        print_state(id, "hungry")

        if id % 2 == 0:
            chopstick[right].acquire()
            print_state(id, "picked up RIGHT chopstick")
            chopstick[left].acquire()
            print_state(id, "picked up LEFT  chopstick")
        else:
            chopstick[left].acquire()
            print_state(id, "picked up LEFT  chopstick")
            chopstick[right].acquire()
            print_state(id, "picked up RIGHT chopstick")

        # --- EATING ---
        print_state(id, "eating")
        time.sleep(random.randint(1, EAT_TIME))

        # --- PUT DOWN ---
        chopstick[left].release()
        chopstick[right].release()
        print_state(id, "put down both chopsticks")

    # --- Finishing order ---
    with sequence_lock:
        finished_sequence.append(id)
    
    with print_lock:
        print(f"*** Philosopher {id} has finished all {ROUNDS} rounds. ***")

if __name__ == "__main__":
    random.seed(42)
    print("=== Dining Philosophers Simulation ===")
    
    threads = []
    for i in range(NUM_PHILOSOPHERS):
        t = threading.Thread(target=philosopher, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # --- NEW: Display the Sequence ---
    print("\n--------------------------------------")
    print("Simulation complete. No deadlock occurred.")
    print(f"Finishing Order: {' -> '.join(f'P{pid}' for pid in finished_sequence)}")
    print("--------------------------------------")