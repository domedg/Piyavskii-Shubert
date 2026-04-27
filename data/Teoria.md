# Relazione Tecnica Estesa: Fondamenti Matematici dell'Ottimizzazione Globale per Funzioni Lipschitziane

## 1. Topologia del Problema e Teorema di Weierstrass
Nell'ambito dell'analisi numerica, la ricerca del minimo globale di una funzione rappresenta una delle sfide computazionali più ardue. 

Sia definita una funzione obiettivo non lineare $f: \Omega \rightarrow \mathbb{R}$. Assumiamo che il dominio di ricerca $\Omega$ sia un sottoinsieme compatto di $\mathbb{R}$, specificamente un intervallo chiuso e limitato $[a, b]$. 
Per il **Teorema di Weierstrass**, se $f(x)$ è una funzione continua in un dominio compatto, essa ammette sempre almeno un punto di minimo e un punto di massimo globale assoluto. Di conseguenza, sappiamo con certezza che esiste almeno un $x^* \in \Omega$ tale per cui:
$$f(x^*) \le f(x) \quad \forall x \in \Omega$$

Tuttavia, la sola continuità non fornisce alcuna informazione su *come* e *quanto velocemente* la funzione oscilli tra due punti valutati. Se valutiamo la funzione in una griglia di punti finita, il vero minimo globale potrebbe annidarsi in una "buca" infinitamente stretta e profonda tra due punti della griglia, rendendo la sua individuazione computazionalmente impossibile con un campionamento discreto. 
Per superare questo ostacolo matematico, è necessario regolarizzare il problema imponendo un vincolo analitico sulla rapidità di variazione della funzione.

## 2. La Condizione di Lipschitz e la Regolarizzazione
Il vincolo più robusto per garantire la risolvibilità algoritmica del problema dell'ottimizzazione globale è l'appartenenza della funzione alla classe delle funzioni lipschitziane.

### 2.1 Definizione Formale
Una funzione $f(x)$ è detta lipschitziana sull'intervallo $\Omega$ se esiste una costante reale $L \in (0, \infty)$ tale che, per ogni coppia di punti $x_1, x_2 \in \Omega$, la disuguaglianza seguente sia sempre soddisfatta:
$$|f(x_1) - f(x_2)| \le L |x_1 - x_2|$$

### 2.2 Connessione con il Calcolo Differenziale
Se la funzione è differenziabile con continuità ($\mathcal{C}^1$) su $\Omega$, per il Teorema di Lagrange (o del Valor Medio), esiste sempre un punto $c$ compreso tra $x_1$ e $x_2$ tale che:
$$\frac{f(x_1) - f(x_2)}{x_1 - x_2} = f'(c)$$
Applicando il valore assoluto, si evince immediatamente che la costante di Lipschitz $L$ coincide con il limite superiore assoluto della derivata prima sull'intero dominio:
$$L \ge \sup_{x \in \Omega} |f'(x)|$$
Dal punto di vista geometrico, questo significa che la pendenza della retta tangente (o secante) al grafico di $f(x)$ non può mai essere più ripida di $L$ né più decrescente di $-L$.

### 2.3 Il Cono Minorante (Bounding Cone)
Se valutiamo la funzione in un generico punto esplorativo $x_k$ ottenendo il valore $f(x_k)$, l'equazione di Lipschitz ci garantisce che per qualsiasi altro punto $x$ incognito, la funzione reale non potrà scendere sotto una determinata soglia. Risolvendo il valore assoluto otteniamo:
$$f(x) \ge f(x_k) - L|x - x_k|$$
Questa equazione definisce un "cono rovesciato" con vertice in $(x_k, f(x_k))$ e rami rettilinei di pendenza $+L$ e $-L$. La vera funzione $f(x)$ giacerà sempre *al di sopra* di questa struttura o, al limite, vi aderirà.

> `[INSERIRE QUI SCREENSHOT: Diagramma geometrico che mostra la curva di f(x) e il cono rovesciato generato da un singolo punto campionato, evidenziando le pendenze +L e -L]`

