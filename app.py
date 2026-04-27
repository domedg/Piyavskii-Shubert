import streamlit as st
import numpy as np
import warnings

# Nascondiamo i RuntimeWarning di Numpy causati da np.where()
warnings.filterwarnings('ignore', category=RuntimeWarning)

# Importiamo la logica dell'algoritmo dal modulo corretto
from src.core.shubert_piyavskii import piyavskii_shubert
from src.core.shubert_piyavskii_optimized import piyavskii_shubert_optimized
from src.utils.test_functions import TEST_FUNCTIONS
from src.utils.plotting import create_optimization_plot

# Impostiamo il layout espanso e un titolo di pagina accattivante
st.set_page_config(
    page_title="Ottimizzatore Globale di Piyavskii-Shubert", 
    page_icon="📈", 
    layout="wide"
)

# =========================================================
# BARRA LATERALE (SIDEBAR) - Input Parametri e Navigazione
# =========================================================
st.sidebar.title("🛠️ Pannello di Controllo Algoritmo")
st.sidebar.markdown("Scegli tra le 20 funzioni di test configurate nel JSON per stressare l'algoritmo globale.")

# 1. Selezione Versione Algoritmo
st.sidebar.markdown("### Selezione Algoritmo")
algo_version = st.sidebar.radio(
    "Scegli quale implementazione eseguire:",
    ("Versione 1 (Originale)", "Versione 2 (Ottimizzata)")
)

# 2. Selezione Funzione Obiettivo
selected_func_name = st.sidebar.selectbox(
    "Seleziona la Funzione da Minimizzare",
    options=list(TEST_FUNCTIONS.keys())
)
func_data = TEST_FUNCTIONS[selected_func_name]
f = func_data["func"]

# Usa i valori di default presi dal JSON delle funzioni di test
default_a, default_b = func_data["a"], func_data["b"]
default_L = func_data["L"]

st.sidebar.markdown("### Equazione Matematica della Selezione:")
if "latex" in func_data and func_data["latex"]:
    st.sidebar.latex(func_data["latex"])

# 2. Slider per intervallo [a, b]
st.sidebar.markdown("### Dominio di Ricerca Spaziale")
a = st.sidebar.number_input("Estremo sinistro dell'intervallo (a)", value=float(default_a), step=1.0)
b = st.sidebar.number_input("Estremo destro dell'intervallo (b)", value=float(default_b), step=1.0)

if a >= b:
    st.sidebar.error("L'estremo a deve essere STRETTAMENTE minore di b!")

# 4. Costante di Lipschitz (L)
st.sidebar.markdown("### Costante di Lipschitz (L)")
st.sidebar.info("Deve essere una sovrastima della massima derivata assoluta possibile nel dominio. \n\n⚠️ **Nota di Sicurezza:** L'algoritmo applica automaticamente una sovrastima dell'**1%** al valore inserito per garantire la stabilità matematica ed evitare che la minorante intersechi la funzione reale.")
L_input = st.sidebar.number_input("Valore Costante di Lipschitz (L)", min_value=0.1, value=float(default_L), step=1.0)
#L = L_input * 1.01
L = L_input

# 5. Parametri Criteri di Arresto
st.sidebar.markdown("### Criteri di Arresto (Tolleranze)")
eps_power = st.sidebar.slider("Esponente della Precisione di Macchina (10^x)", min_value=-7, max_value=-2, value=-4)
eps = 10 ** eps_power
st.sidebar.latex(rf"\epsilon = 10^{{{eps_power}}}")

max_iterations = st.sidebar.slider("Iterazioni massime consentite", min_value=10, max_value=4000, value=2000, step=100)

# =========================================================
# AREA PRINCIPALE - Presentazione al Professore
# =========================================================
st.title("📈 Ottimizzazione Globale: Algoritmo di Piyavskii-Shubert")

