import json
from pathlib import Path

def update_json_with_latex():
    """
    Aggiorna il file JSON di configurazione aggiungendo la rappresentazione
    LaTeX corretta per la validazione visiva.
    """
    base_path = Path.cwd()
    json_path = base_path / "data" / "funzioni_config.json"

    if not json_path.exists():
        print(f"[ERRORE] File JSON non trovato in: {json_path}")
        return

    # Caricamento dati attuali
    with open(json_path, 'r', encoding='utf-8') as f:
        funzioni = json.load(f)

    # Dizionario delle trascrizioni LaTeX corrispondenti (Table 1)
    latex_formulas = {
        "F1":  r"\frac{1}{6}x^6 - \frac{52}{25}x^5 + \frac{39}{80}x^4 + \frac{71}{10}x^3 - \frac{79}{20}x^2 - x + \frac{1}{10}",
        "F2":  r"\sin x + \sin \frac{10x}{3}",
        "F3":  r"-\sum_{k=1}^{5} k \sin[(k+1)x + k]",
        "F4":  r"-(16x^2 - 24x + 5) e^{-x}",
        "F5":  r"(3x - 1.4) \sin 18x",
        "F6":  r"-(x + \sin x) e^{-x^2}",
        "F7":  r"\sin x + \sin \frac{10x}{3} + \ln x - 0.84x + 3",
        "F8":  r"-\sum_{k=1}^{5} k \cos[(k+1)x + k]",
        "F9":  r"\sin x + \sin \frac{2x}{3}",
        "F10": r"-x \sin x",
        "F11": r"2 \cos x + \cos 2x",
        "F12": r"\sin^3 x + \cos^3 x",
        "F13": r"-np.cbrt(x^2) + np.cbrt(x^2 - 1)", # Manteniamo NumPy per F13/F18 per stabilità numerica in visualizzazione
        "F14": r"-e^{-x} \sin(2 \pi x)",
        "F15": r"\frac{x^2 - 5x + 6}{x^2 + 1}",
        "F16": r"2(x - 3)^2 + e^{0.5x^2}",
        "F17": r"x^6 - 15x^4 + 27x^2 + 250",
        "F18": r"np.where(x \le 3, (x - 2)**2, 2 \ln(x - 2) + 1)",
        "F19": r"-x + \sin 3x - 1",
        "F20": r"(\sin x - x) e^{-x^2}"
    }

    # Inserimento nel dizionario
    for nome, formula_latex in latex_formulas.items():
        if nome in funzioni:
            funzioni[nome]["latex"] = formula_latex

    # Salvataggio JSON aggiornato
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(funzioni, f, indent=4, ensure_ascii=False)
        
    print(f"[INFO] JSON aggiornato con successo in: {json_path}")

if __name__ == "__main__":
    update_json_with_latex()