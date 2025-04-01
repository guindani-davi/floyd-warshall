import numpy as np

INF = float('inf')

def ler_grafo(arquivo):
    """Lê um grafo a partir de um arquivo e retorna a matriz de adjacência."""
    with open(arquivo, 'r') as f:
        linhas = f.readlines()

    matriz = []
    for linha in linhas:
        valores = linha.split()
        linha_convertida = [INF if v == "INF" else int(v) for v in valores]
        matriz.append(linha_convertida)

    return np.array(matriz)

def floyd_warshall(grafo):
    """Aplica Floyd-Warshall e retorna a matriz de distâncias e a matriz de predecessores."""
    V = len(grafo)
    dist = grafo.copy()  # Criamos uma cópia para não modificar a matriz original
    
    # Inicializa a matriz de caminhos (next)
    next_vertex = [[j if grafo[i][j] != INF and i != j else None for j in range(V)] for i in range(V)]

    # Algoritmo de Floyd-Warshall
    for k in range(V):  # Vértice intermediário
        for i in range(V):  # Vértice de origem
            for j in range(V):  # Vértice de destino
                if dist[i][k] != INF and dist[k][j] != INF:
                    new_distance = dist[i][k] + dist[k][j]
                    if new_distance < dist[i][j]:  # Se encontramos um caminho mais curto
                        dist[i][j] = new_distance
                        next_vertex[i][j] = next_vertex[i][k]  # Atualiza o próximo nó no caminho
    
    return dist, next_vertex

def reconstruir_caminho(origem, destino, next_vertex):
    """Reconstrói o caminho mínimo entre dois vértices."""
    if next_vertex[origem][destino] is None:
        return []  # Sem caminho
    caminho = [origem]
    while origem != destino:
        origem = next_vertex[origem][destino]
        caminho.append(origem)
    return caminho

def imprimir_matriz(matriz):
    """Exibe a matriz de distâncias de forma legível."""
    for linha in matriz:
        print(" ".join(f"{v:4}" if v != INF else "INF" for v in linha))

if __name__ == "__main__":
    arquivo_grafo = "grafos/grafo_negativos.txt"
    grafo = ler_grafo(arquivo_grafo)

    print("Matriz de adjacência inicial:")
    imprimir_matriz(grafo)

    distancias, next_vertex = floyd_warshall(grafo)

    print("\nMenores distâncias entre todos os pares:")
    imprimir_matriz(distancias)

    print("\nCaminhos mínimos entre os vértices:")
    V = len(grafo)
    for i in range(V):
        for j in range(V):
            if i != j:
                caminho = reconstruir_caminho(i, j, next_vertex)
                if caminho:
                    print(f"Menor caminho de {i} para {j}: {' -> '.join(map(str, caminho))}")
                else:
                    print(f"Não há caminho de {i} para {j}.")