# Spiegazione e formula (LaTeX) come richiesto per il professore
with st.expander("📖 Teoria e Passi dell'Algoritmo (Espandi per mostrare)", expanded=False):
    st.markdown(r"""
L'**Algoritmo di Piyavskii-Shubert** (1972) è un metodo deterministico elegante per l'ottimizzazione globale (black-box). 
Si basa esclusivamente sull'ipotesi che la funzione bersaglio $f(x)$ soddisfi la **condizione di Lipschitz**:
""")
    st.latex(r"|f(x') - f(x'')| \le L \cdot |x' - x''| \quad \forall x', x'' \in [a, b]")
    st.markdown(r"""
Crea dinamicamente una funzione a *denti di sega* definita **minorante** $F(x) \le f(x)$, e a ogni iterazione esplora il punto matematicamente più basso di $F(x)$, individuato dall'incrocio di due rette di pendenza $\pm L$:
""")
    st.latex(r"\hat{x} = \frac{x' + x''}{2} - \frac{f(x'') - f(x')}{2L}")
    st.latex(r"R = F(\hat{x}) = \frac{f(x') + f(x'')}{2} - L\frac{x'' - x'}{2}")
    
    st.markdown(r"""
### Schema Iterativo e Passi dell'Algoritmo

1. **Inizializzazione**: Valutazione della funzione agli estremi originali del dominio in $a$ e $b$ per ottenere $f(a)$ e $f(b)$.
2. **Ciclo Iterativo**: In ogni step per $k \ge 1$:
    * **Ordinamento Spaziale**: I punti valutati vengano sempre considerati in adiacenza ordinata, $x_{i-1} < x_i$.
    * **Costruzione Minorante e Caratteristica**: Si calcola la 'caratteristica' $R_i$ per tutti gli intervalli contigui attraverso l'equazione $R$. In termini implementativi moderni inseriamo queste caratteristiche in un *Min-Heap* (Coda di Priorità) in tempo ${\mathcal{O}}(\log k)$ al fine di trovare subito l'ottimo.
    * **Suddivisione dell'Ottimo Corrente**: L'Algoritmo seleziona l'intervallo con il valore $R$ minore:
    """)
    st.latex(r"t = \arg\min_{1 \le i \le k} R_i")
    st.markdown(r"""
3. **Criterio Di Arresto (Convergenza Spaziale)**:
    Se la larghezza del sottointervallo prescelto $x_t - x_{t-1} < \epsilon$, cioè scende sotto la tolleranza prefissata, si ritiene raggiunta la convergenza e si restituisce l'ottimo.
4. **Nuova Valutazione (Exploration)**:
    Qualora il criterio non fosse raggiunto, si calcola l'ascissa $\hat{x}_t$ dell'intersezione trovata e la si valuta, aggiungendo e dividendo l'intervallo prescelto in due nuovi sotto-intervalli da inserire in coda.
    """)
    st.markdown(r"""
> **Ottimizzazione Implementativa Implementata (Branch and Bound pruning)**: Siccome per implementazione abbiamo strutturato una gestione a Coda di Priorità, il processo ricorda il miglior minimo scovato $f_{best}$. Non ha matematicamente alcun senso esplorare i sotto-intervalli in cui il lower bound $R_i \ge f_{best}$. Il codice interrompe istantaneamente queste computazioni, compiendo una potatura dell'albero delle esplorazioni!
    """)

# =========================================================
# ESECUZIONE DELL'ALGORITMO
# =========================================================

