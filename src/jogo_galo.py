#Bibliotecas para medir tempo de execução e uso de memória
import time
import tracemalloc

# Cria um tabuleiro vazio 3x3
def criar_tabuleiro():
    return [[" " for _ in range(3)] for _ in range(3)]

# Imprime o tabuleiro com separadores e numeração 1-2-3
def imprimir_tabuleiro(tabuleiro):
    for linha in tabuleiro:
        print(" | ".join(linha))
        print("-" * 9)

# Verifica se o jogador venceu (linhas, colunas ou diagonais)
def verificar_vitoria(tabuleiro, jogador):
    for i in range(3):
        if all([tabuleiro[i][j] == jogador for j in range(3)]) or all([tabuleiro[j][i] == jogador for j in range(3)]):
            return True
    if all([tabuleiro[i][i] == jogador for i in range(3)]) or all([tabuleiro[i][2 - i] == jogador for i in range(3)]):
        return True
    return False

# Verifica se o tabuleiro está completamente cheio
def tabuleiro_cheio(tabuleiro):
    return all([celula != " " for linha in tabuleiro for celula in linha])

# Retorna lista de jogadas disponíveis (posições vazias)
def jogadas_disponiveis(tabuleiro):
    return [(i, j) for i in range(3) for j in range(3) if tabuleiro[i][j] == " "]

# Cria uma cópia do tabuleiro
def copiar_tabuleiro(tabuleiro):
    return [linha[:] for linha in tabuleiro]

# Algoritmo MinMax recursivo para escolher a jogada ótima
# MAX = "X", MIN = "O"
def minmax(tabuleiro, jogador):
    if verificar_vitoria(tabuleiro, "X"):
        return 1, None
    elif verificar_vitoria(tabuleiro, "O"):
        return -1, None
    elif tabuleiro_cheio(tabuleiro):
        return 0, None

    if jogador == "X":
        melhor_valor = float('-inf')
        melhor_jogada = None
        for i, j in jogadas_disponiveis(tabuleiro):
            copia = copiar_tabuleiro(tabuleiro)
            copia[i][j] = "X"
            valor, _ = minmax(copia, "O")
            if valor > melhor_valor:
                melhor_valor = valor
                melhor_jogada = (i, j)
        return melhor_valor, melhor_jogada
    else:
        pior_valor = float('inf')
        pior_jogada = None
        for i, j in jogadas_disponiveis(tabuleiro):
            copia = copiar_tabuleiro(tabuleiro)
            copia[i][j] = "O"
            valor, _ = minmax(copia, "X")
            if valor < pior_valor:
                pior_valor = valor
                pior_jogada = (i, j)
        return pior_valor, pior_jogada

def alphabeta(tabuleiro, jogador, alpha=float('-inf'), beta=float('inf')):
    if verificar_vitoria(tabuleiro, "X"):
        return 1, None
    elif verificar_vitoria(tabuleiro, "O"):
        return -1, None
    elif tabuleiro_cheio(tabuleiro):
        return 0, None

    if jogador == "X":
        melhor_valor = float('-inf')
        melhor_jogada = None
        for i, j in jogadas_disponiveis(tabuleiro):
            copia = copiar_tabuleiro(tabuleiro)
            copia[i][j] = "X"
            valor, _ = alphabeta(copia, "O", alpha, beta)
            if valor > melhor_valor:
                melhor_valor = valor
                melhor_jogada = (i, j)
            alpha = max(alpha, melhor_valor)
            if beta <= alpha:
                break
        return melhor_valor, melhor_jogada
    else:
        pior_valor = float('inf')
        pior_jogada = None
        for i, j in jogadas_disponiveis(tabuleiro):
            copia = copiar_tabuleiro(tabuleiro)
            copia[i][j] = "O"
            valor, _ = alphabeta(copia, "X", alpha, beta)
            if valor < pior_valor:
                pior_valor = valor
                pior_jogada = (i, j)
            beta = min(beta, pior_valor)
            if beta <= alpha:
                break
        return pior_valor, pior_jogada


