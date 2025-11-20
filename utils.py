# utils.py
import random
import time
import statistics

def generate_input(n, case='random', random_range=None, seed=None):
    """
    Genera una lista di n chiavi secondo il tipo 'case':
    - 'random'    : numeri uniformi in [0, random_range)
    - 'ascending' : 0,1,...,n-1
    - 'descending': n-1,...,1,0
    - 'repeated'  : valori presi in piccolo range (es. 0..9)
    """
    if seed is not None:
        random.seed(seed)
    if case == 'random':
        if random_range is None:
            random_range = max(1000, n * 10)
        return [random.randint(0, random_range - 1) for _ in range(n)]
    elif case == 'ascending':
        return list(range(n))
    elif case == 'descending':
        return list(range(n-1, -1, -1))
    elif case == 'repeated':
        # valori ripetuti in un piccolo intervallo
        r = max(2, min(10, n // 10))
        return [random.randint(0, r-1) for _ in range(n)]
    else:
        raise ValueError("case must be one of 'random','ascending','descending','repeated'")

def time_function(func, *args, **kwargs):
    """Esegue func(*args,**kwargs) e ritorna il tempo impiegato (in secondi) e il valore restituito."""
    start = time.perf_counter()
    result = func(*args, **kwargs)
    end = time.perf_counter()
    return end - start, result

def aggregate_times(times):
    """Dati una lista di tempi (float), restituisce dict con median, mean, stdev."""
    if len(times) == 0:
        return {"median": None, "mean": None, "stdev": None, "count": 0}
    median = statistics.median(times)
    mean = statistics.mean(times)
    stdev = statistics.stdev(times) if len(times) > 1 else 0.0
    return {"median": median, "mean": mean, "stdev": stdev, "count": len(times)}

def verify_extract_sequence(input_list, extract_sequence):
    """
    Verifica che extract_sequence rappresenti la lista input_list estratta in ordine
    non crescente (max-first). Ritorna True/False.
    """
    # L'estrazione completa dovrebbe produrre l'input ordinato in modo non crescente
    expected = sorted(input_list, reverse=True)
    return expected == list(extract_sequence)
