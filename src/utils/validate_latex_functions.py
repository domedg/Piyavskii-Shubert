import json
from pathlib import Path

def genera_lista_validazione_latex():
    """
    Legge il file funzioni_config.json e genera un file Markdown con
    formule LaTeX in modalità "display" per la massima leggibilità.
    """
    base_path = Path.cwd()
    json_path = base_path / "data" / "funzioni_config.json"
    md_output_path = base_path / "data" / "funzioni_latex.md"

    if not json_path.exists():
        print("[ERRORE] File JSON non trovato.")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        funzioni = json.load(f)

    # Costruzione Markdown con blocchi matematici indipendenti
    linee_md = [
        "# Validazione Visiva Funzioni",
        "Controlla le equazioni sottostanti. Il formato a lista garantisce la massima grandezza e leggibilità del LaTeX su VS Code.\n",
        "---"
    ]

    for nome, dati in funzioni.items():
        nn = nome.replace("F", "")
        # Nessuno spazio tra i $$ e la formula, come da best practice
        formula_math = f"$${dati['latex']}$$"
        intervallo = dati['intervallo']
        l_val = dati['L']
        
        linee_md.append(f"### Funzione {nn}")
        linee_md.append(formula_math)
        linee_md.append(f"* **Intervallo:** [{intervallo[0]}, {intervallo[1]}]")
        linee_md.append(f"* **Costante L:** {l_val}")
        linee_md.append("---\n")

    with open(md_output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(linee_md))

    print(f"[INFO] Documento ad alta leggibilità generato in: {md_output_path}")

if __name__ == "__main__":
    genera_lista_validazione_latex()