def jogar_humano_vs_computador(usar_alphabeta):
    tabuleiro = criar_tabuleiro()
    jogador_atual = "X"

    tempo_total = 0
    memoria_total = 0
    while True:
        imprimir_tabuleiro(tabuleiro)
        print(f"Vez do jogador {jogador_atual}")

        if jogador_atual == "O":
            try:
                linha = int(input("Escolhe a linha (1, 2, 3): ")) -1
                coluna = int(input("Escolhe a coluna (1, 2, 3): ")) -1
                if linha not in range(3) or coluna not in range(3):
                    print("Coordenadas inválidas. Tenta novamente.")
                    continue
            except ValueError:
                print("Entrada inválida. Usa apenas números.")
                continue

        else:
            if usar_alphabeta:
                (_, (linha, coluna)), tempo, memoria = medir_performance(alphabeta, tabuleiro, "X")
            else:
                (_, (linha, coluna)), tempo, memoria = medir_performance(minmax, tabuleiro, "X")


            print(f"O computador jogou: {linha}, {coluna}")
            tempo_total += tempo
            memoria_total += memoria


        if tabuleiro[linha][coluna] != " ":
            print("Posição já ocupada. Tenta novamente.")
            continue

        tabuleiro[linha][coluna] = jogador_atual

        if verificar_vitoria(tabuleiro, jogador_atual):
            imprimir_tabuleiro(tabuleiro)
            print(f"Jogador {jogador_atual} venceu!")
            print(f"Tempo total de execução: {tempo_total:.6f} segundos")
            print(f"Memória total usada: {memoria_total:.2f} KB")
            break
        if tabuleiro_cheio(tabuleiro):
            imprimir_tabuleiro(tabuleiro)
            print("Empate!")
            print(f"Tempo total de execução: {tempo_total:.6f} segundos")
            print(f"Memória total usada: {memoria_total:.2f} KB")
            break

        jogador_atual = "O" if jogador_atual == "X" else "X"


def jogar_computador_vs_computador(usar_alphabeta):
    tabuleiro = criar_tabuleiro()
    jogador_atual = "X"

    tempo_total = 0
    memoria_total = 0
    while True:
        imprimir_tabuleiro(tabuleiro)
        print(f"Computador ({jogador_atual}) a jogar...")

        if usar_alphabeta:
            (_, jogada), tempo, memoria = medir_performance(alphabeta, tabuleiro, jogador_atual)
        else:
            (_, jogada), tempo, memoria = medir_performance(minmax, tabuleiro, jogador_atual)


        print(f"Jogada do Computador: {jogada}")
        tempo_total += tempo
        memoria_total += memoria

        if jogada is None:
            print("Erro: o algoritmo não conseguiu encontrar jogada.")
            break

        linha, coluna = jogada
        tabuleiro[linha][coluna] = jogador_atual


        if verificar_vitoria(tabuleiro, jogador_atual):
            imprimir_tabuleiro(tabuleiro)
            print(f"Computador ({jogador_atual}) venceu!")
            print(f"Tempo total de execução: {tempo_total:.6f} segundos")
            print(f"Memória total usada: {memoria_total:.2f} KB")
            break
        if tabuleiro_cheio(tabuleiro):
            imprimir_tabuleiro(tabuleiro)
            print("Empate!")
            print(f"Tempo total de execução: {tempo_total:.6f} segundos")
            print(f"Memória total usada: {memoria_total:.2f} KB")
            break

        jogador_atual = "O" if jogador_atual == "X" else "X"

def medir_performance(funcao, *args):
    tracemalloc.start()
    inicio = time.perf_counter()
    resultado = funcao(*args)
    fim = time.perf_counter()
    _, memoria_pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    tempo_execucao = fim - inicio
    memoria_kb = memoria_pico / 1024

    return resultado, tempo_execucao, memoria_kb
       

# ================================
# INÍCIO DO JOGO
# ================================
def main():
    while True:
        while True:
            modo = input("Modo de jogo: (1) Humano vs PC, (2) PC vs PC: ").strip()
            if modo in ("1", "2"):
                break
            print("Opção inválida. Por favor escolhe 1 ou 2.")

        while True:
            algoritmo = input("Algoritmo: (1) MinMax, (2) Alpha-Beta: ").strip()
            if algoritmo in ("1", "2"):
                break
            print("Opção inválida. Por favor escolhe 1 ou 2.")

        
        usar_alphabeta = algoritmo == "2"

        if modo == "1":
            jogar_humano_vs_computador(usar_alphabeta)
        else:
            jogar_computador_vs_computador(usar_alphabeta)

        again = input("Queres jogar outra vez? (s/n): ").lower()
        if again == 's':
            print("\nNovo jogo!\n")
        else:

            print("Obrigado por jogar! Até à próxima!")
            break

if __name__ == "__main__":
    main()