## 3. L'Algoritmo di Piyavskij-Shubert (Metodo delle Poligonali)
Questo algoritmo deterministico è il pilastro per la risoluzione del problema. Esso sfrutta la proprietà dei coni minoranti aggregando le informazioni raccolte punto dopo punto, con l'obiettivo di isolare l'area in cui risiede il minimo globale.

### 3.1 Costruzione dell'Inviluppo Inferiore Universale
Supponiamo che l'algoritmo al passo $k$-esimo abbia già campionato la funzione in un insieme di punti distinti $X_k = \{x_1, x_2, \dots, x_k\}$, ordinati in senso strettamente crescente $a = x_1 < x_2 < \dots < x_k = b$.

Per ciascuno di questi punti possiamo generare un cono minorante. La funzione minorante globale (o underestimator) $\Phi_k(x)$ viene definita come il limite inferiore più "stretto" (cioè il più grande) che possiamo costruire sovrapponendo tutti i coni:
$$\Phi_k(x) = \max_{1 \le i \le k} \{ f(x_i) - L|x - x_i| \}$$
Questa funzione $\Phi_k(x)$ risulta essere una poligonale (una linea spezzata "a dente di sega"). Poiché approssima $f(x)$ dal basso, è matematicamente garantito che il minimo globale della poligonale $\Phi_k(x)$ sia inferiore o uguale al minimo globale della funzione vera.

### 3.2 Derivazione Analitica delle Intersezioni
La funzione $\Phi_k(x)$ presenta i suoi minimi locali nei punti in cui si incrociano il ramo decrescente del cono originato da $x_i$ e il ramo crescente del cono originato da $x_{i+1}$. Per trovare questi punti strategici di intersezione (che rappresentano le posizioni più probabili per la presenza del minimo globale incognito), dobbiamo risolvere un sistema lineare.

Siano $y_A$ e $y_B$ le equazioni dei due rami tra $x_i$ e $x_{i+1}$:
1. Ramo decrescente da $x_i$: $\quad y_A = f(x_i) - L(x - x_i)$
2. Ramo crescente da $x_{i+1}$: $\quad y_B = f(x_{i+1}) + L(x - x_{i+1})$

Imponendo $y_A = y_B$, determiniamo l'ascissa di intersezione $x^*$:
$$f(x_i) - L x + L x_i = f(x_{i+1}) + L x - L x_{i+1}$$
$$2Lx = L(x_i + x_{i+1}) + f(x_i) - f(x_{i+1})$$
Dividendo per $2L$, otteniamo in modo inequivocabile la coordinata $x^*$:
$$x^* = \frac{x_i + x_{i+1}}{2} + \frac{f(x_i) - f(x_{i+1})}{2L}$$

Sostituendo $x^*$ in una delle due equazioni della retta (es. nella $y_A$), isoliamo l'ordinata $y^*$, che rappresenta il valore minimo stimato nell'intervallo $[x_i, x_{i+1}]$:
$$y^* = f(x_i) - L\left[ \frac{x_i + x_{i+1}}{2} + \frac{f(x_i) - f(x_{i+1})}{2L} - x_i \right]$$
Semplificando i termini, si arriva alla forma canonica utilizzata in tutti i solutori numerici:
$$y^* = \frac{f(x_i) + f(x_{i+1})}{2} - L\frac{x_{i+1} - x_i}{2}$$

> `[INSERIRE QUI SCREENSHOT: Dettaglio algebrico e visivo di un singolo intervallo tra x_i e x_{i+1}, mostrando graficamente come si forma il triangolo inferiore e l'esatta posizione del punto (x*, y*)]`

## 4. Architettura Logica ed Esecutiva dell'Algoritmo
L'implementazione software deve seguire questo schema iterativo rigoroso:

