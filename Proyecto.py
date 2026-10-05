"""
Componentes conexas de un grafo no dirigido (matriz de adyacencia + BFS)
Requisitos: pip install networkx matplotlib
"""

import random
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt


# ------------------------- 1. ENTRADA DE DATOS -------------------------

def pedir_n():
    """Pide el número de vértices hasta que esté entre 5 y 15."""
    while True:
        try:
            n = int(input("Número de vértices (5 a 15): "))
            if 5 <= n <= 15:
                return n
            print("Error: n debe estar entre 5 y 15.")
        except ValueError:
            print("Error: ingrese un número entero.")


def matriz_aleatoria(n):
    """Matriz booleana simétrica y con diagonal en False (aristas al 30 %)."""
    matriz = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            matriz[i][j] = matriz[j][i] = random.random() < 0.3
    return matriz


def es_valida(matriz):
    """Un grafo no dirigido necesita matriz simétrica y sin lazos."""
    n = len(matriz)
    for i in range(n):
        if matriz[i][i]:
            return False
        for j in range(n):
            if matriz[i][j] != matriz[j][i]:
                return False
    return True


def matriz_manual(n):
    """El usuario escribe la matriz fila por fila (ejemplo de fila: 0 1 1 0 0)."""
    while True:
        print(f"\nEscriba cada fila con {n} valores (0/1) separados por espacios.")
        matriz = []
        for i in range(n):
            while True:
                valores = input(f"Fila {i}: ").split()
                if len(valores) == n and all(v in ("0", "1") for v in valores):
                    matriz.append([v == "1" for v in valores])
                    break
                print(f"Error: ingrese exactamente {n} valores, solo 0 o 1.")
        if es_valida(matriz):
            return matriz
        print("Error: la matriz debe ser simétrica y tener la diagonal en 0. Intente de nuevo.")


# ------------------------- 2. ALGORITMO BFS -------------------------

def componentes_conexas(matriz):
    """Agrupa los vértices en componentes conexas con BFS, mostrando cada paso."""
    n = len(matriz)
    visitado = [False] * n
    componentes = []

    for inicio in range(n):
        if visitado[inicio]:
            continue                          # ya pertenece a otra componente

        print(f"\n--- Componente {len(componentes) + 1}: se inicia en el vértice {inicio} ---")
        componente = []
        cola = deque([inicio])
        visitado[inicio] = True

        while cola:
            actual = cola.popleft()           # sacar el primero de la cola
            componente.append(actual)
            nuevos = [v for v in range(n) if matriz[actual][v] and not visitado[v]]
            for v in nuevos:
                visitado[v] = True
                cola.append(v)
            print(f"Visito {actual} | vecinos nuevos: {nuevos} | cola: {list(cola)} "
                  f"| componente: {componente}")

        componentes.append(sorted(componente))

    return componentes


# ------------------------- 3. GRÁFICOS -------------------------

def construir_grafo(matriz):
    n = len(matriz)
    G = nx.Graph()
    G.add_nodes_from(range(n))
    G.add_edges_from((i, j) for i in range(n) for j in range(i + 1, n) if matriz[i][j])
    return G


def colores_por_vertice(componentes):
    paleta = plt.cm.tab10.colors
    return {v: paleta[k % len(paleta)] for k, comp in enumerate(componentes) for v in comp}


def dibujar_grafo(G, pos, titulo, color=None):
    """Dibuja el grafo; si hay colores, pinta cada componente de un color."""
    color_nodos = [color[v] for v in G.nodes] if color else "lightblue"
    nx.draw(G, pos, with_labels=True, node_color=color_nodos, node_size=650)
    plt.title(titulo)


def dibujar_componentes(G, pos, componentes, color):
    """Una figura con una gráfica por cada componente."""
    k = len(componentes)
    columnas = min(4, k)
    filas = (k + columnas - 1) // columnas
    plt.figure(figsize=(4 * columnas, 3.5 * filas))
    for idx, comp in enumerate(componentes, start=1):
        plt.subplot(filas, columnas, idx)
        dibujar_grafo(G.subgraph(comp), pos, f"Componente {idx}: {comp}", color)
    plt.tight_layout()
    plt.show()


# ------------------------- 4. PROGRAMA PRINCIPAL -------------------------

def main():
    n = pedir_n()

    opcion = ""
    while opcion not in ("1", "2"):
        opcion = input("1 = matriz aleatoria, 2 = ingreso manual: ").strip()
    matriz = matriz_aleatoria(n) if opcion == "1" else matriz_manual(n)

    print("\nMatriz de adyacencia:")
    for fila in matriz:
        print([int(x) for x in fila])

    # Grafo asociado a la matriz
    G = construir_grafo(matriz)
    pos = nx.spring_layout(G, seed=42)       # misma posición en todos los gráficos
    dibujar_grafo(G, pos, "Grafo asociado a la matriz")
    plt.show()

    # Proceso paso a paso
    componentes = componentes_conexas(matriz)

    # Resultado final
    print("\n========== RESULTADO ==========")
    for k, comp in enumerate(componentes, start=1):
        print(f"Componente {k}: {comp}")
    print(f"Número total de componentes conexas: {len(componentes)}")

    # Gráficas
    color = colores_por_vertice(componentes)
    dibujar_grafo(G, pos, f"Componentes conexas: {len(componentes)}", color)
    plt.show()
    dibujar_componentes(G, pos, componentes, color)


if __name__ == "__main__":
    main()
