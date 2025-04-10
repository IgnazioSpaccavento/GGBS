import csv
import re
import sys
import os

def save_to_csv(values, csv_file):
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['node_id', 'offset'])
        writer.writerows(values)

def main(folder_name):
    i = 0
    # Utilizzo del parametro folder_name al posto del valore hardcoded
    gaf_file = f'/home/users/ignazio.spaccavento/GGBS/results/{folder_name}/GraphAligner/MHC/f_MHC-57_alignments.gaf'
    csv_file = '/home/users/ignazio.spaccavento/GGBS/results/position_csv_ga/f_100.csv'
    
    # Verifica che il file esista
    if not os.path.exists(gaf_file):
        print(f"Errore: Il file {gaf_file} non esiste.")
        return

    with open(gaf_file, 'r') as f_in:
        values_pos = []
        for line in f_in:
            i += 1
            if line.startswith('#'):
                continue
            values = line.strip().split('\t')
            if values[2] == "*" or values[5] == "*":
                read = values[0]
                node_id = "0"
                offset = "0"
            else:
                read = values[0]
                nodes = re.split(r'[><]', values[5].strip())
                node_id = nodes[1]
                offset = values[7]

            if node_id is not None and offset is not None and read is not None:
                values_pos.append((int(read), node_id, offset))

    # Sort by the read column numerically
    values_pos.sort(key=lambda x: x[0])

    # Find the range of read values
    min_read = 1
    max_read = 1000

    # Fill in missing read values
    full_values_pos = []
    seen_reads = set()
    for value in values_pos:
        seen_reads.add(value[0])
        full_values_pos.append(value)

    for read in range(min_read, max_read + 1):
        if read not in seen_reads:
            full_values_pos.append((read, '0', '0'))

    # Sort again to ensure the new entries are in the correct order
    full_values_pos.sort(key=lambda x: x[0])

    # Remove duplicates based on the read column, keeping the first occurrence
    unique_values_pos = []
    seen_reads = set()
    for value in full_values_pos:
        if value[0] not in seen_reads:
            seen_reads.add(value[0])
            unique_values_pos.append(value)

    # Remove the read column
    final_values_pos = [(node_id, offset) for _, node_id, offset in unique_values_pos]

    # Save to CSV
    save_to_csv(final_values_pos, csv_file)
    print(f"File CSV generato: {csv_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Utilizzo: python GA_gaf_parser.py nome_cartella")
        print("Esempio: python GA_gaf_parser.py 2025_04_09_09_50_38")
        sys.exit(1)
    
    folder_name = sys.argv[1]
    main(folder_name)