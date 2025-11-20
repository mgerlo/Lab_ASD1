# sorted_linked_list_priority_queue.py

from priority_queue_base import PriorityQueue

class Node:
    def __init__(self, key, next=None):
        self.key = key
        self.next = next


class SortedLinkedListPriorityQueue(PriorityQueue):

    def __init__(self):
        self.head = None
        self.n = 0

    def size(self):
        return self.n

    def peek(self):
        if self.head is None:
            raise IndexError("peek from empty sorted list")
        return self.head.key  # massimo in testa (lista decrescente)

    def insert(self, key):
        """
        Inserimento mantenendo l'ordine decrescente.
        O(n)
        """
        new_node = Node(key)

        # Caso 1: lista vuota o key è il nuovo massimo
        if self.head is None or key >= self.head.key:
            new_node.next = self.head
            self.head = new_node
            self.n += 1
            return

        # Caso 2: cerca la posizione corretta
        prev = self.head
        current = self.head.next

        while current is not None and current.key > key:
            prev = current
            current = current.next

        # Inserisci tra prev e current
        prev.next = new_node
        new_node.next = current
        self.n += 1

    def extract_max(self):
        """O(1): rimuove il primo nodo."""
        if self.head is None:
            raise IndexError("extract_max from empty sorted list")
        max_val = self.head.key
        self.head = self.head.next
        self.n -= 1
        return max_val
