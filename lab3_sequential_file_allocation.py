# ============================================================
#   Sequential (Contiguous) File Allocation Simulator
# ============================================================

# --- ANSI Color Codes ---
C_TITLE  = "\033[1;95m"
C_HEADER = "\033[1;96m"
C_SUCCESS= "\033[92m"
C_ERROR  = "\033[91m"
C_DISK   = "\033[1;93m"
RESET    = "\033[0m"

class SequentialDisk:
    def __init__(self, total_blocks):
        self.total_blocks = total_blocks
        # The disk array: 'None' means free, a string means it holds a file
        self.disk = [None] * total_blocks
        # Directory tracks the starting block and length of each file
        self.directory = {}

    def allocate(self, filename, length):
        """Automatically finds the first available contiguous space."""
        if filename in self.directory:
            print(f"{C_ERROR}Error: File '{filename}' already exists.{RESET}")
            return

        if length <= 0:
            print(f"{C_ERROR}Error: File length must be greater than 0.{RESET}")
            return

        # Search for 'length' consecutive free blocks
        start_block = -1
        consecutive_free = 0

        for i in range(self.total_blocks):
            if self.disk[i] is None:
                if consecutive_free == 0:
                    start_block = i
                consecutive_free += 1
                
                # If we found enough space, stop searching
                if consecutive_free == length:
                    break
            else:
                # Reset counter if we hit an occupied block
                consecutive_free = 0

        # Check if allocation is possible
        if consecutive_free == length:
            # Mark blocks as occupied
            for i in range(start_block, start_block + length):
                self.disk[i] = filename
            
            # Record in directory
            self.directory[filename] = {'start': start_block, 'length': length}
            print(f"{C_SUCCESS}Success: '{filename}' allocated from block {start_block} to {start_block + length - 1}.{RESET}")
        else:
            print(f"{C_ERROR}Error: Not enough contiguous space for '{filename}' ({length} blocks needed).{RESET}")

    def delete(self, filename):
        if filename not in self.directory:
            print(f"{C_ERROR}Error: File '{filename}' not found.{RESET}")
            return

        # Get file details
        start = self.directory[filename]['start']
        length = self.directory[filename]['length']

        # Free the blocks
        for i in range(start, start + length):
            self.disk[i] = None
        
        # Remove from directory
        del self.directory[filename]
        print(f"{C_SUCCESS}Success: File '{filename}' deleted. Blocks {start} to {start + length - 1} freed.{RESET}")

    def show_directory(self):
        print(f"\n{C_HEADER}{'='*40}")
        print(f"{'File Name':<15}{'Start Block':<15}{'Length'}")
        print(f"{'='*40}{RESET}")
        
        if not self.directory:
            print("Directory is empty.")
        else:
            for fname, details in self.directory.items():
                print(f"{fname:<15}{details['start']:<15}{details['length']}")
        print(f"{C_HEADER}{'='*40}{RESET}")

    def show_disk_status(self):
        print(f"\n{C_DISK}--- Disk Block Status ---{RESET}")
        display_str = ""
        for i in range(self.total_blocks):
            if self.disk[i] is None:
                display_str += "[ ] "
            else:
                display_str += f"[{self.disk[i]}] "
            
            # Print 10 blocks per line for readability
            if (i + 1) % 10 == 0:
                display_str += "\n"
                
        print(display_str)
        
        free_blocks = self.disk.count(None)
        print(f"{C_DISK}Total Free Blocks: {free_blocks} / {self.total_blocks}{RESET}\n")

# --- Main Execution ---
if __name__ == "__main__":
    print(f"{C_TITLE}{'='*50}")
    print(f"  Sequential File Allocation Simulator")
    print(f"{'='*50}{RESET}\n")

    try:
        n = int(input("Enter total number of disk blocks: "))
        my_disk = SequentialDisk(n)

        while True:
            print(f"\n{C_TITLE}--- Menu ---{RESET}")
            print("1. Allocate File (Auto-find space)")
            print("2. Delete File")

            print("3. Show Directory")
            print("4. Show Disk Status")
            print("5. Exit")
            
            choice = input("\nEnter your choice (1-5): ")
            
            if choice == '1':
                fname = input("Enter file name: ")
                length = int(input("Enter number of blocks needed: "))
                my_disk.allocate(fname, length)
            elif choice == '2':
                fname = input("Enter file name to delete: ")
                my_disk.delete(fname)
            elif choice == '3':
                my_disk.show_directory()
            elif choice == '4':
                my_disk.show_disk_status()
            elif choice == '5':
                print(f"{C_TITLE}Exiting simulator. Goodbye!{RESET}")
                break
            else:
                print(f"{C_ERROR}Invalid choice. Please try again.{RESET}")
    except ValueError:
        print(f"{C_ERROR}Error: Please enter valid integer values for blocks/length.{RESET}")