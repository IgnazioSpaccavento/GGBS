import subprocess
import sys
import time
import os
import shutil
import glob
import datetime
import re
import csv

def remove_2025_folders():
    """
    Rimuove tutte le cartelle che contengono '2025' nel nome
    """
    # Cerca tutte le cartelle che contengono '2025' nel nome
    found_folders = []
    for root, dirs, _ in os.walk('.'):
        for dir in dirs:
            if '2025' in dir:
                folder_path = os.path.join(root, dir)
                found_folders.append(folder_path)
    
    # Elimina le cartelle trovate
    if found_folders:
        for folder in found_folders:
            try:
                shutil.rmtree(folder)
            except Exception:
                pass

def execute_command(command, description, capture_output=False, show_output=False):
    """
    Esegue un comando nel terminale e opzionalmente mostra l'output in tempo reale
    
    Parametri:
        command (str): Comando da eseguire
        description (str): Descrizione del comando da mostrare
        capture_output (bool): Se True, cattura e restituisce l'output
        show_output (bool): Se True, mostra l'output in tempo reale
    
    Ritorna:
        bool: True se il comando è stato eseguito con successo
        str: L'output del comando (solo se capture_output=True)
    """
    if show_output:
        print(f"\n{'=' * 50}")
        print(f"Esecuzione di: {description}")
        print(f"Comando: {command}")
        print(f"{'=' * 50}\n")
    
    output = ""
    
    try:
        # Esecuzione del comando con output opzionale
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        
        # Lettura dell'output (mostrato solo se richiesto)
        for line in process.stdout:
            if show_output:
                print(line, end='')
            if capture_output:
                output += line
        
        # Attesa del completamento del processo
        return_code = process.wait()
        
        if (return_code != 0):
            if show_output:
                print(f"\nATTENZIONE: Il comando '{command}' è terminato con codice di uscita {return_code}")
            if capture_output:
                return False, output
            return False
        
        if show_output:
            print(f"\nComando '{command}' completato con successo!")
        if capture_output:
            return True, output
        return True
    
    except Exception as e:
        if show_output:
            print(f"\nErrore durante l'esecuzione del comando '{command}': {e}")
        if capture_output:
            return False, output
        return False

def find_latest_folder():
    """
    Cerca la cartella più recente che ha il formato di data e orario (2025_MM_DD_HH_MM_SS)
    nella directory results
    """
    # Cerca specificatamente nella directory results
    results_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
    pattern = os.path.join(results_path, "2025_*_*_*_*_*")
    
    matching_folders = glob.glob(pattern)
    
    if not matching_folders:
        return None
    
    # Ordina per data di creazione e prendi la più recente
    latest_folder = sorted(matching_folders, key=os.path.getctime)[-1]
    # Estrai solo il nome della cartella dalla path completa
    folder_name = os.path.basename(latest_folder)
    
    return folder_name

def modify_seeds_minimizer_length(length):
    """
    Modifica il valore del parametro --seeds-minimizer-length nel file make_dockercompose.py
    """
    file_path = "make_dockercompose.py"
    
    # Leggi il contenuto del file
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Trova e sostituisci il valore del parametro --seeds-minimizer-length
    pattern = r"--seeds-minimizer-length\s+\d+"
    replacement = f"--seeds-minimizer-length {length}"
    modified_content = re.sub(pattern, replacement, content)
    
    # Scrivi il contenuto modificato nel file
    with open(file_path, 'w') as file:
        file.write(modified_content)

def modify_seeds_minimizer_windowsize(windowsize):
    """
    Modifica il valore del parametro --seeds-minimizer-windowsize nel file make_dockercompose.py
    """
    file_path = "make_dockercompose.py"
    
    # Leggi il contenuto del file
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Trova e sostituisci il valore del parametro --seeds-minimizer-windowsize
    pattern = r"--seeds-minimizer-windowsize\s+\d+"
    replacement = f"--seeds-minimizer-windowsize {windowsize}"
    modified_content = re.sub(pattern, replacement, content)
    
    # Scrivi il contenuto modificato nel file
    with open(file_path, 'w') as file:
        file.write(modified_content)
    
    # Rimuovo la riga di print
    # print(f"Parametro --seeds-minimizer-windowsize modificato a {windowsize} nel file {file_path}")

def modify_seeds_minimizer_density(density):
    """
    Modifica il valore del parametro --seeds-minimizer-density nel file make_dockercompose.py
    """
    file_path = "make_dockercompose.py"
    
    # Leggi il contenuto del file
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Trova e sostituisci il valore del parametro --seeds-minimizer-density
    pattern = r"--seeds-minimizer-density\s+\d+"
    replacement = f"--seeds-minimizer-density {density}"
    modified_content = re.sub(pattern, replacement, content)
    
    # Scrivi il contenuto modificato nel file
    with open(file_path, 'w') as file:
        file.write(modified_content)
    

