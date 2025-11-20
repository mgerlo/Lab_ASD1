# linked_list_priority_queue.py

from priority_queue_base import PriorityQueue

class Node:
    def __init__(self, key, next=None):
        self.key = key
        self.next = next


class LinkedListPriorityQueue(PriorityQueue):

    def __init__(self):
        self.head = None
        self.n = 0

    def size(self):
        return self.n

    def insert(self, key):
        """Inserisce in testa (O(1))."""
        new_node = Node(key, self.head)
        self.head = new_node
        self.n += 1

    def peek(self):
        """Restituisce il massimo (O(n))."""
        if self.head is None:
            raise IndexError("peek from empty list")

        current = self.head
        max_val = current.key

        while current is not None:
            if current.key > max_val:
                max_val = current.key
            current = current.next

        return max_val

    def extract_max(self):
        """Rimuove il massimo dalla lista (O(n))."""
        if self.head is None:
            raise IndexError("extract_max from empty list")

        # prima passata: trova il valore massimo
        max_val = self.peek()

        # seconda passata: rimuovi il nodo con max_val
        current = self.head
        prev = None

        while current is not None:
            if current.key == max_val:
                if prev is None:
                    self.head = current.next
                else:
                    prev.next = current.next
                self.n -= 1
                return max_val

            prev = current
            current = current.next

        # non dovrebbe mai succedere
        raise RuntimeError("unexpected error in extract_max")
