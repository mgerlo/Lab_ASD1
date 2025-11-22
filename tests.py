# tests.py
#
# Questo script esegue TEST DI PERFORMANCE sulle tre implementazioni
# delle code di priorità:
#
#  - HeapPriorityQueue
#  - LinkedListPriorityQueue
#  - SortedLinkedListPriorityQueue
#
# Genera i file CSV:
#   - raw_results.csv        → risultati grezzi, run per run
#   - aggregated_results.csv → tempi aggregati (mediana, media, stdev)
#
# Serve come base per generare grafici e tabelle nella relazione LaTeX.


import os
import csv
import argparse
from collections import defaultdict

from utils import (
    generate_input,
    time_function,
    aggregate_times,
    verify_extract_sequence
)

# Importiamo le implementazioni delle tre priority queue
from heap_priority_queue import HeapPriorityQueue
from linked_list_priority_queue import LinkedListPriorityQueue
from sorted_linked_list_priority_queue import SortedLinkedListPriorityQueue


def get_impls():
    """
    Restituisce un dizionario:
        nome → classe
    in modo da poter iterare comodamente tutte le implementazioni.
    """
    return {
        "heap": HeapPriorityQueue,
        "linked_list": LinkedListPriorityQueue,
        "sorted_linked_list": SortedLinkedListPriorityQueue
    }


def run_insert_test(pq_class, keys):
    """
    Misura il TEMPO necessario a inserire tutti i valori 'keys'
    dentro una nuova priority queue della classe `pq_class`.

    - pq_class: classe della struttura (Heap / Lista / Lista ordinata)
    - keys: lista di valori da inserire

    Ritorna:
        (tempo_in_secondi, pq_instance)

    La coda risultante viene restituita in modo che sia possibile
    utilizzarla per ulteriori test (se necessario).
    """

    pq = pq_class()

    def do_inserts():
        for k in keys:
            pq.insert(k)
        return pq

    # time_function misura il tempo esatto della funzione
    t, _ = time_function(do_inserts)
    return t, pq


def run_extract_test(pq_class, keys):
    """
    Testa il tempo di estrazione COMPLETA.

    Procedura:
    1. Crea una PQ vuota.
    2. Inserisce tutti i valori di 'keys'.
    3. Misura il tempo necessario a estrarre TUTTI gli elementi.

    Ritorna:
        (tempo_in_secondi, lista_estratta)
    """

    pq = pq_class()

    # Inseriamo i valori prima di misurare l’estrazione
    for k in keys:
        pq.insert(k)

    extracted = []

    def do_extracts():
        while pq.size() > 0:
            extracted.append(pq.extract_max())
        return extracted

    t, _ = time_function(do_extracts)
    return t, extracted


def ensure_results_dir(path):
    """
    Crea la cartella dei risultati se non esiste.
    Serve per salvare i CSV in modo ordinato.
    """
    if not os.path.exists(path):
        os.makedirs(path)


