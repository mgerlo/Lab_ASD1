# plot_results.py
#
# Questo script legge i risultati aggregati (CSV)
# generati da tests.py e produce grafici in formato PNG.
#
# I grafici generati servono per:
#   - confrontare performance delle 3 implementazioni
#   - inserire figure nella relazione LaTeX
#   - osservare trend al variare della dimensione n
#
# Viene usata matplotlib per generare line plot.


import os
import csv
import matplotlib.pyplot as plt


def read_aggregated(path):
    """
    Legge il file CSV output di aggregated_results.csv
    e restituisce una lista di dizionari (uno per riga).

    Ogni dizionario contiene stringhe, per esempio:
        {
            'impl': 'heap',
            'operation': 'insert',
            'n': '500',
            'case': 'random',
            'median_s': '0.00234',
            'mean_s': '0.00241',
            'stdev_s': '0.00010',
            'count': '5'
        }

    Scopo:
    - isolare la lettura del CSV
    - fornire una struttura comoda per analisi successive
    """

    data = []
    with open(path, newline='') as f:
        reader = csv.DictReader(f)  # legge usando l'header del CSV
        for r in reader:
            data.append(r)
    return data


def plot_by_operation(data, operation, outdir="results/plots"):
    """
    Genera un grafico per una determinata operazione:
        - "insert"
        - "extract_all"

    La funzione produce UN grafico per ogni tipo di input (case):
        random, ascending, descending, repeated

    Per ogni grafico:
    - Sull'asse X: n (dimensione input)
    - Sull'asse Y: tempo mediano (in millisecondi)
    - Una curva per ogni implementazione (heap, linked_list, sorted_list)

    Parametri:
    - data: risultati aggregati (lista di dict)
    - operation: string ("insert" oppure "extract_all")
    - outdir: cartella dove salvare i PNG
    """

    # Creiamo la cartella plots/ se non esiste
    os.makedirs(outdir, exist_ok=True)

    # Filtriamo le casistiche
    cases = sorted(set(d['case'] for d in data if d['operation'] == operation))
    impls = sorted(set(d['impl'] for d in data if d['operation'] == operation))

    for case in cases:
        # Apriamo un nuovo grafico
        plt.figure(figsize=(8, 5))

        for impl in impls:
            xs = []  # valori di n
            ys = []  # mediane dei tempi in millisecondi

            # Ordiniamo i dati per n (altrimenti la curva sarebbe disordinata)
            for d in sorted(data, key=lambda r: int(r['n'])):
                if (
                    d['operation'] == operation
                    and d['case'] == case
                    and d['impl'] == impl
                ):
                    xs.append(int(d['n']))
                    # Convertiamo secondi → millisecondi
                    ys.append(float(d['median_s']) * 1000.0)

            if xs:
                # Disegniamo la curva
                plt.plot(xs, ys, marker='o', label=impl)

        # Titoli e assi
        plt.xlabel("n (number of elements)")
        plt.ylabel("median time (ms)")
        plt.title(f"{operation} - case: {case}")
        plt.legend()
        plt.grid(True)

        # Salvataggio file PNG
        outfile = os.path.join(outdir, f"{operation}_{case}.png")
        plt.savefig(outfile, bbox_inches='tight')
        plt.close()

        print("Saved", outfile)


def main(agg_csv="results/aggregated_results.csv"):
    """
    Funzione principale:
    - legge il CSV aggregato
    - genera grafici per:
        * insert
        * extract_all
    """

    data = read_aggregated(agg_csv)

    # Genera grafici per le due operazioni principali
    plot_by_operation(data, operation="insert")
    plot_by_operation(data, operation="extract_all")


if __name__ == "__main__":
    # Esecuzione come script indipendente
    main()
