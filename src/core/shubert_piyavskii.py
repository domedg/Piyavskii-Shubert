import heapq
import itertools
from typing import Callable, Tuple, List

def piyavskii_shubert(
    objective_function: Callable[[float], float], 
    domain_start: float, 
    domain_end: float, 
    lipschitz_constant: float, 
    tolerance: float = 1e-4, 
    max_iterations: int = 1000
) -> Tuple[float, float, int, List[Tuple[float, float]]]:
    r"""
    Algoritmo di Piyavskii-Shubert per l'Ottimizzazione Globale (Minimizzazione).
    
    Questo metodo trova il minimo globale di una funzione Lipschitziana f
    in un intervallo [a, b]. Funziona costruendo progressivamente una 
    funzione "minorante" (lower bound) a forma di denti di sega.

    Parametri:
    ----------
    objective_function : Callable
        La funzione matematica da analizzare e minimizzare.
    domain_start, domain_end : float
        Estremi dell'intervallo di ricerca (dominio).
    lipschitz_constant : float
        Costante di Lipschitz (stima \hat{L}). Rappresenta la massima 
        pendenza possibile della funzione nell'intervallo.
    tolerance : float
        Tolleranza (\epsilon). Criterio di arresto globale o spaziale.
    max_iterations : int
        Numero massimo di valutazioni della funzione per evitare cicli infiniti.

    Ritorna:
    --------
    best_minimum_x (float): L'ascissa del minimo globale trovato.
    best_minimum_value (float): Il valore della funzione nel minimo globale.
    iteration_count (int): Numero di iterazioni impiegate dall'algoritmo.
    evaluated_points (List[Tuple]): Lista di punti (x, f(x)) esplorati, utile per il plottaggio.
    """
    
    # 1. VALUTAZIONE INIZIALE
    # Valutiamo la funzione ai bordi del dominio.
    function_value_start = objective_function(domain_start)
    function_value_end = objective_function(domain_end)
    
    # Teniamo traccia di tutti i punti valutati per poter poi
    # far capire graficamente all'utente quali zone abbiamo esplorato.
    evaluated_points = [(domain_start, function_value_start), (domain_end, function_value_end)]
    
    # Inizializziamo il "Miglior Minimo Corrente" (Branch and Bound)
    # Serve per scartare in futuro esplorazioni matematicamente inutili.
    best_minimum_value = min(function_value_start, function_value_end)
    best_minimum_x = domain_start if function_value_start < function_value_end else domain_end
    
    # Adattamento della tolleranza all'ampiezza del dominio per coerenza spaziale
    effective_tolerance = tolerance * (domain_end - domain_start)
    
    # -- Funzioni di supporto matematico (Closures) --
    
    # 1. Calcolo del limite inferiore teorico (Caratteristica R)
    # Questa formula calcola il valore minimo possibile che la funzione f(x) può raggiungere
    # nell'intervallo [left_x, right_x]. Si basa sull'ipotesi che la funzione scenda con
    # la massima pendenza possibile definita dalla costante di Lipschitz L a partire da entrambi gli estremi.
    # Formula matematica: R = (f(a) + f(b))/2 - L*(b - a)/2
    calculate_lower_bound = lambda left_x, right_x, left_f, right_f: 0.5 * (left_f + right_f) - 0.5 * lipschitz_constant * (right_x - left_x)
    
    # 2. Calcolo del punto di intersezione delle rette (x_hat)
    # Calcola l'ascissa del punto in cui le due rette con pendenza +L e -L si incontrano.
    # Questo punto rappresenta la "valle" del dente di sega (M-conica) ed è il punto in cui
    # andremo a valutare fisicamente la nostra funzione obiettivo nella fase di Exploration.
    # Formula matematica: x_hat = (a + b)/2 - (f(b) - f(a))/(2*L)
    calculate_intersection_x = lambda left_x, right_x, left_f, right_f: 0.5 * (left_x + right_x) - (right_f - left_f) / (2 * lipschitz_constant)

    # 2. STRUTTURA DATI NAIVE: Lista Piatta
    # Come fatto notare, nella versione Naive non usiamo l'Albero (Heap)
    # ma una semplice lista, e ad ogni iterazione faremo un ciclo FOR per trovare il minimo (O(N)).
    tie_breaker = itertools.count() 
    initial_lower_bound = calculate_lower_bound(domain_start, domain_end, function_value_start, function_value_end)
    
    # Elemento: (Restima (Minorante R), id_univoco, left_x, right_x, f(left), f(right))
    intervals_list = [(initial_lower_bound, next(tie_breaker), domain_start, domain_end, function_value_start, function_value_end)]
    
    actual_iterations = 0
    
    # 3. CICLO ITERATIVO DELL'ALGORITMO
    for _ in range(max_iterations):
        if not intervals_list:
            break  
            
        # -- PASSO 1: ESTRAZIONE --
        # Cerchiamo l'intervallo con il potenziale minimo globale peggiore.
        # Creiamo una lista delle caratteristiche R per trovare il minimo e il suo indice.
        # estraiamo il primo elemento della lista ovvero il lower bound
        lista_R = [intervallo[0] for intervallo in intervals_list]
        min_R = min(lista_R)
        best_index = lista_R.index(min_R)
                
        # Estraiamo e rimuoviamo l'elemento dalla lista
        current_lower_bound, _, current_left_x, current_right_x, current_left_f, current_right_f = intervals_list.pop(best_index)
        
        # -- CRITERIO DI ARRESTO GLOBALE (PIYAVSKII-SHUBERT) --
        # Verifichiamo se il peggior "lower bound" possibile (current_lower_bound) è ormai vicinissimo
        # al miglior valore reale che abbiamo già trovato (best_minimum_value). Se la differenza
        # è inferiore alla tolleranza, abbiamo la garanzia matematica che non esistono minimi migliori.
        if best_minimum_value - current_lower_bound <= effective_tolerance:
            break
            
        # -- CRITERIO DI ARRESTO SPAZIALE --
        # Termina se l'ampiezza dell'intervallo che stiamo per esplorare è scesa sotto la soglia.
        if (current_right_x - current_left_x) <= effective_tolerance:
            break
            
        # -- PASSO 2: CALCOLO DEL NUOVO PUNTO (x_hat) --
        # Calcoliamo l'ascissa del vertice inferiore del "dente di sega" in questo intervallo.
        intersection_x = calculate_intersection_x(current_left_x, current_right_x, current_left_f, current_right_f)
        
        # Protezione numerica: se a causa dell'approssimazione dei float ci sovrapponiamo agli estremi, saltiamo.
        if intersection_x <= current_left_x or intersection_x >= current_right_x:
            continue
            
        # -- PASSO 3: VALUTAZIONE DELLA FUNZIONE (Black Box) --
        # Interroghiamo la funzione obiettivo nel punto x_hat per scoprire il suo VERO valore.
        intersection_f = objective_function(intersection_x)
        evaluated_points.append((intersection_x, intersection_f))
        
        # Se il nuovo punto valutato è più basso del nostro record attuale, aggiorniamo l'ottimo globale.
        if intersection_f < best_minimum_value:
            best_minimum_value = intersection_f
            best_minimum_x = intersection_x
            
        # -- PASSO 4: SUDDIVISIONE E INSERIMENTO --
        # Il punto valutato spezza l'intervallo [left, right] in due sottometa: [left, x_hat] e [x_hat, right].
        # Calcoliamo subito la nuova Caratteristica R per i due nuovi sotto-intervalli.
        lower_bound_left = calculate_lower_bound(current_left_x, intersection_x, current_left_f, intersection_f)
        lower_bound_right = calculate_lower_bound(intersection_x, current_right_x, intersection_f, current_right_f)
        
        # Strutturiamo i due nuovi intervalli calcolati come tuple contenenti tutti i dati utili
        nuovi_intervalli = [
            (lower_bound_left, next(tie_breaker), current_left_x, intersection_x, current_left_f, intersection_f),
            (lower_bound_right, next(tie_breaker), intersection_x, current_right_x, intersection_f, current_right_f)
        ]
        
        # Inseriamo i nuovi intervalli in cima alla lista per valutarli nelle prossime iterazioni.
        intervals_list = nuovi_intervalli + intervals_list
        
        actual_iterations += 1

    return best_minimum_x, best_minimum_value, actual_iterations, evaluated_points

# Difetti:
# - Usa una semplice lista invece del min-heap
# - Manca il pruning di intervalli inutili