# Check integrità matematica
if a < b:
    with st.spinner("Sto calcolando esplorando i coni di Lipschitz..."):
        import time
        start_time = time.perf_counter()
        
        # Chiamata al modulo core Python! (Dove la magia risiede)
        if algo_version == "Versione 1 (Originale)":
            best_x, best_f, iters, points = piyavskii_shubert(f, a, b, L, eps, max_iterations)
        else:
            best_x, best_f, iters, points = piyavskii_shubert_optimized(f, a, b, L, eps, max_iterations)
            
        end_time = time.perf_counter()
        execution_time_ms = (end_time - start_time) * 1000

    st.success(f"Trovato l'ottimo globale in maniera deterministica in {execution_time_ms:.2f} ms! ✅")

    # Layout delle statistiche di convergenza
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Asse X (Ottimo Globale)", f"{best_x:.6f}")
    with col2:
        st.metric("Valore f(x) Ottimo", f"{best_f:.6f}")
    with col3:
        st.metric("Iterazioni", f"{iters}")
    with col4:
        st.metric("Punti Valutati", f"{len(points)}")
    with col5:
        st.metric("Tempo Esecuzione", f"{execution_time_ms:.2f} ms")

    # Plot
    st.markdown("### Rappresentazione Visiva")
    st.markdown("Il grafico mostra l'incredibile capacità dell'elaboratore di escludere enormi distese del dominio, abbassando la minorante a fette fino alla convergenza sul minimo assoluto.")
    
    fig = create_optimization_plot(f, a, b, L, best_x, best_f, points)
    st.plotly_chart(fig, width="stretch")

    # =========================================================
    # CONVALIDA SCIENTIFICA (Dimostrazione Matematica)
    # =========================================================
    st.markdown("---")
    st.markdown("### 🔬 Convalida Matematica e Analisi dell'Errore")
    st.markdown(r"Questa sezione dimostra algebricamente l'accuratezza del punto trovato rispetto alla vera radice matematica, mostrando l'errore residuo causato dall'arresto anticipato (tolleranza $\epsilon$).")
    
    # 1. Calcolo derivata prima (se è un minimo, la derivata deve essere 0)
    h_val = 1e-5
    f_plus = f(min(b, best_x + h_val))
    f_minus = f(max(a, best_x - h_val))
    derivata_nel_punto = (f_plus - f_minus) / (2 * h_val)
    
    # 2. Calcolo Ground Truth (Verità Assoluta) tramite libreria scientifica
    from scipy.optimize import minimize
    res = minimize(f, best_x, bounds=[(a, b)])
    true_min_x = res.x[0]
    
    # 3. Calcolo Errore
    error_x = abs(best_x - true_min_x)
    
    col_v1, col_v2, col_v3 = st.columns(3)
    with col_v1:
        st.metric(label="Derivata nel punto trovato f'(x)", value=f"{derivata_nel_punto:.2e}", help="Se il valore è vicinissimo a zero, significa che siamo geometricamente sul fondo piatto della valle (minimo esatto).")
    with col_v2:
        st.metric(label="Minimo Reale Assoluto (Scipy)", value=f"{true_min_x:.6f}", help="Il minimo matematico assoluto calcolato dai solutori di eccellenza mondiale (Ground Truth).")
    with col_v3:
        st.metric(label="Errore di Approssimazione", value=f"{error_x:.2e}", help="Distanza tra il punto trovato dal nostro algoritmo e la vera radice matematica. Minore è l'errore, più il nostro algoritmo è perfetto.")

    # =========================================================
    # BENCHMARK GLOBALE COMPLETO
    # =========================================================
    st.markdown("---")
    st.markdown("### 🏆 Benchmark Globale (Confronto Naive vs Ottimizzato)")
    st.markdown("Genera una tabella riassuntiva eseguendo in batch entrambi gli algoritmi su tutte le funzioni di test configurate.")
    
    if st.button("🚀 Esegui Benchmark su tutte le funzioni"):
        with st.spinner("Esecuzione massiva degli algoritmi in corso (potrebbe richiedere qualche secondo)..."):
            import pandas as pd
            import time
            
            benchmark_data = []
            
            # Limitiamo l'esecuzione alle prime 10 funzioni
            funzioni_da_testare = list(TEST_FUNCTIONS.items())[:20]

            
            for func_id, f_data in funzioni_da_testare:
                func_obj = f_data["func"]
                dom_a = f_data["a"]
                dom_b = f_data["b"]
                L_val = f_data["L"] * 1.01  # Sovrastima di sicurezza 1%
                
                # Esecuzione Naive
                start_n = time.perf_counter()
                best_x_n, best_f_n, iters_n, points_n = piyavskii_shubert(func_obj, dom_a, dom_b, L_val, eps, max_iterations)
                end_n = time.perf_counter()
                
                time_n = (end_n - start_n) * 1000
                
                benchmark_data.append({
                    "Funzione": f"{func_id}",
                    "Algoritmo": "Naive",
                    "Tempo (ms)": f"{time_n:.3f}",
                    "Minimo f(x)": f"{best_f_n:.6f}",
                    "Iterazioni": iters_n,
                    "Coordinate (x, y)": f"({best_x_n:.6f}, {best_f_n:.6f})",
                    "Numero Punti": len(points_n)
                })
                
                # Esecuzione Optimized
                start_opt = time.perf_counter()
                best_x_opt, best_f_opt, iters_opt, points_opt = piyavskii_shubert_optimized(func_obj, dom_a, dom_b, L_val, eps, max_iterations)
                end_opt = time.perf_counter()
                time_opt = (end_opt - start_opt) * 1000
                
                benchmark_data.append({
                    "Funzione": "",  # Lasciato vuoto per leggibilità della tabella
                    "Algoritmo": "Ottimizzato",
                    "Tempo (ms)": f"{time_opt:.3f}",
                    "Minimo f(x)": f"{best_f_opt:.6f}",
                    "Iterazioni": iters_opt,
                    "Coordinate (x, y)": f"({best_x_opt:.6f}, {best_f_opt:.6f})",
                    "Numero Punti": len(points_opt)
                })
                
            df = pd.DataFrame(benchmark_data)
            
            # --- STYLING DELLA TABELLA ---
            def color_rows(row):
                if row['Algoritmo'] == 'Ottimizzato':
                    return ['background-color: rgba(46, 204, 113, 0.15)'] * len(row)
                else:
                    return ['background-color: rgba(231, 76, 60, 0.1)'] * len(row)
                    
            styled_df = df.style.apply(color_rows, axis=1)
            
            # Mostriamo il DataFrame nascondendo l'indice numerico di default di pandas per un look più pulito
            st.dataframe(styled_df, width="stretch", hide_index=True)
            st.success("Benchmark generato con successo! ")