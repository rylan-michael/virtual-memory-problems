import random


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


class LRUClock:
    """Counter for keeping time inside of the LRU page-replacement algorithm.

    tick: keeps track of how much time has passed.
    increment(): increases tick by 1.
    """
    def __init__(self):
        self.tick = 0

    def increment(self):
        self.tick += 1


def counter_lru_page_replacement(reference_string, memory_size):
    """Counter-based LRU page-replacement algorithm.

    Use the recent past as an approximation for the near future. Replace the
    page that has not been used for the longest period of time. Associates a
    page with time of its last use.
    We use counters to implement the algorithm. The clock is incremented for
    every memory reference. Whenever a reference to a page is made, the contents
    of the clock register are copied to the time-of-use filed in the page-table
    entry for that page. (see pg. 416)
    :return:
    """
    memory = [None for x in range(memory_size)]
    clock = LRUClock()
    for c in reference_string:
        frame = {"#": c, "TOU": clock.tick}  # Frame number, time of use
        clock.increment()
        # print(c)
        # Would be easiest to check if frame were already in memory by using
        # if frame in memory:, but we need to ignore age comparison.
        if None in memory:  # Load frame
            memory[memory.index(None)] = frame
        else:
            loaded = False
            for f in memory:
                if f["#"] is frame["#"]:
                    # print("frame in memory")
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
                # print("page replaced")
        # print(memory)


def opt_page_replacement(reference_str):
    """Optimal page-replacement algorithm.

    Replace the page that will not be used for the longest period of time. Use
    of this page-replacement algorithm guarantees the lowest possible page-fault
    rate for a fixed number of frames. (see pg. 414)
    :param reference_str: string
    :return:
    """

    return False


# counter_lru_page_replacement(rand_page_ref_str(), 1)
# Static reference str used by book to test algorithm correctness
counter_lru_page_replacement("70120304230321201701", 3)