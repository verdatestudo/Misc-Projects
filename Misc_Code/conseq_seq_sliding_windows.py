'''
Sliding Window - contiguous subsequence

Last Updated: 2016-Nov-30
First Created: 2016-Nov-29
Python 3.5
Chris

# http://stackoverflow.com/questions/6822725/rolling-or-sliding-window-iterator-in-python
'''

from collections import deque

def window_no_import(seq, n=2):
    '''
    Sliding window without using import.
    '''
    my_list = seq
    for num in range(1, len(my_list) + 1): # size of window starting with 1, finishing with window length == len(list)
        for idx in range(len(my_list)): # setting start position of window
            if idx+num <= len(my_list): # as we get towards the end of list we won't be getting a full window, so don't include those.
                yield my_list[idx:idx+num]

a = window_no_import([1, 2, 3, 4, 5], 2)
print(a)
print([item for item in a])

def window(seq, n=3):
    '''
    Takes seq, a sequence (list), and n, an int for length of the sliding window.
    e.g ([1, 2, 3, 4], 3) returns (1, 2, 3) and (2, 3, 4).
    Triangular progression, n * (n+1) / 2 or O(n**2).
    '''
    it = iter(seq)
    win = deque((next(it, None) for _ in range(n)), maxlen=n)
    yield list(win)
    #append = win.append
    for e in it:
        win.append(e)
        yield list(win)

def max_contig_sum(L):
    """ L, a list of integers, at least one positive
    Returns the maximum sum of a contiguous subsequence in L """

    # get all possible sliding windows of all possible lengths.
    options = []
    for n in range(len(L) + 1):
        options.extend([item for item in window(L, n)])

    # return the max sum from the possible options.
    return sum(max(options, key=sum))

def testing():
    '''
    testing
    '''
    print(max_contig_sum([1, 2, 3]), 6)
    print(max_contig_sum([10, -8, 2]), 10)
    print(max_contig_sum([5, -2, 7]), 10)
    print(max_contig_sum([1, 2, 3, -10, 40, -50, 100]), 100)

a = window([1, 2, 3, 4, 5], 2)
for item in a:
    print(item)

#testing()
