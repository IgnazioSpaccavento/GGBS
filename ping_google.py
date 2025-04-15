#!/usr/bin/env python3
# filepath: /home/users/ignazio.spaccavento/ping_google.py

import subprocess
import time
import datetime

def ping_google():
    """Esegue un ping a google.com e stampa il risultato."""
    try:
        # Esegue un solo ping (-c 1) con timeout di 5 secondi
        result = subprocess.run(
            ['ping', '-c', '1', '-W', '5', 'google.com'],
            capture_output=True,
            text=True,
            check=True
        )
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Ping riuscito:")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Ping fallito:")
        print(e.stderr)
        return False
    except Exception as e:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Errore durante l'esecuzione del ping: {str(e)}")
        return False

def main():
    interval_minutes = 20
    interval_seconds = interval_minutes * 60
    
    print(f"Avvio monitoraggio ping a google.com ogni {interval_minutes} minuti. Premi Ctrl+C per interrompere.")
    
    try:
        while True:
            ping_google()
            print(f"In attesa {interval_minutes} minuti prima del prossimo ping...")
            time.sleep(interval_seconds)
    except KeyboardInterrupt:
        print("\nMonitoraggio interrotto dall'utente.")

if __name__ == "__main__":
    main()