def extract_similarity_score(output):
    """
    Estrae il punteggio di similarità dall'output del comando compare_file_csv.py
    
    Parametri:
        output (str): L'output del comando compare_file_csv.py
    
    Ritorna:
        float: Il punteggio di similarità o None se non trovato
    """
    match = re.search(r"Similarity score: (\d+\.\d+)", output)
    if match:
        return float(match.group(1))
    return None

def print_csv_output(data):
    """
    Stampa in modo conciso i dati che andranno nel CSV
    """
    if not data:
        print("Nessun dato disponibile per il CSV")
        return
    
    print("\n=== DATI CSV ===")
    print("seeds_minimizer_length,seeds_minimizer_windowsize,seeds_minimizer_density,similarity_score")
    for entry in data:
        print(f"{entry['seeds_minimizer_length']},{entry['seeds_minimizer_windowsize']},{entry['seeds_minimizer_density']},{entry['similarity_score']}")
    print("===============\n")

def run_pipeline_with_parameters(length, windowsize=30, density=2, results=[]):
    # Modifica i valori dei parametri
    modify_seeds_minimizer_length(length)
    modify_seeds_minimizer_windowsize(windowsize)
    modify_seeds_minimizer_density(density)
    
    # Lista di comandi da eseguire in sequenza
    commands = [
        {"cmd": "python3 make_dockerfiles.py", "desc": f"Prima esecuzione di make_dockerfiles.py"},
        {"cmd": "python3 make_dockercompose.py", "desc": f"Esecuzione di make_dockercompose.py"},
        {"cmd": "docker compose up", "desc": f"Avvio di Docker Compose"}
    ]
    
    # Esecuzione sequenziale dei comandi senza mostrare output
    for cmd_info in commands:
        success = execute_command(cmd_info["cmd"], cmd_info["desc"], show_output=False)
        if not success:
            print(f"{length},{windowsize},{density},ERROR")
            return False
        if "docker compose up" in cmd_info["cmd"]:
            time.sleep(1)
        else:
            time.sleep(0.5)
    
    # Trova la cartella più recente
    folder_name = find_latest_folder()
    
    if (folder_name):
        # Esegui GA_gaf_parser.py senza mostrare output
        gaf_command = f"python3 utils/GA_gaf_parser.py {folder_name}"
        execute_command(gaf_command, f"Esecuzione di GA_gaf_parser.py", show_output=False)
        
        # Esegui compare_file_csv.py senza mostrare output
        compare_command = "python3 utils/compare_file_csv.py"
        success, output = execute_command(compare_command, f"Esecuzione di compare_file_csv.py", capture_output=True, show_output=False)
        
        if success:
            # Estrai lo score di similarità
            similarity_score = extract_similarity_score(output)
            if similarity_score is not None:
                # Stampa solo il risultato in formato CSV
                print(f"{length},{windowsize},{density},{similarity_score}")
                
                # Salva i risultati
                results.append({
                    "seeds_minimizer_length": length,
                    "seeds_minimizer_windowsize": windowsize,
                    "seeds_minimizer_density": density,
                    "similarity_score": similarity_score
                })
            else:
                print(f"{length},{windowsize},{density},N/A")
                return False
    else:
        print(f"{length},{windowsize},{density},ERROR_NO_FOLDER")
        return False
    
    return True

def save_results_to_csv(results, filename="similarity_scores.csv"):
    """
    Salva i risultati in un file CSV
    """
    try:
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['seeds_minimizer_length', 'seeds_minimizer_windowsize', 'seeds_minimizer_density', 'similarity_score']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for result in results:
                writer.writerow(result)
            
        print(f"\nI risultati sono stati salvati nel file {filename}")
    except Exception as e:
        print(f"\nErrore durante il salvataggio dei risultati: {e}")

def main():
    # Per ogni valore di density (da 2 a 9 inclusi)
    for density in range(3, 10):  # Da 2 a 9 incluso
        # Creiamo una lista per salvare i risultati
        results = []
        
        print(f"### DENSITY = {density} ###")
        print("seeds_minimizer_length,seeds_minimizer_windowsize,seeds_minimizer_density,similarity_score")
        
        # Prima rimuovi le cartelle contenenti "2025"
        remove_2025_folders()
        
        # Esegui il pipeline invertendo i cicli: prima windowsize e poi length
        for windowsize in range(10, 41):  # Da 30 a 40 incluso
            for length in range(10, 31):  # Da 10 a 30 incluso
                # Esegui il pipeline con i valori correnti
                success = run_pipeline_with_parameters(length, windowsize=windowsize, density=density, results=results)
                
                if not success:
                    print(f"{length},{windowsize},{density},ERROR")
                
                # Rimuovi le cartelle create in questo ciclo prima di passare al successivo
                remove_2025_folders()
                
                time.sleep(0.5)
        
        # Salva i risultati finali per questo valore di density
        save_results_to_csv(results, f"similarity_scores_density_{density}.csv")
        
        # Stampa riepilogo dei dati raccolti
        print_csv_output(results)
    
    print("Completato!")

if __name__ == "__main__":
    main()