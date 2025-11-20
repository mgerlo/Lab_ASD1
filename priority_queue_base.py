# priority_queue_base.py

class PriorityQueue:
    """
    Interfaccia comune per tutte le implementazioni
    di code di priorità nel progetto.
    """
    def insert(self, key):
        """Inserisce un elemento con valore 'key'."""
        raise NotImplementedError("Metodo non implementato")

    def extract_max(self):
        """Rimuove e restituisce il valore massimo."""
        raise NotImplementedError("Metodo non implementato")

    def peek(self):
        """Restituisce il massimo senza rimuoverlo."""
        raise NotImplementedError("Metodo non implementato")

    def size(self):
        """Numero di elementi nella struttura."""
        raise NotImplementedError("Metodo non implementato")
