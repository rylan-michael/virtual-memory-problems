# Virtual Memory

* [Operating System Concepts 9e](https://www.os-book.com/OS9/)
* [Stack Overflow - Paging](https://www.quora.com/Whats-the-difference-between-page-and-page-frame)

#### Implementation of Page Replacement Algorithms.

Implement the counter-based implementation of the LRU algorithm. Also implement
the optimal page replacement algorithm. The main goal is to examine the impact 
of the number of frames on both the LRU and optimal algorithms by varying the 
number of frames. Investigate how the LRU algorithm performs in terms of the
number of page faults in comparison with the optimal algorithm.

**HOW**: Generate a random page-reference string where page numbers range from
0 to 9. The length of the reference string should be 10 characters. Apply the
random page-reference string to each algorithm, and record the number of page
faults incurred by each algorithm. Vary the number of frames from 1 to 7 and
repeat the experiment with the same reference string. Draw a graph that
illustrates the results. The x-axis, and y-axis of the graph should be the
number of frames, and the number of page faults, respectively.

#### Performance Evaluation of the LRU Algorithm

Evaluate the performance of the timer-based vs. stack-based LRU algorithm.
Measure and compare the running times of the algorithms.

**HOW**: Generate a random-reference string with a length of 500 characters
page numbers range from 0 to 20 (e.g. 0 2 18 12 20 1 ...). Measure the running
times of both timer-based and stack-based LRU algorithms with the random
reference string as input. Vary the number of frames from 1 to 10 and repeat the
experiment with the same reference string.

Here the running time is defined as the amount of time the algorithm takes to
complete processing the random reference string. Draw a graph that illustrates
the results. The x-axis and y-axis of the graph should be the number of frames,
and running time, respectively.

#### Quick Notes

* Physical - (RAM) An actual device
* Logical - (CPU Generated Address) A translation to a physical device
* Virtual - A simulation of a physical device

Paging: Break **physical memory** into fixed-sized blocks called **frames**
and break **logical memory** into blocks of the same size called **pages**.

Page is what you want to store and the page frame is where you want to store
the page.
* Page - logical addresses (addresses referred in a program)
* Page Frame - physical addresses (addresses present in RAM)