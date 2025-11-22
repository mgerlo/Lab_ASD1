# linked_list_priority_queue.py
#
# Implementazione di una coda di priorità con LISTA CONCATENATA NON ORDINATA.
#
# Caratteristiche principali:
# - Insert: O(1) perché inseriamo sempre in testa.
# - Peek (trovare il massimo): O(n) perché dobbiamo scorrere tutta la lista.
# - Extract_max: O(n) perché dobbiamo cercare il massimo e poi rimuoverlo.
#
# Questa implementazione è molto efficiente per molte "insert"
# ma inefficiente per molte "extract_max".


from priority_queue_base import PriorityQueue


class Node:
    """
    Un nodo della lista concatenata.
    Contiene:
    - key  = valore (intero) memorizzato
    - next = puntatore al nodo successivo (o None)
    """

    def __init__(self, key, next=None):
        self.key = key
        self.next = next


class LinkedListPriorityQueue(PriorityQueue):

    def __init__(self):
        """
        Inizializza una lista concatenata vuota.
        head → None
        n = numero di elementi
        """
        self.head = None
        self.n = 0

    def size(self):
        """Restituisce il numero di elementi presenti nella struttura."""
        return self.n

    def insert(self, key):
        """
        Inserisce un nuovo elemento in TESTA alla lista.

        Complessità: O(1)
        Perché:
        - creiamo un nodo
        - il nuovo nodo diventa il nuovo head
        """
        new_node = Node(key, self.head)
        self.head = new_node
        self.n += 1

    def peek(self):
        """
        Restituisce il valore massimo SENZA rimuoverlo.

        Complessità: O(n)
        Perché dobbiamo scorrere tutta la lista
        confrontando tutte le chiavi.
        """
        if self.head is None:
            raise IndexError("peek from empty list")

        current = self.head
        max_val = current.key

        # Scandisci tutta la lista e cerca il valore massimo
        while current is not None:
            if current.key > max_val:
                max_val = current.key
            current = current.next

        return max_val

    def extract_max(self):
        """
        Rimuove e restituisce l'elemento con valore massimo.

        Strategia:
        1. Usiamo 'peek' per trovare il valore massimo → O(n)
        2. Scorriamo la lista una seconda volta per rimuovere
           il primo nodo che contiene tale valore → O(n)

        Complessità totale: O(n)
        (Due passate separate, ma sempre O(n))
        """
        if self.head is None:
            raise IndexError("extract_max from empty list")

        # Primo passaggio: individua il valore massimo
        max_val = self.peek()

        # Secondo passaggio: trova e rimuovi il nodo con quel valore
        current = self.head
        prev = None

        while current is not None:
            # Quando troviamo il nodo contenente max_val...
            if current.key == max_val:

                # Caso 1: il massimo è in testa
                if prev is None:
                    self.head = current.next
                else:
                    # Caso 2: il massimo è in mezzo/in fondo
                    prev.next = current.next

                self.n -= 1
                return max_val

            # Avanza nella lista
            prev = current
            current = current.next

        # Se arriviamo qui significa che c'è un problema logico,
        # perché max_val dovrebbe sempre essere trovato.
        raise RuntimeError("unexpected error in extract_max")
