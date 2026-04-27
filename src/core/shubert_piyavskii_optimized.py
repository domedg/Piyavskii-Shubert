import heapq
import itertools
from typing import Callable, Tuple, List

def piyavskii_shubert_optimized(
    objective_function: Callable[[float], float], 
    domain_start: float, 
    domain_end: float, 
    lipschitz_constant: float, 
    tolerance: float = 1e-4, 
    max_iterations: int = 1000
) -> Tuple[float, float, int, List[Tuple[float, float]]]:
    r"""
    Algoritmo di Piyavskii-Shubert Ottimizzato.
    
    Implementa miglioramenti sulla stabilità numerica, l'efficienza delle strutture dati
    e Pruning.
    """
    
    # 1. VALUTAZIONE INIZIALE
    function_value_start = objective_function(domain_start)
    function_value_end = objective_function(domain_end)
    evaluated_points = [(domain_start, function_value_start), (domain_end, function_value_end)]
    
    # Inizializziamo il best_minimum_value (Ottimo Globale Corrente)
    best_minimum_value = min(function_value_start, function_value_end)
    best_minimum_x = domain_start if function_value_start < function_value_end else domain_end
    
    # Adattamento della tolleranza all'ampiezza del dominio per coerenza spaziale
    effective_tolerance = tolerance * (domain_end - domain_start)
    
    # -- Funzioni di supporto matematico --
    
    # 1. Calcolo del limite inferiore teorico (Caratteristica R)
    # Questa formula calcola il valore minimo possibile che la funzione f(x) può raggiungere
    # nell'intervallo [left_x, right_x]. Si basa sull'ipotesi che la funzione scenda con
    # la massima pendenza possibile definita dalla costante di Lipschitz L a partire da entrambi gli estremi.
    # Formula matematica: R = (f(a) + f(b))/2 - L*(b - a)/2
    # dove R viene definita Caratteristica dell'intervallo [a, b], definisce il punto inferiore del dente di sega.
    calculate_lower_bound = lambda left_x, right_x, left_f, right_f: 0.5 * (left_f + right_f) - 0.5 * lipschitz_constant * (right_x - left_x)
    
    # 2. Calcolo del punto di intersezione delle rette (x_hat)
    # Calcola l'ascissa del punto in cui le due rette con pendenza +L e -L si incontrano.
    # Questo punto rappresenta la "valle" del dente di sega (M-conica) ed è il punto in cui
    # andremo a valutare fisicamente la nostra funzione obiettivo nella fase di Exploration.
    # Formula matematica: x_hat = (a + b)/2 - (f(b) - f(a))/(2*L)
    # Rappresenta il valore dell'ascissa del punto R che è il punto più basso del dente di sega.
    calculate_intersection_x = lambda left_x, right_x, left_f, right_f: 0.5 * (left_x + right_x) - (right_f - left_f) / (2 * lipschitz_constant)

    # 2. STRUTTURA DATI: MIN-HEAP
    # Un Min-Heap è un albero binario in cui il valore di ciascun nodo è minore o uguale
    # a quello dei suoi figli. Ci permette di estrarre in tempo O(1) e inserire in tempo O(log N)
    # il nostro "intervallo più promettente" (quello col 'lower_bound' più basso).
    # Utilizziamo un contatore (itertools.count) per evitare errori di confronto nell'heap
    # quando due intervalli hanno lo stesso identico lower bound (funge da tie-breaker / criterio di spareggio).
    # E' un generatore di numeri che parte da 0 e incrementa di 1 ad ogni chiamata next, garantendo unicità.
    tie_breaker = itertools.count() 
    
    # Calcoliamo il "lower bound" dell'intero intervallo iniziale [a,b]
    initial_lower_bound = calculate_lower_bound(domain_start, domain_end, function_value_start, function_value_end)
    
    # Inizializziamo la lista che fungerà da coda di priorità (Min-Heap in Python con 'heapq').
    # La chiave di ordinamento (elemento in posizione 0 della tupla) è proprio il lower bound.
    priority_queue = [(initial_lower_bound, next(tie_breaker), domain_start, domain_end, function_value_start, function_value_end)]
    
    # Variabile contatore per tenere traccia delle iterazioni effettivamente svolte
    actual_iterations = 0
    
    # 3. CICLO ITERATIVO
    # Eseguiamo l'algoritmo fino al limite massimo di iterazioni consentite
    for _ in range(max_iterations):
        # Condizione di sicurezza: se per qualche motivo l'heap è vuoto, fermiamo il ciclo
        if not priority_queue:
            break  
            
        # Estraiamo dalla coda di priorità (heap) l'intervallo col minor lower bound in assoluto
        current_lower_bound, _, current_left_x, current_right_x, current_left_f, current_right_f = heapq.heappop(priority_queue)
        
        # -- CRITERIO DI ARRESTO GLOBALE (PIYAVSKII-SHUBERT) --
        # Verifichiamo se il peggior "lower bound" possibile (current_lower_bound) è ormai vicinissimo
        # al miglior valore reale che abbiamo già trovato (best_minimum_value). Se la differenza
        # è inferiore alla tolleranza, abbiamo la garanzia matematica che non esistono minimi migliori.
        # Questo perchè essendo current_lower_bound (R_min) per definizione il punto piu basso, se è già vicino 
        # al best_minimum_value, non esistono minimi migliori.
        if best_minimum_value - current_lower_bound <= effective_tolerance:
            break
            
        # -- CRITERIO DI ARRESTO SPAZIALE --
        # Termina se l'ampiezza dell'intervallo che stiamo per esplorare è scesa sotto la soglia.
        if (current_right_x - current_left_x) <= effective_tolerance:
            break
            
        # -- PASSO 2: CALCOLO DEL NUOVO PUNTO (x_hat) --
        # Calcoliamo l'ascissa del vertice inferiore del "dente di sega" in questo intervallo.
        intersection_x = calculate_intersection_x(current_left_x, current_right_x, current_left_f, current_right_f)
        
        # Protezione numerica contro loop infiniti dovuti ai limiti dei floating-point (1e-15).
        # Se il nuovo punto calcolato si sovrappone agli estremi, lo ignoriamo.
        if intersection_x <= current_left_x or intersection_x >= current_right_x:
            continue
            
        # -- PASSO 3: VALUTAZIONE DELLA FUNZIONE (Black Box) --
        # Interroghiamo la funzione obiettivo nel punto x_hat per scoprire il suo VERO valore.
        intersection_f = objective_function(intersection_x)
        evaluated_points.append((intersection_x, intersection_f))
        
        # Aggiornamento dell'Ottimo Globale Corrente
        if intersection_f < best_minimum_value:
            best_minimum_value = intersection_f
            best_minimum_x = intersection_x

        # =========================================================================
        # INSERIMENTO IN MIN-HEAP + Pruning
        # =========================================================================
        # Questa sezione contiene il nucleo dell'ottimizzazione spaziale.
        # Il punto appena valutato (x_hat) ha spezzato l'intervallo padre in due:
        # [left, x_hat] e [x_hat, right].
        # Calcoliamo la Caratteristica R (lower_bound) per entrambi.
        
        lower_bound_left = calculate_lower_bound(current_left_x, intersection_x, current_left_f, intersection_f)
        
        # PRUNING:
        # Se il limite inferiore (R) del nuovo sotto-intervallo non potrà MAI scendere
        # al di sotto del miglior minimo reale che abbiamo già in tasca (best_minimum_value),
        # è matematicamente inutile inserire questo intervallo nell'albero. Lo "potiamo" (pruning).
        # Questo riduce drasticamente l'uso della RAM e accorcia l'albero.

        # heapq.heappush esegue un sorting automatico dell'heap dopo l'inserimento, 
        # garantendo che il prossimo pop estragga sempre l'intervallo con il minor lower bound.
        if best_minimum_value - lower_bound_left > tolerance:
            heapq.heappush(priority_queue, (lower_bound_left, next(tie_breaker), current_left_x, intersection_x, current_left_f, intersection_f))
            
        lower_bound_right = calculate_lower_bound(intersection_x, current_right_x, intersection_f, current_right_f)
        
        # Ripetiamo il Pre-Pruning per il ramo destro.
        if best_minimum_value - lower_bound_right > tolerance:
            heapq.heappush(priority_queue, (lower_bound_right, next(tie_breaker), intersection_x, current_right_x, intersection_f, current_right_f))
        # =========================================================================

        actual_iterations += 1

    return best_minimum_x, best_minimum_value, actual_iterations, evaluated_points
