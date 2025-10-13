MAX_DEZENA_VALOR = 60

def ordenar_posicao(dados, posicao):
    n = len(dados)
    dados_ordenados = [None] * n
    count = [0] * (MAX_DEZENA_VALOR + 1)

    for i in range(n):
        dezena = dados[i]['dezenas'][posicao]
        count[dezena] += 1

    for i in range(1, MAX_DEZENA_VALOR + 1):
        count[i] += count[i - 1]

    i = n - 1
    while i >= 0:
        sorteio = dados[i]
        dezena = sorteio['dezenas'][posicao]
        posicao_final = count[dezena] - 1
        dados_ordenados[posicao_final] = sorteio
        count[dezena] -= 1
        i -= 1
        
    return dados_ordenados

def ordenar_radix(dados):
    dados_a_ordenar = list(dados)
    for i in range(5, -1, -1):
        dados_a_ordenar = ordenar_posicao(dados_a_ordenar, posicao=i)
    return dados_a_ordenar

dados_megasena = [
    {'concurso': 2683, 'dezenas': [1, 3, 23, 27, 47, 57]},
    {'concurso': 2667, 'dezenas': [1, 4, 8, 21, 46, 51]},
    {'concurso': 2700, 'dezenas': [1, 11, 19, 20, 28, 48]},
    {'concurso': 2675, 'dezenas': [1, 26, 31, 34, 42, 45]},
    {'concurso': 2668, 'dezenas': [1, 27, 30, 41, 46, 57]},
    {'concurso': 2690, 'dezenas': [4, 5, 17, 20, 48, 52]},
    {'concurso': 2691, 'dezenas': [4, 6, 17, 22, 27, 53]},
    {'concurso': 2692, 'dezenas': [4, 6, 30, 35, 48, 56]},
    {'concurso': 2680, 'dezenas': [3, 4, 24, 30, 44, 55]},
]

#sor, não achei nenhuma forma de pegar os numeros da megasena na internet, então coloquei alguns resultados aleatórios
resultados_ordenados = ordenar_radix(dados_megasena)

print("Resultados da Mega-Sena Ordenados por Dezenas:\n")

for sorteio in resultados_ordenados:
    dezenas_formatadas = [f"{d:02d}" for d in sorteio['dezenas']]
    dezenas_str = str(dezenas_formatadas).replace("'", "")
    print(f"{dezenas_str} - {sorteio['concurso']}")