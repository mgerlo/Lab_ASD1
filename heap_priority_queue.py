# heap_priority_queue.py

from priority_queue_base import PriorityQueue

class HeapPriorityQueue(PriorityQueue):

    def __init__(self):
        self.data = []   # array che rappresenta l'heap

    def size(self):
        return len(self.data)

    def peek(self):
        if self.size() == 0:
            raise IndexError("peek from empty heap")
        return self.data[0]

    def insert(self, key):
        """Inserisce un nuovo elemento nel max-heap."""
        self.data.append(key)
        self._heapify_up(self.size() - 1)

    def extract_max(self):
        """Rimuove e restituisce il massimo (in radice)."""
        n = self.size()
        if n == 0:
            raise IndexError("extract_max from empty heap")
        if n == 1:
            return self.data.pop()

        # Scambia radice <-> ultimo elemento
        self._swap(0, n - 1)
        max_val = self.data.pop()
        self._heapify_down(0)
        return max_val

    # --- METODI INTERNI ---

    def _parent(self, i):
        return (i - 1) // 2

    def _left(self, i):
        return 2 * i + 1

    def _right(self, i):
        return 2 * i + 2

    def _swap(self, i, j):
        self.data[i], self.data[j] = self.data[j], self.data[i]

    def _heapify_up(self, i):
        """Ripristina la proprietà di heap risalendo l'albero."""
        while i > 0:
            p = self._parent(i)
            if self.data[i] > self.data[p]:
                self._swap(i, p)
                i = p
            else:
                break

    def _heapify_down(self, i):
        """Ripristina la proprietà di heap scendendo nell'albero."""
        n = self.size()
        while True:
            left = self._left(i)
            right = self._right(i)
            largest = i

            if left < n and self.data[left] > self.data[largest]:
                largest = left
            if right < n and self.data[right] > self.data[largest]:
                largest = right

            if largest != i:
                self._swap(i, largest)
                i = largest
            else:
                break
