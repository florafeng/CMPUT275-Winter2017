import sys
from minheap import MinHeap
from collections import Counter


def compute_bit(heap):
    while not len(heap) == 1:
        array1 = heap.pop_min()
        array2 = heap.pop_min()
        heap.add(array1[0] + array2[0], array1[0] + array2[0] + array1[1] + array2[1])

    array = heap.pop_min()
    return array[1]

    # if len(heap) == 1:
    #     # print("1111111")
    #     array = heap.pop_min()
    #     print(array[1])
    #     return array[1]
    # else:
    #     # print("22222")
    #     array1 = heap.pop_min()
    #     array2 = heap.pop_min()
    #     heap.add(array1[0] + array2[0], array1[0] + array2[0] + array1[1] + array2[1])
    #
    #     print(array1[0] + array2[0] + array1[1] + array2[1])
    #     compute_bit(heap)

def huff_cost(s):

    """
    Compute characteristics of the optimal  Huffman encoding of the string s.

    Input:
        Any string s.  But to be interesting s needs to have at least 2
        different kinds of characters.

    Output:
        Returns the tuple
            (num_distinct_chars, total_num_chars, total_num_bits)
        num_distinct_chars - count of the number of distinct chars in s
        total_num_chars - len(s)
        total_num_bits - the total number of bits needed for an optimal
            Huffman encoding of s

    Note: The algorithm simulates the construction of the optimal Huffman
        tree, but just keeps track of the bits used to encode s.
    """

    # get the character frequencies
    freq = Counter()
    freq.update(s)

    num_distinct_chars = len(freq)
    total_num_chars = len(s)
    total_num_bits = None

    if num_distinct_chars == 0:
        return (0, 0, 0)

    if num_distinct_chars == 1:
        return (1, len(s), 0)

    # YOUR CODE GOES HERE
    heap = MinHeap()
    for k, v in freq.items():
        heap.add(v, 0)

    total_num_bits = compute_bit(heap)

    return (num_distinct_chars, total_num_chars, total_num_bits)

def main():
    for s in sys.stdin:
        s = s.strip()

        (num_distinct_chars, total_num_chars, total_num_bits) = huff_cost(s)

        print("'{}'".format(s))
        print("{} {} {}".format(num_distinct_chars, total_num_chars, total_num_bits))

main()
