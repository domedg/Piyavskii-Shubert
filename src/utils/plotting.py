import numpy as np
import plotly.graph_objects as go
from typing import Callable, List, Tuple

def calculate_minorante(
    points: List[Tuple[float, float]], 
    L: float
) -> Tuple[List[float], List[float]]:
    """
    Costruisce la forma della funzione minorante (lower bound a dente di sega)
    a partire dai punti campionati, sfruttando la costante di Lipschitz L.
    """
    # Ordiniamo i punti per x crescente
    sorted_points = sorted(points, key=lambda p: p[0])
    
    xs_minorante = []
    ys_minorante = []
    
    # Aggiungiamo il primo punto e poi interpoliamo tutti gli apici dei V
    for i in range(len(sorted_points) - 1):
        x1, y1 = sorted_points[i]
        x2, y2 = sorted_points[i+1]
        
        # Punti interpolati dal Teorema di Piyavskii
        x_hat = 0.5 * (x1 + x2) - (y2 - y1) / (2 * L)
        y_hat = 0.5 * (y1 + y2) - 0.5 * L * (x2 - x1)
        
        # Aggiungiamo i vertici della V capovolta (il cono di Lipschitz)
        if i == 0:
            xs_minorante.append(x1)
            ys_minorante.append(y1)
            
        xs_minorante.extend([x_hat, x2])
        ys_minorante.extend([y_hat, y2])
        
    return xs_minorante, ys_minorante

def create_optimization_plot(
    f: Callable[[float], float],
    a: float,
    b: float,
    L: float,
    best_x: float,
    best_f: float,
    evaluated_points: List[Tuple[float, float]]
) -> go.Figure:
    """
    Genera un grafico Plotly interattivo e ricchissimo di informazioni didattiche.
    """
    # 1. Punti continui per disegnare in modo "smooth" la vera funzione obiettivo
    x_smooth = np.linspace(a, b, 1000)
    # Vettorizziamo f per supportare numpy logic ma gestire le nostre lambda
    vectorized_f = np.vectorize(f)
    y_smooth = vectorized_f(x_smooth)
    
    fig = go.Figure()

    # TRACCIA 1: La Funzione Obbiettivo f(x) [Curva Continua]
    fig.add_trace(go.Scatter(
        x=x_smooth, 
        y=y_smooth, 
        mode='lines', 
        name='Funzione Obiettivo f(x)',
        line=dict(color='deepskyblue', width=2),
        opacity=0.7
    ))

    # TRACCIA 2: Funzione Minorante (Lower Bound a denti di sega)
    xs_min, ys_min = calculate_minorante(evaluated_points, L)
    fig.add_trace(go.Scatter(
        x=xs_min, 
        y=ys_min, 
        mode='lines', 
        name='Minorante Empirica F(x) (Lower Bound)',
        line=dict(color='tomato', width=1.5, dash='dot'),
        fill='tonexty',              # Colora l'area tra vera func e minorante
        fillcolor='rgba(255, 99, 71, 0.1)'
    ))
    
    # TRACCIA 3: I Punti Valutati dall'algoritmo (Scatter)
    eval_x = [p[0] for p in evaluated_points]
    eval_y = [p[1] for p in evaluated_points]
    fig.add_trace(go.Scatter(
        x=eval_x, 
        y=eval_y, 
        mode='markers', 
        name=f"Tentativi dell'algoritmo ({len(evaluated_points)} pti)",
        marker=dict(color='black', size=6, symbol='x')
    ))
    
    # TRACCIA 4: L'Ottimo Globale trovato
    fig.add_trace(go.Scatter(
        x=[best_x], 
        y=[best_f], 
        mode='markers',
        name='Ottimo Globale Calcolato',
        marker=dict(color='gold', size=14, line=dict(color='black', width=2), symbol='star')
    ))

    # Layout esteticamente curato
    fig.update_layout(
        title='Algoritmo di ottimizzazione Globale di Piyavskii-Shubert',
        xaxis_title='Asse X (Spazio di Ricerca)',
        yaxis_title='Asse Y (Funzione f(x))',
        template='plotly_dark',     # L'estetica scura impressiona sempre (Modalità "Hacker")
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=40, r=40, t=60, b=40)
    )
    
    return fig
