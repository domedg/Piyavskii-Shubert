# Ottimizzatore Globale di Piyavskii-Shubert 📈

Una dashboard interattiva basata su **Python e Streamlit** per risolvere e visualizzare problemi di *Ottimizzazione Globale Deterministica* usando l'algoritmo di Piyavskii-Shubert per funzioni Lipschitziane.

![Demo Video](./piyavskii_demo.webp)

## ✨ Features
- **Piyavskii-Shubert 1D**: Algoritmo globalmente infallibile per minmizzare funzioni *black-box* a densità multimodale.
- **Struttura a O(1) e O(log k)**: Ottimizzazione della Complessità tramite Coda di Priorità (Min-Heap in CPython).
- **Pruning (Branch & Bound)**: Evita calcoli inutili interrompendo l'esplorazione spaziale quando il lower bound scende sotto l'ottimo già ottenuto.
- **Visualizzazione Dinamica**: Disegna istantaneamente la *Funzione Minorante a Dente di Sega* interfacciandosi con Plotly per rappresentare le iterazioni di convergenza.

## 🚀 Come avviare l'Applicazione

Clona il repository sul tuo computer e apri un terminale nella cartella del progetto:

```bash
# 1. Installa tutte le dipendenze richieste
pip install -r requirements.txt

# 2. Avvia la Dashboard Streamlit
streamlit run app.py
```
Il sistema avvierà un web server locale. Apri la pagina `http://localhost:8501` nel tuo browser.

## 🧮 Base Matematica 

L'algoritmo crea dinamicamente una funzione *minorante* $F(x) \le f(x)$ che imita il profilo del tetto di pendenza della funzione vera, sfruttando l'ipotesi della derivata massima stimata (Costante di Lipschitz $L$). Valuta il punto d'incrocio tra due pendenze per dedurre dove si possa fisicamente nascondere il minimo:

$$ R = F(\hat{x}) = \frac{f(x') + f(x'')}{2} - L\frac{x'' - x'}{2} $$

Troverai la documentazione accademica completa per l'esame leggendo il file `Relazione_Progetto.md` in questo repo!
