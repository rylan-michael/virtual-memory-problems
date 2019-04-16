import random
import pandas as pd
import matplotlib.pyplot as plt


def rand_page_ref_str():
    """Generate a random reference string.

    A reference string is used for evaluating performance of page replacement
    algorithms. We test the algorithm by running it on a particular string of
    memory references called a reference string. (see pg. 412)
    The reference string is 10 characters long with each character representing
    a frame number.
    """
    characters = "0123456789"
    return ''.join(random.choice(characters) for i in range(10))


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
                    # print("Replaced frame that would'nt be used again.")
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
    ref_str = rand_page_ref_str()
    # data_set = {"algorithm": [], "memory size": [], "page fault count": []}
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
    # for i in range(1, 8):
    #     (ref_len, mem_size, page_fault_count) = counter_lru_page_replacement(ref_str, i)
    #     data_set["algorithm"].append("LRU")
    #     data_set["memory size"].append(mem_size)
    #     data_set["page fault count"].append(page_fault_count)
    #     (ref_len, mem_size, page_fault_count) = opt_page_replacement(ref_str, i)
    #     data_set["algorithm"].append("OPT")
    #     data_set["memory size"].append(mem_size)
    #     data_set["page fault count"].append(page_fault_count)

    # df = pd.DataFrame(data=data_set)
    # df.sort_values("memory size", axis=0, inplace=True)
    # print(df)
    # df.pivot(index="algorithm", columns="memory size", values="page fault count").plot(kind="bar")

    # df = pd.DataFrame(data=data_set)
    # print(df)
    #
    # df.plot.bar(x="memory size", y="page fault count")
    # plt.show()
    # data_set = {"mem_size_lru": [], "page_fault_count_lru": [],
    #             "mem_size_opt": [], "page_fault_count_opt": []}
    #
    # for i in range(1, 8):
    #     (ref_len, mem_size, page_fault_count) = counter_lru_page_replacement(ref_str, i)
    #     data_set["mem_size_lru"].append(mem_size)
    #     data_set["page_fault_count_lru"].append(page_fault_count)
    #     (ref_len, mem_size, page_fault_count) = opt_page_replacement(ref_str, i)
    #     data_set["mem_size_opt"].append(mem_size)
    #     data_set["page_fault_count_opt"].append(page_fault_count)
    #
    # df = pd.DataFrame(data=data_set)
    # # df.pivot(index="channel")
    # fig = plt.figure(figsize=(12, 7))
    # fig.suptitle(f"Page Replacement Algorithm Performance")
    # ax = fig.add_subplot(111)
    # ax.set_title("Counter-based LRU Implementation")
    # ax.text(6, 8, "ref_str: {0}".format(ref_str),
    #         bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})
    # ax.set_xlabel("Number of Frames")
    # ax.set_ylabel("Number of Page Faults")
    #
    # positions = [x for x in range(1, 8)]
    # plt.bar(positions, df["page_fault_count_lru"].data.obj, width=0.7, align="center")
    # # plt.bar(positions, df["page_fault_count_opt"].data.obj, width=0.7, align="center")
    # plt.xticks(positions, df["mem_size_lru"].data.obj)
    # plt.show()


analyze_page_replacement_performance()

# opt_page_replacement(rand_page_ref_str(), 5)
