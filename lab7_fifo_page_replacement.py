

def fifo(pages, num_frames):
    # this list holds the pages in memory right now
    frames = []
    page_faults = 0

    print("Page\tFrames\t\t\tStatus")
    print("-" * 40)

    for page in pages:
        # thischecks if page is already in memory
        if page in frames:
            status = "Hit"
        else:
            status = "Page Fault"
            page_faults += 1

            # if memory is full, remove the oldest page ,first one that came in
            if len(frames) == num_frames:
                frames.pop(0)

            # add the new page
            frames.append(page)

        print(f"{page}\t{frames}\t\t{status}")

    print("-" * 40)
    print(f"Total Page Faults: {page_faults}")


# get input from user
pages = list(map(int, input("Enter reference string (space separated): ").split()))
num_frames = int(input("Enter number of frames: "))

fifo(pages, num_frames)
