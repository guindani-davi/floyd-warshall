import numpy as np

INF = float('inf')

def ler_grafo(arquivo): 
    """O(V²)"""
    """Lê um grafo a partir de um arquivo e retorna a matriz de adjacência."""
    with open(arquivo, 'r') as a:
        linhas = a.readlines()

    matriz = []
    for linha in linhas:
        valores = linha.split()
        linha_convertida = [INF if v == "INF" else int(v) for v in valores]
        matriz.append(linha_convertida)

    return np.array(matriz)

def floyd_warshall(grafo):
    """O(V³)"""
    """Aplica Floyd-Warshall e retorna as matrizes de distâncias e de predecessores."""
    V = len(grafo)
    distancias = grafo.copy()  # Para não modificar o original, se eu só faço dist = grafo acontece uma passagem por referência
    
    # Inicialização da matriz de predecessores
    pred = [[j if grafo[i][j] != INF and i != j else None for j in range(V)] for i in range(V)]

    for k in range(V):
        for i in range(V):
            for j in range(V):
                if distancias[i][k] != INF and distancias[k][j] != INF:
                    nova_distancia = distancias[i][k] + distancias[k][j]
                    if nova_distancia < distancias[i][j]:
                        distancias[i][j] = nova_distancia
                        pred[i][j] = pred[i][k]
    
    return distancias, pred

def reconstruir_caminho(origem, destino, prox_vertice):
    """O(V)"""
    """Reconstrói o caminho mínimo entre dois vértices."""
    if prox_vertice[origem][destino] is None:
        return []
    caminho = [origem]
    while origem != destino:
        origem = prox_vertice[origem][destino]
        caminho.append(origem)
    return caminho

def imprimir_matriz(matriz):
    """O(V²)"""
    for linha in matriz:
        print(" ".join(f"{v:4}" if v != INF else "INF" for v in linha))

if __name__ == "__main__":
    arquivo_grafo = "grafos/grafo_medio.txt"
    grafo = ler_grafo(arquivo_grafo)

    print("Matriz de adjacência inicial:")
    imprimir_matriz(grafo)

    distancias, predecessores = floyd_warshall(grafo)

    print("\nMenores distâncias entre todos os pares:")
    imprimir_matriz(distancias)

    print("\nCaminhos mínimos entre os vértices:")
    V = len(grafo)
    """O(V³)"""
    for i in range(V):
        for j in range(V):
            if i != j:
                caminho = reconstruir_caminho(i, j, predecessores)
                if caminho:
                    print(f"Menor caminho de {i} para {j}: {' -> '.join(map(str, caminho))}")
                else:
                    print(f"Não há caminho de {i} para {j}.")
