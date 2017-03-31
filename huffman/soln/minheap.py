class MinHeap:

    def __init__(self):
        self._array = []

    def add(self, key, value):
        self._array.append((key, value))
        self.fix_heap_up(len(self._array)-1)

    def pop_min(self):
        if not self._array:
            raise RuntimeError("Attempt to call pop_min on empty heap")
        retval = self._array[0]
        self._array[0] = self._array[-1]
        del self._array[-1]
        if self._array:
            self.fix_heap_down(0)
        return retval

    def fix_heap_up(self, i):
        if self.isroot(i):
            return
        p = self.parent(i)
        if self._array[i][0] < self._array[p][0]:
            self.swap(i, p)
            self.fix_heap_up(p)

    def swap(self, i, j):
        self._array[i], self._array[j] = \
            self._array[j], self._array[i]

    def isroot(self, i):
        return i == 0

    def isleaf(self, i):
        return self.lchild(i) >= len(self._array)

    def lchild(self, i):
        return 2*i+1

    def rchild(self, i):
        return 2*i+2

    def parent(self, i):
        return (i-1)//2

    def min_child_index(self, i):
        l = self.lchild(i)
        r = self.rchild(i)
        retval = l
        if r < len(self._array) and self._array[r][0] < self._array[l][0]:
            retval = r
        return retval

    def isempty(self):
        return len(self._array) == 0

    def length(self):
        return len(self._array)

    def fix_heap_down(self, i):
        if self.isleaf(i):
            return

        j = self.min_child_index(i)
        if self._array[i][0] > self._array[j][0]:
            self.swap(i, j)
            self.fix_heap_down(j)

    # Some stnadard collection interfaces

    # So the len() function will work.
    def __len__(self):
        return len(self._array)

    # Iterator
    def __iter__(self):
        return iter(self._array)

    def __next__(self):
        return (self._array).__next__


def test_minheap():
    # testing against the heapq module
    import random
    import heapq
    tracing = False

    def test_pop(heap, ourheap):
        if len(heap) == 0 and ourheap.isempty():
            return
        item = heapq.heappop(heap)
        item2 = our_heap.pop_min()
        if item != item2[0]:
            raise RuntimeError("Unequal elements %s!=%s" % (item, item2[0]))
        tracing and print("Popped", item)

    for n in range(100):  # length
        print("Testing for length %s" % n)
        for i in range(100):  # random instances
            s = [random.randrange(-10, 10) for j in range(n)]
            heap = []
            our_heap = MinHeap()
            for x in s:
                heapq.heappush(heap, x)
                our_heap.add(x, None)
                tracing and print("Added ", x)
                if random.uniform(0, 1) < 0.2:
                    tracing and print("Popping")
                    test_pop(heap, our_heap)
            while heap:
                tracing and print("Popping")
                test_pop(heap, our_heap)
            if not our_heap.isempty():
                raise RuntimeError("Too few elements")
    print("Test finished")

if __name__ == '__main__':
    test_minheap()
