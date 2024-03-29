# Given ‘M’ sorted arrays, find the smallest range that includes at least one 
# number from each of the ‘M’ lists.

# Example:
# Input: L1=[1, 5, 8], L2=[4, 12], L3=[7, 8, 10]
# Output: [4, 7]
# Explanation: The range [4, 7] includes 5 from L1, 4 from L2 and 7 from L3.

from heapq import heappush, heappop
from math import inf

def find_smallest_range(lists):
    min_heap = []
    range_start, range_end = 0, inf
    current_max = -inf
    for l in lists:
        heappush(min_heap, (l[0], 0, l))
        current_max = max(current_max, l[0])

    while len(min_heap) == len(lists):
        num, i, arr = heappop(min_heap)
        if range_end - range_start > current_max - num:
            range_end = current_max
            range_start = num
        if len(arr) > i + 1:
            heappush(min_heap, (arr[i+1], i+1, arr))
            current_max = max(current_max, arr[i+1])

    return [range_start, range_end]


def main():
    print("Smallest range is: " +
        str(find_smallest_range([[1, 5, 8], [4, 12], [7, 8, 10]])))

main()