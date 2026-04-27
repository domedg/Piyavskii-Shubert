# Relazione di Progetto: Ottimizzatore Globale di Piyavskii-Shubert

## 1. Introduzione e Motivazione
Il presente progetto ha lo scopo di illustrare, analizzare e implementare computazionalmente l'**Algoritmo di Piyavskii-Shubert** (1972) per la risoluzione di problemi di **Ottimizzazione Globale Deterministica** in una singola dimensione (1D).

A differenza dei tradizionali metodi iterativi basati sul gradiente (come la discesa del gradiente o le iterazioni di Newton), che possiedono un focus esclusivamente locale e sono perciò soggetti all'intrappolamento nei minimi locali di funzioni *multimodali* (funzioni con molteplici picchi e valli), l'algoritmo di Piyavskii assicura una convergenza garantita al **minimo globale assoluto** senza richiedere la differenziabilità della funzione obiettivo. 

Tutto l'impianto software (accessibile tramite dashboard interattiva) opera trattando la funzione come una *scatola nera* (black-box), di cui valuta il comportamento esclusivamente per mezzo del campionamento diretto.

---

## 2. Fondamento Matematico: La Condizione di Lipschitz
Il presupposto fondamentale, nonché l'unico requisito rigoroso per l'applicabilità del metodo, è che la funzione obiettivo $f(x)$ obbedisca alla **Condizione di Lipschitz** sull'intero dominio di ricerca $[a, b]$. 

Questo significa che l'entità della pendenza (o del rateo di variazione) della funzione deve avere un confine massimo superiore definito da una costante positiva $\mathit{L}$.
Formalmente, si deve soddisfare:
$$|f(x_1) - f(x_2)| \le L \cdot |x_1 - x_2|, \quad \forall x_1, x_2 \in [a, b]$$

L'intuizione alla base della soluzione di Piyavskii poggia interamente su questa disuguaglianza: se la funzione assume il valore $f(x_i)$ nel punto $x_i$, allora nello spazio circostante, la vera funzione $f(x)$ non potrà mai decrescere più velocemente della "caduta" generata da due rette uscenti dal punto $x_i$ aventi coefficiente angolare $+L$ e $-L$.
Tali rette formano quello che chiamiamo un *Cono di Lipschitz* inferiore.

---

## 3. L'Algoritmo della Minorante: Teoria ed Equazioni

L'algoritmo opera costruendo una **Funzione Minorante** (Lower Bound), qui indicata come $F(x)$, che gode della fondamentale proprietà di sottostimare la vera funzione in ogni punto del dominio:
$$F(x) \le f(x), \quad \forall x \in [a,b]$$

### Costruzione Empirica
Sia noto il valore della funzione in due punti adiacenti valutati: $f(x')$ e $f(x'')$ con $x' < x''$.
Costruendo i coni di Lipschitz verso il basso a partire da questi due punti, l'intersezione tra la pendenza discendente dal primo punto ($-L$) e la pendenza ascendente verso il secondo ($+L$) indicherà il valore più basso **assolutamente raggiungibile** dalla funzione in quel sottointervallo.

Il punto ascissa $\hat{x}$ dell'intersezione, che diventerà il nostro miglior "candidato" all'esplorazione, si ricava algebricamente:
$$\hat{x} = \frac{x' + x''}{2} - \frac{f(x'') - f(x')}{2L}$$