1. **Inizializzazione (Fase Boot):** Campionare i bordi del dominio valutando $f(a)$ e $f(b)$. Memorizzare l'insieme dei punti campionati $X = \{a, b\}$ e i rispettivi valori $Z = \{f(a), f(b)\}$. Definire la tolleranza $\epsilon$.
2. **Ciclo di Aggiornamento Poligonale:** * Per ogni coppia di punti consecutivi memorizzati $[x_i, x_{i+1}]$, calcolare l'intersezione $(x_i^*, y_i^*)$ sfruttando le formule analitiche precedentemente derivate.
3. **Selezione del Minimo Relativo Globale:** * Tra tutti i punti di intersezione appena calcolati, individuare quello con la componente $y$ minore assoluta. Sia questo l'indice $t$:
     $$y_t^* = \min_{i} y_i^*$$
4. **Campionamento e Inserimento:**
   * Definire il nuovo punto di campionamento strategico $x_{new} = x_t^*$.
   * Valutare $f(x_{new})$ chiamando la funzione obiettivo oggettiva.
   * Aggiungere $x_{new}$ nell'array ordinato delle ascisse $X$ e $f(x_{new})$ nell'array delle ordinate $Z$. Questa operazione "rompe" l'intervallo $[x_t, x_{t+1}]$ originario, affinando la risoluzione locale della poligonale.
5. **Verifica della Convergenza:** Il ciclo continua fino al soddisfacimento del criterio di arresto rigoroso.

## 5. Criteri di Arresto e Garanzia di Accuratezza Asintotica
Il vero potere dei metodi basati sulla lipschitzianità è la garanzia formale di aver confinato l'errore asintotico globale.

Sia $f_{best}^{(k)}$ il miglior valore della funzione (il più piccolo) osservato fisicamente dopo $k$ valutazioni. Questo è un limite superiore (upper bound) sicuro per il minimo globale reale:
$$f^* \le f_{best}^{(k)} = \min \{ f(x_1), f(x_2), \dots, f(x_k) \}$$

Simultaneamente, definiamo $R_k$ come il limite inferiore globale (lower bound), corrispondente al più profondo tra i vertici $y_i^*$ correnti calcolati sulla poligonale minorante $\Phi_k(x)$:
$$R_k = \min_{1 \le i \le k-1} y_i^*$$

Il Teorema fondamentale per l'arresto assicura che il vero valore incognito si trovi incapsulato in questo scarto (gap di sub-ottimalità):
$$R_k \le f^* \le f_{best}^{(k)}$$

L'algoritmo si interrompe (Break Condition) all'iterazione $k$ se l'ampiezza di questa finestra scende sotto una tolleranza impostata dall'utente $\epsilon > 0$:
$$f_{best}^{(k)} - R_k \le \epsilon$$
Tale disuguaglianza previene sia l'arresto prematuro (errore di troncamento non desiderato) sia i cicli infiniti dovuti alla limitata precisione di macchina (errore di arrotondamento floating-point tipico dello standard IEEE 754).

## 6. Dinamiche Sensibili: La Costante L come Parametro Iper-Critico
Nell'implementazione software, la scelta della Costante di Lipschitz $L$ rappresenta un trade-off fra sicurezza esplorativa ed efficienza computazionale.

1. **Eccessiva Sovrastima ($L_{inserita} \gg L_{reale}$):** I coni risultano profondissimi. Il termine $- L\frac{x_{i+1} - x_i}{2}$ nella formula di $y^*$ sovrasta l'effettiva differenza delle altezze. Di conseguenza, l'algoritmo frammenterà quasi uniformemente l'intero dominio $\Omega$ comportandosi a tutti gli effetti come un algoritmo di Grid Search cieco (costo computazionale sub-ottimale, eccesso di valutazioni, ma certezza totale).
2. **Sottostima ($L_{inserita} < L_{reale}$):** Il disastro numerico. Se si sottostima $L$, il cono generato sarà troppo "aperto" o piatto, tagliando la funzione obiettivo reale. La proprietà $\Phi_k(x) \le f(x)$ viene violata, causando un artefatto numerico per cui l'algoritmo dichiara convergenza in una regione errata, producendo falsi positivi sistematici.

Per bilanciare la robustezza senza collassare nell'inefficienza prestazionale, estensioni successive al metodo Shubert puro implementano tecniche per calibrare localmente la pendenza $L_i$ in specifici sotto-intervalli, attingendo a metodi predittivi adattivi (es. Informazione Statistica, Global vs Local searches).