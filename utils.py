# utils.py
#
# Questo modulo contiene funzioni di utilità utilizzate
# dai programmi di test e dagli script di misurazione.
#
# Include:
# - generazione di input per gli esperimenti (varie forme)
# - misurazione dei tempi di esecuzione di funzioni
# - aggregazione delle statistiche sui tempi
# - verifica della correttezza delle estrazioni (max-first)


import random
import time
import statistics


def generate_input(n, case='random', random_range=None, seed=None):
    """
    Genera una lista di 'n' chiavi per testare le code di priorità.

    Parametri:
    - n   : numero di elementi da generare
    - case: tipo di input da generare, uno tra:
        * 'random'     → numeri casuali uniformi
        * 'ascending'  → sequenza crescente 0..n-1
        * 'descending' → sequenza decrescente n-1..0
        * 'repeated'   → valori ripetuti in un intervallo molto piccolo
    - random_range: range per il caso 'random'
    - seed: per rendere la generazione riproducibile

    Scopi nei test:
    - Studiare come le strutture reagiscono a input diversi.
    - Testare casi peggiori, medi e migliori.
    - Verificare robustezza e comportamento rispetto all'ordinamento iniziale.

    Complessità: O(n)
    """

    # Per avere risultati riproducibili
    if seed is not None:
        random.seed(seed)

    # Caso 1: distribuzione uniforme casuale
    if case == 'random':
        if random_range is None:
            # Se non specificato: range abbastanza ampio
            random_range = max(1000, n * 10)
        return [random.randint(0, random_range - 1) for _ in range(n)]

    # Caso 2: input crescente (peggior caso per lista ordinata)
    elif case == 'ascending':
        return list(range(n))

    # Caso 3: input decrescente (caso migliore per lista ordinata)
    elif case == 'descending':
        return list(range(n - 1, -1, -1))

    # Caso 4: valori ripetuti in un piccolo range
    elif case == 'repeated':
        # Il range è massimo tra 2 e 10, proporzionato all'input
        r = max(2, min(10, n // 10))
        return [random.randint(0, r - 1) for _ in range(n)]

    else:
        raise ValueError("case must be one of 'random','ascending','descending','repeated'")


def time_function(func, *args, **kwargs):
    """
    Misura il tempo di esecuzione di una funzione.

    Restituisce:
        (tempo_in_secondi, valore_restituito)

    Utile per misurare:
    - tempo di insert
    - tempo di extract_max
    - tempo di costruzione iniziale
    - ogni altra operazione che vogliamo confrontare

    Usa time.perf_counter() che è ad alta risoluzione.

    Complessità: dipende dalla funzione misurata.
    """

    start = time.perf_counter()
    result = func(*args, **kwargs)
    end = time.perf_counter()

    return end - start, result


def aggregate_times(times):
    """
    Aggrega una lista di tempi (float) e restituisce:
    {
        "median": mediana,
        "mean": media,
        "stdev": deviazione standard,
        "count": numero di misure
    }

    Scopi:
    - stabilizzare i risultati sperimentali
    - eliminare effetto di outlier o interferenze del sistema operativo
    - ottenere valori robusti per grafici e tabelle della relazione

    Complessità: O(n)
    """

    if len(times) == 0:
        return {"median": None, "mean": None, "stdev": None, "count": 0}

    median = statistics.median(times)
    mean = statistics.mean(times)
    stdev = statistics.stdev(times) if len(times) > 1 else 0.0

    return {
        "median": median,
        "mean": mean,
        "stdev": stdev,
        "count": len(times)
    }


def verify_extract_sequence(input_list, extract_sequence):
    """
    Verifica la correttezza di una sequenza di estrazioni completa.

    input_list:         lista originale di valori inseriti
    extract_sequence:   lista dei valori estratti con extract_max()

    Il comportamento corretto di ogni coda di priorità è:
        estrazioni devono restituire i valori in ordine NON CRESCENTE
        (cioè: max → secondo max → terzo max → ...)

    Quindi:
        sorted(input_list, reverse=True)
    deve essere == extract_sequence

    Restituisce:
        True  se la sequenza è corretta
        False altrimenti

    Utile per:
    - test di correttezza automatica delle implementazioni
    - debugging
    - garantire consistenza prima di lanciare test più grandi
    """

    expected = sorted(input_list, reverse=True)
    return expected == list(extract_sequence)
