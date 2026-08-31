"""
Componentes Conexas de un Grafo No Dirigido
============================================
Programa que determina las componentes conexas de un grafo no dirigido
representado mediante una matriz de adyacencia booleana.

Requisitos (instalar antes de ejecutar):
    pip install networkx matplotlib

Ejecución:
    python componentes_conexas.py
"""

import random
import networkx as nx
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# 1. ENTRADA DE DATOS
# ---------------------------------------------------------------------------

def pedir_numero_vertices():
    """Solicita al usuario el número de vértices n (5 <= n <= 15)."""
    while True:
        try:
            n = int(input("Ingrese el número de vértices (5 <= n <= 15): "))
            if 5 <= n <= 15:
                return n
            print("Error: el número de vértices debe estar entre 5 y 15.")
        except ValueError:
            print("Error: debe ingresar un número entero.")


def generar_matriz_aleatoria(n, densidad=0.30):
    """
    Genera aleatoriamente una matriz de adyacencia booleana simétrica
    para un grafo no dirigido, sin lazos (diagonal en False).
    """
    matriz = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            existe_arista = random.random() < densidad
            matriz[i][j] = existe_arista
            matriz[j][i] = existe_arista
    return matriz


def ingresar_matriz_manual(n):
    """
    Permite al usuario ingresar manualmente la matriz de adyacencia.
    Solo se pregunta una vez por cada par de vértices distintos (i < j),
    ya que el grafo no es dirigido y se asume sin lazos.
    """
    matriz = [[False] * n for _ in range(n)]
    print("\nIngrese la existencia de cada arista (1 = existe, 0 = no existe).\n")
    for i in range(n):
        for j in range(i + 1, n):
            while True:
                valor = input(f"¿Existe arista entre el vértice {i} y el vértice {j}? (1/0): ").strip()
                if valor in ("0", "1"):
                    existe = valor == "1"
                    matriz[i][j] = existe
                    matriz[j][i] = existe
                    break
                print("Entrada inválida. Ingrese 1 o 0.")
    return matriz


def mostrar_matriz(matriz, n):
    """Imprime la matriz de adyacencia en forma de tabla."""
    print("\nMatriz de adyacencia:")
    print("    " + " ".join(f"{j:2}" for j in range(n)))
    for i in range(n):
        fila = " ".join(f"{1 if matriz[i][j] else 0:2}" for j in range(n))
        print(f"{i:2}: {fila}")


# ---------------------------------------------------------------------------
# 2. CONSTRUCCIÓN Y VISUALIZACIÓN DEL GRAFO
# ---------------------------------------------------------------------------

def construir_grafo_networkx(matriz, n):
    """Construye un objeto Graph de networkx a partir de la matriz booleana."""
    G = nx.Graph()
    G.add_nodes_from(range(n))
    for i in range(n):
        for j in range(i + 1, n):
            if matriz[i][j]:
                G.add_edge(i, j)
    return G


def mostrar_grafo(G, titulo="Grafo", colores_por_componente=None):
    """
    Dibuja el grafo usando matplotlib. Si se provee 'colores_por_componente'
    (lista de listas de vértices), cada componente se pinta con un color distinto.
    """
    plt.figure(figsize=(6, 5))
    pos = nx.spring_layout(G, seed=42)

    if colores_por_componente:
        paleta = plt.cm.tab10.colors
        color_map = []
        for nodo in G.nodes():
            for idx, comp in enumerate(colores_por_componente):
                if nodo in comp:
                    color_map.append(paleta[idx % len(paleta)])
                    break
        nx.draw(G, pos, with_labels=True, node_color=color_map,
                node_size=650, font_weight='bold', edge_color='gray')
    else:
        nx.draw(G, pos, with_labels=True, node_color='lightblue',
                node_size=650, font_weight='bold', edge_color='gray')

    plt.title(titulo)
    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------------------------
# 3. BÚSQUEDA DE COMPONENTES CONEXAS (BFS paso a paso)
# ---------------------------------------------------------------------------

def encontrar_componentes_conexas(matriz, n):
    """
    Encuentra las componentes conexas usando BFS, imprimiendo paso a paso
    el proceso de agrupación de vértices.
    Retorna una lista de listas; cada sublista contiene los vértices de
    una componente.
    """
    visitados = [False] * n
    componentes = []

    print("\n" + "=" * 60)
    print("PROCESO DE BÚSQUEDA DE COMPONENTES CONEXAS (BFS)")
    print("=" * 60)

    for inicio in range(n):
        if visitados[inicio]:
            continue

        componente = []
        cola = [inicio]
        visitados[inicio] = True
        num_componente = len(componentes) + 1

        print(f"\n--- Iniciando búsqueda de la Componente {num_componente} ---")
        print(f"Vértice semilla: {inicio}")

        while cola:
            actual = cola.pop(0)
            componente.append(actual)
            print(f"  Visitando vértice {actual}. Componente parcial: {componente}")

            vecinos = [v for v in range(n) if matriz[actual][v] and not visitados[v]]
            if vecinos:
                print(f"    Vecinos no visitados de {actual}: {vecinos}")
            for vecino in vecinos:
                visitados[vecino] = True
                cola.append(vecino)

        componente.sort()
        print(f"--- Componente {num_componente} completa: {componente} ---")
        componentes.append(componente)

    return componentes


# ---------------------------------------------------------------------------
# 4. PROGRAMA PRINCIPAL
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("  COMPONENTES CONEXAS DE UN GRAFO NO DIRIGIDO")
    print("=" * 60)

    n = pedir_numero_vertices()

    print("\n¿Cómo desea construir la matriz de adyacencia?")
    print("1. Generación automática (aleatoria)")
    print("2. Ingreso manual")

    while True:
        opcion = input("Seleccione una opción (1/2): ").strip()
        if opcion in ("1", "2"):
            break
        print("Opción inválida. Ingrese 1 o 2.")

    matriz = generar_matriz_aleatoria(n) if opcion == "1" else ingresar_matriz_manual(n)

    mostrar_matriz(matriz, n)

    G = construir_grafo_networkx(matriz, n)
    print("\nMostrando el grafo original...")
    mostrar_grafo(G, titulo="Grafo original")

    componentes = encontrar_componentes_conexas(matriz, n)

    print("\n" + "=" * 60)
    print("RESULTADO FINAL")
    print("=" * 60)
    for idx, comp in enumerate(componentes, start=1):
        print(f"Componente {idx}: {comp}  (tamaño: {len(comp)})")
    print(f"\nNúmero total de componentes conexas: {len(componentes)}")

    print("\nMostrando el grafo original con las componentes coloreadas...")
    mostrar_grafo(G, titulo="Componentes conexas (coloreadas)",
                  colores_por_componente=componentes)

    print("Mostrando cada componente por separado...")
    for idx, comp in enumerate(componentes, start=1):
        subgrafo = G.subgraph(comp)
        mostrar_grafo(subgrafo, titulo=f"Componente {idx}: {comp}")


if __name__ == "__main__":
    main()