L'ordinata di questa intersezione è convenzionalmente definita **Caratteristica dell'Intervallo** e la indichiamo con $R$. Definisce il punto inferiore della "V" (il dente di sega) e si calcola come:
$$R = \frac{f(x') + f(x'')}{2} - L\frac{x'' - x'}{2}$$

> **Interpretazione Filosofica dell'equazione:**
> Notiamo che $R$ è formato da due addendi precisi. Il primo termine rappresenta la *media dei valori valutati* (favorisce lo sfruttamento intensivo, o **Exploitation**, spingendo a esplorare zone in cui abbiamo trovato valori già bassi); il secondo termine dipende all'ampiezza dell'intervallo $(x'' - x')$ sottratta (favorisce l'esplorazione spaziale, o **Exploration**, spingendo a esplorare zone larghe e ancora sconosciute in quanto potenzialmente in grado di scendere molto col favore di $L$).

---

## 4. Architettura Software e Complessità Computazionale

L'implementazione computazionale Python sviluppata è stata rigorosamente modellata per abbattere l'onere computazionale dell'originaria stesura teorica del metodo.

### Struttura Dati: Il Min-Heap (Coda di Priorità)
Al Passo 3 della formulazione iterativa base "ingenua", l'algoritmo impone la ricerca del sotto-intervallo avente la caratteristica globale $R$ minima, esplorando l'intero array di segmenti. Questo costerebbe tempo $\mathcal{O}(k)$ a ogni iterazione, dove $k$ s'ingrandisce costantemente.

L'uso geniale della struttura dati logica a **Coda di Priorità** nativa (Min-Heap in linguaggio C via CPython) permette invece di inserire ogni nuovo sottointervallo (costo di riordino logaritmico $\mathcal{O}(\log k)$) e recuperare il valore avente priorità più alta, ovvero il minimo del limite inferiore assoluto rimasto nel dominio, con costo computazionale **costante** $\mathcal{O}(1)$.

### Workflow e Fasi Iterative:
1. **Inizializzazione**: Valuta la funzione black-box ai poli $a$ e $b$. Crea l'unico macro-intervallo ed estrae istantaneamente la prima $\hat{x}$ e la sua caratteristica $R$. Le inietta nello Heap.
2. **Ciclo Main**: 
   - Estrae il sottointervallo più promettente (quello col valore di $R$ estratto dal Min-Heap minimo sull'intero dominio).
   - Valuta matematicamente l'equazione $f(x)$ in corrispondenza del punto $\hat{x}$ associato, generando il nuovo campionamento.
3. **Aggiornamento Globale**:
   - Salva e storicizza il minimo miglior punto assoluto testato finora ($f_{best}$).
   - Genera due nuovi sotto-intervalli contigui dividendo il precedente alla radice $\hat{x}$, e valuta a sua volta per entrambi l'intersezione profonda $R_{left}$ e $R_{right}$. Inietta di nuovo tutto nella Coda di Priorità e ricomincia.

---

## 5. Teoria dell'Arresto Deterministico (Convergence Theorem)

Una peculiarità eccellente di questa implementazione risiede nelle condizioni di arresto, che garantiscono un esito matematicamente inappuntabile.
Per arrestare l'algoritmo non contiamo sul "numero di iterazioni" bensì su un arresto **globale**.

Ad ogni iterazione calcoliamo $\Delta = f_{best} - R_{min}$. 
Essendo $R_{min}$ per definizione il punto più basso, asintoticamente realistico, di limite inferiore sull'intero dominio inesplorato della funzione minorante $F(x)$, **sappiamo per garanzia teorica** che la funzione bersaglio reale non assumerà mai valori sotto di esso. 
Quando questo delta cala sotto la prefissata tolleranza di ingegneria o precisione macchina $\epsilon$ (ad es. $10^{-4}$):
$$f_{best} - R_{min} \le \epsilon$$

L'algoritmo rileva automaticamente la cessazione scientifica di ogni utilità nell'eseguire altri tentativi, poichè persino il miglior punto in assoluto immaginabile dall'esistenza non dista più di una virgola dal punto empirico posseduto. **L'algoritmo s'arresta restituendo l'ottimo globale validato.**

> *Branch and Bound implicito*: Se per via topologica venisse estratto per sfortuna dallo heap un intervallo con un potenziale $R \ge f_{best}$, il sistema lo ignorerebbe tagliando il nodo del calcolo alla radice.

---

## 6. Sviluppo Dashboard 

La *delivery* finale del codice racchiude la matematica in una soluzione software in Data Visualisation moderna.
Basato su Python puro e **Streamlit**, l'applicativo fa uso estensivo della libreria **Plotly** per eseguire un re-sampling dell'history calcolata e generare una view front-end vettoriale.
Dal menu è possibile navigare funzioni lette mediante deserializzazione di JSON (dimostrando portabilità), calibrare l'inclinazione $L$ e osservare visivamente come l'errata calibrazione di questo iperparametro porti all'inefficacia dell'esplorazione, o, se preciso, garantendo una convergenza in un numero sbalorditivamente piccolo di iterazioni.
