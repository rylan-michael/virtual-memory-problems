import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
import time


def rand_page_ref_str(page_numbers, reference_length):
    """Generate a random reference string.

    A reference string is used for evaluating performance of page replacement
    algorithms. We test the algorithm by running it on a particular string of
    memory references called a reference string. (see pg. 412)
    The reference string is 10 characters long with each character representing
    a frame number.
    """
    return [random.choice(range(page_numbers)) for i in range(reference_length)]


def counter_lru_page_replacement(reference_string, memory_size):
    """Counter-based LRU page-replacement algorithm.

    Use the recent past as an approximation for the near future. Replace the
    page that has not been used for the longest period of time. Associates a
    page with time of its last use.
    We use counters to implement the algorithm. The clock is incremented for
    every memory reference. Whenever a reference to a page is made, the contents
    of the clock register are copied to the time-of-use filed in the page-table
    entry for that page. (see pg. 416)
    :return: tuple of reference_string length, allocated memory space for page
             frames and the number of page fault occurrences.
    """
    class LRUClock:
        """Counter for keeping time inside of the LRU page-replacement algorithm.

        tick: keeps track of how much time has passed.
        increment(): increases tick by 1.
        """
        def __init__(self):
            self.tick = 0

        def increment(self):
            self.tick += 1

    page_fault_count = 0
    memory = [None for x in range(memory_size)]
    clock = LRUClock()
    for c in reference_string:
        frame = {"#": c, "TOU": clock.tick}  # Frame number, time of use
        clock.increment()
        # Would be easiest to check if frame were already in memory by using
        # if frame in memory:, but we need to ignore age comparison.

        # Check if the frame is already loaded into memory. Since frames are
        # loaded serially, if we hit a None element then that means the array
        # is empty moving forward and won't contain the frame we are looking for.
        if None in memory:
            # Checks for page faults when the memory isn't full.
            # The frame could already be loaded.
            for f in memory:
                if f is None:  # Frame isn't loaded into memory
                    page_fault_count += 1
                    memory[memory.index(None)] = frame
                    break
                elif f["#"] is frame["#"]:  # Frame is loaded
                    # Since frame is already loaded, update the time value.
                    index = memory.index(f)
                    memory[index] = frame
                    break
        else:
            loaded = False
            for f in memory:
                if f["#"] is frame["#"]:  # If frame in memory
                    memory[memory.index(f)] = frame
                    loaded = True
            if not loaded:
                # find the oldest frame and replace it with the current frame
                oldest_frame = None
                index = 0
                for f in memory:
                    if oldest_frame is None:
                        oldest_frame = f
                    elif f["TOU"] < oldest_frame["TOU"]:
                        oldest_frame = f
                    index = memory.index(oldest_frame)
                memory[index] = frame
                page_fault_count += 1
    return len(reference_string), memory_size, page_fault_count


def stack_lru_page_replacement(reference_string, memory_size):
    frame_stack = deque(maxlen=memory_size)
    page_fault_count = 0
    for c in reference_string:
        if c in frame_stack:
            # If the frame is in stack, move to top of stack.
            frame_stack.remove(c)
            frame_stack.append(c)
        elif len(frame_stack) < memory_size:
            # There is room on the stack to add frame.
            frame_stack.append(c)
            page_fault_count += 1
        else:
            # There is no room on stack, replace frame.
            frame_stack.popleft()
            frame_stack.append(c)
            page_fault_count += 1
    return len(reference_string), memory_size, page_fault_count


def opt_page_replacement(reference_str, memory_size):
    """Optimal page-replacement algorithm.

    Replace the page that will not be used for the longest period of time. Use
    of this page-replacement algorithm guarantees the lowest possible page-fault
    rate for a fixed number of frames. (see pg. 414)
    """
    memory = [None for x in range(memory_size)]

    # Check loaded frames for page existence.
    # If page not in a loaded frame then load in frame
        # If available memory, load frame
        # Else replace frame that wont be used longest time
    page_fault_count = 0
    unmodified_ref_str = reference_str
    for page in reference_str:
        reference_str = reference_str[1:]
        if page in memory:  # Frame exists.
            pass
        elif None in memory:  # Load frame.
            page_fault_count += 1
            index = memory.index(None)
            memory[index] = page
        else:  # Replace frame.
            page_fault_count += 1
            rank_dict = {}
            loaded = False
            for p in memory:  # Is there any page in memory that won't be used again?
                if p not in reference_str:
                    loaded = True
                    index = memory.index(p)
                    memory[index] = page
                    break
                else:  # Give each loaded frame a rank.
                    index = reference_str.index(p)
                    rank_dict[p] = index
            if not loaded:
                least_active = max(rank_dict)
                index = memory.index(least_active)
                memory[index] = page
    return len(unmodified_ref_str), memory_size, page_fault_count


def analyze_page_replacement_performance():
    ref_str = rand_page_ref_str(page_numbers=10, reference_length=10)
    data_set = {"LRU": [], "OPT":  []}
    index = []
    for i in range(1, 8):
        (ref_len, mem_size, page_fault_count) = counter_lru_page_replacement(ref_str, i)
        data_set["LRU"].append(page_fault_count)
        (ref_len, mem_size, page_fault_count) = opt_page_replacement(ref_str, i)
        data_set["OPT"].append(page_fault_count)
        index.append(i)
    df = pd.DataFrame(data=data_set, index=index)
    ax = df.plot.bar(rot=0)
    plt.suptitle(f"Page Replacement Algorithm Performance")
    ax.text(4, 7, "ref_str: {0}".format(ref_str),
            bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})
    ax.set_xlabel("Number of Frames")
    ax.set_ylabel("Number of Page Faults")
    plt.show()


def analyze_lru_runtime_performance():
    reference_string = rand_page_ref_str(page_numbers=20, reference_length=50000)
    data_set = {"counter": [], "stack": []}
    index = []
    for i in range(1, 11):
        index.append(i)
        time_start = time.time()
        counter_lru_page_replacement(reference_string, i)
        time_end = time.time()
        data_set["counter"].append(time_end - time_start)
        time_start = time.time()
        stack_lru_page_replacement(reference_string, i)
        time_end = time.time()
        data_set["stack"].append(time_end - time_start)

    df = pd.DataFrame(data=data_set, index=index)
    lines = df.plot.line()
    lines.set_xlabel("Number of Frames")
    lines.set_ylabel("Running Time")
    lines.set_yticklabels([])
    plt.suptitle(f"LRU Runtime Performance Comparison")

    plt.show()


analyze_page_replacement_performance()
analyze_lru_runtime_performance()
