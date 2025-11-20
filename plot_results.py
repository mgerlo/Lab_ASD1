# plot_results.py
import os
import csv
import matplotlib.pyplot as plt

def read_aggregated(path):
    data = []
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for r in reader:
            data.append(r)
    return data

def plot_by_operation(data, operation, outdir="results/plots"):
    os.makedirs(outdir, exist_ok=True)
    # data: list of dicts with keys 'impl','operation','n','case','median_s',...
    # group by case and impl
    cases = sorted(set(d['case'] for d in data if d['operation']==operation))
    impls = sorted(set(d['impl'] for d in data if d['operation']==operation))

    for case in cases:
        plt.figure(figsize=(8,5))
        for impl in impls:
            xs = []
            ys = []
            for d in sorted(data, key=lambda r:(int(r['n']))):
                if d['operation']==operation and d['case']==case and d['impl']==impl:
                    xs.append(int(d['n']))
                    ys.append(float(d['median_s']) * 1000.0)  # convert to ms
            if xs:
                plt.plot(xs, ys, marker='o', label=impl)
        plt.xlabel("n (number of elements)")
        plt.ylabel("median time (ms)")
        plt.title(f"{operation} - case: {case}")
        plt.legend()
        plt.grid(True)
        outfile = os.path.join(outdir, f"{operation}_{case}.png")
        plt.savefig(outfile, bbox_inches='tight')
        plt.close()
        print("Saved", outfile)

def main(agg_csv="results/aggregated_results.csv"):
    data = read_aggregated(agg_csv)
    plot_by_operation(data, operation="insert")
    plot_by_operation(data, operation="extract_all")

if __name__ == "__main__":
    main()
