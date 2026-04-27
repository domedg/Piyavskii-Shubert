import os
import json
from pathlib import Path

def setup_project_architecture():
    """
    Inizializza la struttura delle directory per il progetto di Calcolo Numerico
    e crea il file di configurazione completo con le 20 funzioni di test.
    """
    # Definizione delle directory principali
    directories = [
        "data",
        "src/core",
        "src/utils",
        "plots"
    ]
    
    # Creazione delle cartelle
    base_path = Path.cwd()
    for dir_path in directories:
        (base_path / dir_path).mkdir(parents=True, exist_ok=True)
        if "src" in dir_path:
            (base_path / dir_path / "__init__.py").touch()
            
    print("[INFO] Struttura delle directory confermata.")

    # Dizionario completo delle 20 funzioni estratte dalla Tabella 1
    funzioni_config = {
        "F1":  {"formato_np": "(1/6)*x**6 - (52/25)*x**5 + (39/80)*x**4 + (71/10)*x**3 - (79/20)*x**2 - x + 1/10", "intervallo": [-1.5, 11.0], "L": 13870.0},
        "F2":  {"formato_np": "np.sin(x) + np.sin((10*x)/3)", "intervallo": [2.7, 7.5], "L": 4.29},
        "F3":  {"formato_np": "-sum(k * np.sin((k + 1) * x + k) for k in range(1, 6))", "intervallo": [-10.0, 10.0], "L": 67.0},
        "F4":  {"formato_np": "-(16*x**2 - 24*x + 5) * np.exp(-x)", "intervallo": [1.9, 3.9], "L": 3.0},
        "F5":  {"formato_np": "(3*x - 1.4) * np.sin(18*x)", "intervallo": [0.0, 1.2], "L": 36.0},
        "F6":  {"formato_np": "-(x + np.sin(x)) * np.exp(-x**2)", "intervallo": [-10.0, 10.0], "L": 2.5},
        "F7":  {"formato_np": "np.sin(x) + np.sin((10*x)/3) + np.log(x) - 0.84*x + 3", "intervallo": [2.7, 7.5], "L": 6.0},
        "F8":  {"formato_np": "-sum(k * np.cos((k + 1) * x + k) for k in range(1, 6))", "intervallo": [-10.0, 10.0], "L": 67.0},
        "F9":  {"formato_np": "np.sin(x) + np.sin((2*x)/3)", "intervallo": [3.1, 20.4], "L": 1.7},
        "F10": {"formato_np": "-x * np.sin(x)", "intervallo": [0.0, 10.0], "L": 11.0},
        "F11": {"formato_np": "2 * np.cos(x) + np.cos(2*x)", "intervallo": [-1.57, 6.28], "L": 3.0},
        "F12": {"formato_np": "np.sin(x)**3 + np.cos(x)**3", "intervallo": [0.0, 6.28], "L": 2.2},
        "F13": {"formato_np": "-np.cbrt(x**2) + np.cbrt(x**2 - 1)", "intervallo": [0.001, 0.99], "L": 8.5},
        "F14": {"formato_np": "-np.exp(-x) * np.sin(2 * np.pi * x)", "intervallo": [0.0, 4.0], "L": 6.5},
        "F15": {"formato_np": "(x**2 - 5*x + 6) / (x**2 + 1)", "intervallo": [-5.0, 5.0], "L": 6.5},
        "F16": {"formato_np": "2*(x - 3)**2 + np.exp(0.5 * x**2)", "intervallo": [-3.0, 3.0], "L": 85.0},
        "F17": {"formato_np": "x**6 - 15*x**4 + 27*x**2 + 250", "intervallo": [-4.0, 4.0], "L": 2520.0},
        "F18": {"formato_np": "np.where(x <= 3, (x - 2)**2, 2 * np.log(x - 2) + 1)", "intervallo": [0.0, 6.0], "L": 4.0},
        "F19": {"formato_np": "-x + np.sin(3*x) - 1", "intervallo": [0.0, 6.5], "L": 4.0},
        "F20": {"formato_np": "(np.sin(x) - x) * np.exp(-x**2)", "intervallo": [-10.0, 10.0], "L": 1.3}
    }

    # Salvataggio in JSON
    config_path = base_path / "data" / "funzioni_config.json"
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(funzioni_config, f, indent=4)
        
    print(f"[INFO] File di configurazione salvato in: {config_path}")
    
    # Inizializzazione Relazione Tecnica
    md_path = base_path / "relazione_progetto.md"
    if not md_path.exists():
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write("# Relazione Progetto: Ottimizzazione Numerica Unidimensionale\n\n")
        print(f"[INFO] Documento {md_path.name} inizializzato.")

if __name__ == "__main__":
    setup_project_architecture()