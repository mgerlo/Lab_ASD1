# priority_queue_base.py

class PriorityQueue:
    """
    Classe base (interfaccia astratta) per tutte le implementazioni
    di una coda di priorità.

    Non contiene logica, ma definisce i metodi che tutte le
    implementazioni concrete devono avere.
    In Python non abbiamo interfacce vere, ma usiamo questa tecnica.
    """

    def insert(self, key):
        """
        Inserisce un elemento con valore 'key' all'interno della coda di priorità.

        Metodo astratto: deve essere implementato nelle sottoclassi.
        """
        raise NotImplementedError("Metodo non implementato")

    def extract_max(self):
        """
        Rimuove e restituisce il valore massimo contenuto nella coda di priorità.

        Metodo astratto: deve essere implementato nelle sottoclassi.
        """
        raise NotImplementedError("Metodo non implementato")

    def peek(self):
        """
        Restituisce il massimo senza rimuoverlo dalla struttura.

        Utile per controllare l'elemento prioritario corrente.
        """
        raise NotImplementedError("Metodo non implementato")

    def size(self):
        """
        Restituisce il numero di elementi attualmente presenti nella struttura.
        """
        raise NotImplementedError("Metodo non implementato")
