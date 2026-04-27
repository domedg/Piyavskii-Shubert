# Relazione di Progetto: Ottimizzazione Globale (Algoritmo di Piyavskii-Shubert)

Questo documento contiene tutta la teoria matematica, i dettagli implementativi e le analisi ingegneristiche dell'algoritmo di Piyavskii-Shubert. È stato concepito per offrire una chiara visione d'insieme dell'implementazione di base e giustificare il passaggio alla Versione "Next-Gen" (Ottimizzata) per il benchmark accademico.

---

## 1. Introduzione Teorica: L'Algoritmo Base

L'algoritmo di Piyavskii-Shubert è un metodo deterministico elegante per trovare il minimo globale di una funzione continua $f(x)$ in un intervallo $[a, b]$, con un'unica precondizione: la funzione deve essere **Lipschitziana**.
Ciò significa che la sua derivata (se esiste) o la sua pendenza massima è sempre limitata da una costante $L > 0$. Matematicamente, per ogni coppia di punti $x_1, x_2 \in [a, b]$:
$$ |f(x_1) - f(x_2)| \le L |x_1 - x_2| $$

Dal punto di vista geometrico, se conosciamo il valore della funzione in un punto $x'$, la funzione non potrà sprofondare più rapidamente della pendenza $-L$. Possiamo perciò costruire una funzione "minorante" a forma di dente di sega (cono di Lipschitz):
$$ F(x) = f(x') - L |x - x'| $$

Se valutiamo la funzione agli estremi di un intervallo $[x_{left}, x_{right}]$, le due rette di pendenza $+L$ e $-L$ si intersecheranno in un punto preciso di ascissa $\hat{x}$:
$$ \hat{x} = \frac{x_{left} + x_{right}}{2} - \frac{f(x_{right}) - f(x_{left})}{2L} $$

Il valore in quel punto rappresenta il limite inferiore teorico (lower bound, che chiamiamo $R$) che la funzione potrebbe assumere nell'intervallo:
$$ R = F(\hat{x}) = \frac{f(x_{left}) + f(x_{right})}{2} - L \frac{x_{right} - x_{left}}{2} $$

### Dalla Teoria al Codice (Versione Originale)
Nel nostro codice Python, questo motore matematico è stato implementato in modo funzionale tramite due *closures* lambda, garantendo perfetta aderenza alle formule:

```python
# Calcolo del limite inferiore teorico (R)
calculate_lower_bound = lambda left_x, right_x, left_f, right_f: 0.5 * (left_f + right_f) - 0.5 * lipschitz_constant * (right_x - left_x)

# Calcolo del punto di intersezione (\hat{x})
calculate_intersection_x = lambda left_x, right_x, left_f, right_f: 0.5 * (left_x + right_x) - (right_f - left_f) / (2 * lipschitz_constant)
```

---

## 2. Il Limite della Versione Originale (Approccio "Naive")

Ad ogni iterazione, l'algoritmo divide l'intervallo più "promettente" (quello con il valore $R$ più basso), calcola $f(\hat{x})$ nel punto di mezzo, e spezza l'intervallo originale in due nuovi sotto-intervalli: $[x_{left}, \hat{x}]$ e $[\hat{x}, x_{right}]$.

Nella **Versione 1 (Originale)**, la gestione di questi intervalli avviene in modo scolastico ed "ingenuo", accumulandoli in una semplice `Lista` piatta. Questo comporta due colli di bottiglia critici:
1. **Estrazione Lenta in $\mathcal{O}(N)$**: Per trovare il segmento col potenziale peggiore, si è costretti a scorrere iterativamente l'intera lista. A tolleranze microscopiche, la lista si intasa di decine di migliaia di nodi, rendendo l'estrazione estremamente pesante.
2. **Shift della Memoria $\mathcal{O}(N)$**: L'inserimento (o concatenazione) in testa e l'estrazione causano riallocazioni continue e costose della memoria da parte del processore, un difetto strutturale che affligge linguaggi come Java e Python quando usati senza criterio.

---

## 3. La Versione "Next-Gen" (Le Tre Ottimizzazioni)

Per difendere con orgoglio il progetto al ricevimento, la **Versione Ottimizzata** integra queste tre eleganti correzioni ingegneristiche:

### 3.1. Architettura Dati: Coda di Priorità (Min-Heap)
Sostituiamo la goffa lista lineare con una **Struttura Dati ad Albero Binario (Min-Heap)**. L'Heap si auto-bilancia in tempo reale tenendo sempre l'intervallo con il valore $R$ minore in cima alla radice:
- **Inserimento:** Complessità crollata a $\mathcal{O}(\log N)$
- **Estrazione del Minimo:** Complessità crollata a $\mathcal{O}(1)$

```python
import heapq

# Estraiamo istantaneamente il segmento con potenziale minimo globale peggiore senza cicli For
current_lower_bound, _, current_left_x, current_right_x, current_left_f, current_right_f = heapq.heappop(priority_queue)
```

### 3.2. Stabilità Numerica e Tolleranza Relativa
**Prevenzione Crash:** Anziché un'Eccezione esplicita, usiamo un controllo matematico sui limiti della macchina (1e-15). Se due punti si sovrappongono troppo, usiamo un `continue` per saltare e andare ad esplorare gli altri rami intatti senza fermare l'algoritmo.
Inoltre, convertiamo la tolleranza `tol` spaziale basata su un moltiplicatore dell'ampiezza dell'intervallo originario.

```python
# Scongiuriamo loop infiniti per i limiti dei float
if (intersection_x - current_left_x) <= 1e-15 or (current_right_x - intersection_x) <= 1e-15:
    continue
```

### 3.3. Algoritmo Branch & Bound (Pre-Pruning Spaziale)
Teniamo traccia del minimo globale assoluto trovato finora, detto $f_{best}$ (`best_minimum_value`).
Quando calcoliamo un nuovo intervallo, osserviamo la sua $R$. Se $f_{best} - R \le \epsilon$, è **matematicamente impossibile** che quell'intervallo celi un risultato migliore.
Dunque, anziché inserirlo, lo falciamo ancor prima che tocchi l'Heap (Pruning preventivo).

```python
lower_bound_left = calculate_lower_bound(current_left_x, intersection_x, current_left_f, intersection_f)

# Pruning Ingegneristico: Inseriamo nell'heap SOLO se matematicamente utile
if best_minimum_value - lower_bound_left > tolerance:
    heapq.heappush(priority_queue, (lower_bound_left, ...))
```
**Risultato:** Complessità spaziale (RAM) ridotta drasticamente: da $\mathcal{O}(N)$ a $\mathcal{O}(K)$, dove $K \ll N$.

### Riepilogo Benchmark Finale
La dashboard `app.py` ti consente di selezionare la Versione 1 o la Versione 2 al volo. Mettendo a confronto le metriche, dimostrerai al professore un principio fondamentale dell'Ingegneria degli Algoritmi:

- **Iterazioni e Punti Valutati:** Le due versioni restituiscono **esattamente gli stessi valori**. L'algoritmo matematico non è stato alterato o drogato con euristiche. Inoltre, è geometricamente dimostrato che il numero di Punti Valutati è sempre pari al numero di Iterazioni + 2 (i due estremi iniziali del dominio $a$ e $b$).
- **Tempo di Esecuzione (Millisecondi):** La Versione Ottimizzata impiega una frazione infinitesima del tempo rispetto alla Versione Originale.

Questo dimostra che il vero scoglio computazionale di Piyavskii-Shubert non era il calcolo matematico della funzione, bensì l'estrazione inefficiente dei dati ($\mathcal{O}(N)$). Avendo sostituito il loop iterativo "Naive" con una struttura dati avanzata ad albero (Min-Heap in $\mathcal{O}(\log N)$) ed avendola ulteriormente potenziata con il Branch & Bound, abbiamo polverizzato i tempi di esecuzione mantenendo un rigore matematico assoluto.

Questo garantisce stabilità accademica ed efficienza ingegneristica per sfidare funzioni Lipschitziane complesse!