def main(out_dir="results",
         ns=(100, 500, 1000, 5000),
         cases=("random", "ascending", "descending", "repeated"),
         runs=5,
         random_range=None):
    """
    Funzione principale che esegue TUTTI i test.

    Parametri:
    - out_dir: cartella dove salvare CSV
    - ns: diverse dimensioni dei test (numero di elementi)
    - cases: tipi di input da testare
    - runs: ripetizioni per ogni configurazione
    - random_range: range numerico per il caso "random"

    Strategia di test:
      Per ogni n
        Per ogni tipo di input (case)
          Per ogni implementazione
            Per ogni run (ripetizione)
              - genera input
              - misura tempo insert
              - verifica correttezza (estrazione completa)
              - misura tempo extract_all
              - salva risultati
    """

    ensure_results_dir(out_dir)

    raw_path = os.path.join(out_dir, "raw_results.csv")
    agg_path = os.path.join(out_dir, "aggregated_results.csv")

    impls = get_impls()

    # Apriamo il file CSV RAW: un record per ogni run
    with open(raw_path, "w", newline="") as raw_file:
        raw_writer = csv.writer(raw_file)

        # Header CSV
        raw_writer.writerow([
            "impl", "operation", "n", "case",
            "run_id", "time_seconds", "valid"
        ])

        # Struttura che accumula i tempi per l’aggregazione
        agg_storage = defaultdict(list)

        run_id = 0

        # Triple loop su ns, cases, implementazioni
        for n in ns:
            for case in cases:
                for impl_name, impl_cls in impls.items():

                    for run_idx in range(runs):

                        run_id += 1
                        seed = run_idx  # per garantire riproducibilità parziale

                        # --- GENERAZIONE INPUT ---
                        keys = generate_input(
                            n,
                            case=case,
                            random_range=random_range,
                            seed=seed
                        )

                        # --- TEST INSERT ---
                        t_insert, pq_instance = run_insert_test(impl_cls, keys)

                        # Verifica della correttezza:
                        # estrai tutti gli elementi da una NUOVA PQ basata sugli stessi keys
                        _, extracted = run_extract_test(impl_cls, keys)
                        valid = verify_extract_sequence(keys, extracted)

                        # Scriviamo riga dei RAW data
                        raw_writer.writerow([
                            impl_name, "insert", n, case,
                            run_id, t_insert, valid
                        ])

                        # Salviamo per l’aggregazione
                        agg_storage[(impl_name, "insert", n, case)].append(t_insert)

                        # --- TEST EXTRACT (solo tempo di estrazione) ---
                        t_extract, extracted2 = run_extract_test(impl_cls, keys)
                        valid2 = verify_extract_sequence(keys, extracted2)

                        raw_writer.writerow([
                            impl_name, "extract_all", n, case,
                            run_id, t_extract, valid2
                        ])

                        agg_storage[(impl_name, "extract_all", n, case)].append(t_extract)

                        # Log su console (utile quando i test sono lunghi)
                        print(
                            f"[run {run_id}] impl={impl_name} n={n} case={case} "
                            f"run={run_idx+1}/{runs} insert={t_insert:.6f}s "
                            f"extract={t_extract:.6f}s valid={valid and valid2}"
                        )

    # --- PHASE 2: AGGREGAZIONE DEI RISULTATI ---
    with open(agg_path, "w", newline="") as agg_file:
        agg_writer = csv.writer(agg_file)

        agg_writer.writerow([
            "impl", "operation", "n", "case",
            "median_s", "mean_s", "stdev_s", "count"
        ])

        for key, times in agg_storage.items():
            impl_name, operation, n, case = key

            stats = aggregate_times(times)

            agg_writer.writerow([
                impl_name,
                operation,
                n,
                case,
                stats["median"],
                stats["mean"],
                stats["stdev"],
                stats["count"]
            ])

    print("Raw results saved to:", raw_path)
    print("Aggregated results saved to:", agg_path)


# --- PARTE CLI (Command Line Interface) ---
# consente di lanciare:
#     python tests.py --runs 10 --ns 100,200,500
# utile per ripetere esperimenti senza modificare il codice

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run priority queue performance tests.")
    parser.add_argument("--out", default="results", help="results directory")
    parser.add_argument("--runs", type=int, default=5, help="runs per configuration")
    parser.add_argument("--ns", type=str, default="100,500,1000", help="comma-separated n sizes")
    parser.add_argument("--cases", type=str, default="random,ascending,descending,repeated",
                        help="comma-separated case types")
    parser.add_argument("--random_range", type=int, default=None, help="range for random generator")

    args = parser.parse_args()

    ns = tuple(int(x) for x in args.ns.split(",") if x.strip())
    cases = tuple(x.strip() for x in args.cases.split(",") if x.strip())

    main(out_dir=args.out, ns=ns, cases=cases, runs=args.runs, random_range=args.random_range)
