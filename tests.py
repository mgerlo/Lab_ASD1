# tests.py
import os
import csv
import argparse
from collections import defaultdict
from utils import generate_input, time_function, aggregate_times, verify_extract_sequence
# importa le implementazioni (assumi che i file siano nello stesso folder)
from heap_priority_queue import HeapPriorityQueue
from linked_list_priority_queue import LinkedListPriorityQueue
from sorted_linked_list_priority_queue import SortedLinkedListPriorityQueue

def get_impls():
    return {
        "heap": HeapPriorityQueue,
        "linked_list": LinkedListPriorityQueue,
        "sorted_linked_list": SortedLinkedListPriorityQueue
    }

def run_insert_test(pq_class, keys):
    """
    Misura tempo totale per inserire tutti i keys in una istanza di pq_class.
    Ritorna (time_seconds, pq_instance)
    """
    pq = pq_class()
    def do_inserts():
        for k in keys:
            pq.insert(k)
        return pq
    t, _ = time_function(do_inserts)
    return t, pq

def run_extract_test(pq_class, keys):
    """
    Inserisce tutti i keys, poi misura il tempo per estrarre *tutti* gli elementi.
    Ritorna (time_seconds, extracted_list)
    """
    pq = pq_class()
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
    if not os.path.exists(path):
        os.makedirs(path)

def main(out_dir="results",
         ns=(100,500,1000,5000),
         cases=("random","ascending","descending","repeated"),
         runs=5,
         random_range=None):
    ensure_results_dir(out_dir)
    raw_path = os.path.join(out_dir, "raw_results.csv")
    agg_path = os.path.join(out_dir, "aggregated_results.csv")

    impls = get_impls()

    # apri CSV raw e scrivi riga per riga
    with open(raw_path, "w", newline="") as raw_file:
        raw_writer = csv.writer(raw_file)
        raw_writer.writerow([
            "impl","operation","n","case","run_id","time_seconds","valid"
        ])

        # raccogli dati per aggregazione
        agg_storage = defaultdict(list)

        run_id = 0
        for n in ns:
            for case in cases:
                for impl_name, impl_cls in impls.items():
                    for run_idx in range(runs):
                        run_id += 1
                        seed = run_idx  # per riproducibilità parziale
                        keys = generate_input(n, case=case, random_range=random_range, seed=seed)

                        # INSERT test
                        t_insert, pq_instance = run_insert_test(impl_cls, keys)
                        # verifica base: estrai tutto e controlla correttezza (per sicurezza)
                        # per non invalidare il test di insert, cloniamo la lista:
                        # ma PQ ha già la struttura occupata da insert; estraiamo da una copia di pq_instance
                        # per semplicità, qui verifichiamo estraendo gli elementi in un nuovo PQ costruito
                        # a partire dagli stessi keys
                        t_verify, extracted = run_extract_test(impl_cls, keys)
                        valid = verify_extract_sequence(keys, extracted)

                        raw_writer.writerow([impl_name,"insert",n,case,run_id,t_insert, valid])
                        agg_storage[(impl_name,"insert",n,case)].append(t_insert)

                        # EXTRACT test (measure extraction time only)
                        t_extract, extracted2 = run_extract_test(impl_cls, keys)
                        valid2 = verify_extract_sequence(keys, extracted2)

                        raw_writer.writerow([impl_name,"extract_all",n,case,run_id,t_extract, valid2])
                        agg_storage[(impl_name,"extract_all",n,case)].append(t_extract)

                        print(f"[run {run_id}] impl={impl_name} n={n} case={case} run={run_idx+1}/{runs} insert={t_insert:.6f}s extract={t_extract:.6f}s valid={valid and valid2}")

    # ora aggregazione e salvataggio
    with open(agg_path, "w", newline="") as agg_file:
        agg_writer = csv.writer(agg_file)
        agg_writer.writerow([
            "impl","operation","n","case","median_s","mean_s","stdev_s","count"
        ])
        for key, times in agg_storage.items():
            impl_name, operation, n, case = key
            stats = aggregate_times(times)
            agg_writer.writerow([impl_name,operation,n,case,stats["median"],stats["mean"],stats["stdev"],stats["count"]])

    print("Raw results saved to:", raw_path)
    print("Aggregated results saved to:", agg_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run priority queue performance tests.")
    parser.add_argument("--out", default="results", help="results directory")
    parser.add_argument("--runs", type=int, default=5, help="runs per configuration")
    parser.add_argument("--ns", type=str, default="100,500,1000", help="comma-separated n sizes")
    parser.add_argument("--cases", type=str, default="random,ascending,descending,repeated", help="comma-separated case types")
    parser.add_argument("--random_range", type=int, default=None, help="range for random generator")
    args = parser.parse_args()

    ns = tuple(int(x) for x in args.ns.split(",") if x.strip())
    cases = tuple(x.strip() for x in args.cases.split(",") if x.strip())

    main(out_dir=args.out, ns=ns, cases=cases, runs=args.runs, random_range=args.random_range)
