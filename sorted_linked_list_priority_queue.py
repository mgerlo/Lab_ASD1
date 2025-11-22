# sorted_linked_list_priority_queue.py
#
# Implementazione di una coda di priorità usando LISTA CONCATENATA ORDINATA.
#
# In questa versione la lista è mantenuta sempre in ordine DECRESCENTE:
#     head -> valore massimo
#
# Caratteristiche importanti:
# - Insert: O(n) perché dobbiamo trovare la posizione corretta.
# - Peek: O(1) il massimo è sempre in testa!
# - Extract_max: O(1) rimuoviamo la testa.
#
# Questa struttura è ottima se facciamo tante "extract_max" e relativamente
# poche "insert", perché inserire è lento ma estrarre è velocissimo.


from priority_queue_base import PriorityQueue


class Node:
    """
    Nodo della lista concatenata.
    - key  = valore memorizzato
    - next = puntatore al prossimo nodo
    """
    def __init__(self, key, next=None):
        self.key = key
        self.next = next


class SortedLinkedListPriorityQueue(PriorityQueue):

    def __init__(self):
        """
        Inizializza una lista concatenata ordinata.
        head → nodo con valore massimo
        """
        self.head = None
        self.n = 0

    def size(self):
        """Restituisce il numero di elementi nella coda di priorità."""
        return self.n

    def peek(self):
        """
        Restituisce il valore massimo senza rimuoverlo.

        Poiché la lista è ORDINATA in modo DECRESCENTE,
        il massimo è sempre il primo elemento.

        Complessità: O(1)
        """
        if self.head is None:
            raise IndexError("peek from empty sorted list")
        return self.head.key

    def insert(self, key):
        """
        Inserisce un valore mantenendo la lista ordinata in senso decrescente.

        Strategia:
        - Se la lista è vuota, o la chiave è il nuovo massimo, inseriamo in testa.
        - Altrimenti cerchiamo la posizione corretta scorrendo la lista.

        Complessità: O(n)
        Perché nel caso peggiore dobbiamo scorrere tutta la lista.
        """
        new_node = Node(key)

        # Caso 1: lista vuota o key è >= del valore massimo
        # → inserimento in testa O(1)
        if self.head is None or key >= self.head.key:
            new_node.next = self.head
            self.head = new_node
            self.n += 1
            return

        # Caso 2: scorre la lista finché non trova la posizione corretta
        prev = self.head
        current = self.head.next

        # Scorri finché:
        # - non finisce la lista
        # - e il nodo corrente ha un valore > key (per mantenere ordine DECRESCENTE)
        while current is not None and current.key > key:
            prev = current
            current = current.next

        # Inserisce new_node tra prev e current
        prev.next = new_node
        new_node.next = current
        self.n += 1

    def extract_max(self):
        """
        Rimuove e restituisce il massimo dalla lista.

        Poiché la lista è in ordine DECRESCENTE, il massimo
        si trova SEMPRE in testa → O(1)

        Complessità: O(1)
        """
        if self.head is None:
            raise IndexError("extract_max from empty sorted list")

        max_val = self.head.key
        self.head = self.head.next
        self.n -= 1
        return max_val
