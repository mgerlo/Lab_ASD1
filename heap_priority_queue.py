# heap_priority_queue.py
#
# Implementazione di una coda di priorità basata su un max-heap binario.
# Il max-heap è rappresentato tramite una lista Python (array) dove:
# - l'elemento con priorità massima è in posizione 0
# - ogni nodo ha due figli in posizioni 2*i + 1 (sinistra) e 2*i + 2 (destra)
#
# Tutte le operazioni mantengono la proprietà di heap:
#   data[parent] >= data[left_child], data[parent] >= data[right_child]
#
# Complessità:
#   insert      = O(log n)
#   extract_max = O(log n)
#   peek        = O(1)
#   size        = O(1)


from priority_queue_base import PriorityQueue


class HeapPriorityQueue(PriorityQueue):

    def __init__(self):
        # Lista che rappresenta l'heap binario.
        # Inizialmente è vuota.
        self.data = []

    def size(self):
        """Restituisce il numero di elementi presenti nell'heap."""
        return len(self.data)

    def peek(self):
        """
        Restituisce il massimo senza rimuoverlo.
        L'elemento massimo si trova sempre in posizione 0.
        """
        if self.size() == 0:
            raise IndexError("peek from empty heap")
        return self.data[0]

    def insert(self, key):
        """
        Inserisce un nuovo elemento nel max-heap.
        1. Aggiunge l'elemento alla fine dell'array (foglia più a destra)
        2. Risale l'albero con heapify_up per ripristinare la proprietà di heap.
        Complessità: O(log n)
        """
        self.data.append(key)  # inserimento in fondo
        self._heapify_up(self.size() - 1)

    def extract_max(self):
        """
        Rimuove e restituisce l'elemento massimo (in radice).
        Procedura:
        1. Scambia la radice con l’ultimo elemento
        2. Rimuove l'ultimo elemento (che era la radice originale)
        3. Ripristina l'heap con heapify_down
        Complessità: O(log n)
        """
        n = self.size()
        if n == 0:
            raise IndexError("extract_max from empty heap")
        if n == 1:
            # caso speciale: un solo elemento
            return self.data.pop()

        # Scambia radice ↔ ultimo elemento
        self._swap(0, n - 1)

        # Rimuove l'ultimo elemento (che era la radice)
        max_val = self.data.pop()

        # Ripristina la proprietà di heap partendo dalla radice
        self._heapify_down(0)

        return max_val

    # -------------------------------------------------------------------
    # METODI INTERNI (helper)
    # -------------------------------------------------------------------

    def _parent(self, i):
        """Restituisce l'indice del nodo padre."""
        return (i - 1) // 2

    def _left(self, i):
        """Restituisce l'indice del figlio sinistro."""
        return 2 * i + 1

    def _right(self, i):
        """Restituisce l'indice del figlio destro."""
        return 2 * i + 2

    def _swap(self, i, j):
        """Scambia gli elementi in posizione i e j."""
        self.data[i], self.data[j] = self.data[j], self.data[i]

    def _heapify_up(self, i):
        """
        Ripristina la proprietà di max-heap risalendo l'albero.
        Usato dopo l'inserimento.
        Finché il nodo è maggiore del padre, lo scambiamo verso l'alto.
        """
        while i > 0:
            p = self._parent(i)
            if self.data[i] > self.data[p]:
                self._swap(i, p)
                i = p
            else:
                break  # proprietà dell'heap ristabilita

    def _heapify_down(self, i):
        """
        Ripristina la proprietà di max-heap scendendo nell'albero.
        Usato dopo extract_max.
        Confronta il nodo con i suoi figli e lo sposta verso il più grande.
        """
        n = self.size()
        while True:
            left = self._left(i)
            right = self._right(i)
            largest = i  # assume che il nodo corrente sia il più grande

            # controlla figlio sinistro
            if left < n and self.data[left] > self.data[largest]:
                largest = left

            # controlla figlio destro
            if right < n and self.data[right] > self.data[largest]:
                largest = right

            # se un figlio è più grande, scambia
            if largest != i:
                self._swap(i, largest)
                i = largest
            else:
                break  # l'heap è corretto
