import os
from typing import List, Dict, Any

MAX_DEZENA_VALOR = 60

def ordenar_posicao(dados: List[Dict[str, Any]], posicao: int) -> List[Dict[str, Any]]:
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

def ordenar_radix(dados: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    dados_a_ordenar = list(dados)
    NUMERO_DE_DEZENAS = 6
    for i in range(NUMERO_DE_DEZENAS - 1, -1, -1):
        dados_a_ordenar = ordenar_posicao(dados_a_ordenar, posicao=i)
    return dados_a_ordenar

def carregar_dados_de_arquivo(nome_arquivo: str) -> List[Dict[str, Any]]:
    dados_carregados = []
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            for numero_linha, linha in enumerate(arquivo, 1):
                linha_limpa = linha.strip()
                if not linha_limpa:
                    continue

                try:
                    partes = linha_limpa.split(' - ')
                    
                    if len(partes) < 3:
                        print(f"Aviso: Linha {numero_linha} ignorada. Formato inesperado.")
                        continue

                    concurso_texto = partes[0].strip()
                    concurso = int(concurso_texto)
                    
                    dezenas_texto = partes[-1].strip()
                    dezenas = [int(d) for d in dezenas_texto.split()]

                    if len(dezenas) == 6:
                        dados_carregados.append({'concurso': concurso, 'dezenas': dezenas})
                    else:
                        print(f"Aviso: Linha {numero_linha} ignorada. Não contém 6 dezenas.")

                except (ValueError, IndexError) as e:
                    print(f"Aviso: Erro ao processar a linha {numero_linha}: '{linha_limpa}'. Erro: {e}")
                    continue

    except FileNotFoundError:
        print(f"Erro: O arquivo '{nome_arquivo}' não foi encontrado.")
        
    return dados_carregados

def imprimir_resultados(resultados: List[Dict[str, Any]]):
    print("\nResultados da Mega-Sena ordenados utilizando radix sort:\n")
    for sorteio in resultados:
        dezenas_formatadas = [f"{d:02d}" for d in sorteio['dezenas']]
        dezenas_str = " ".join(dezenas_formatadas)
        print(f"{dezenas_str} - {sorteio['concurso']}")

def main():
    diretorio_do_script = os.path.dirname(os.path.abspath(__file__))
    caminho_do_arquivo = os.path.join(diretorio_do_script, 'resultados.txt')
    
    dados_megasena = carregar_dados_de_arquivo(caminho_do_arquivo)

    if dados_megasena:
        resultados_ordenados = ordenar_radix(dados_megasena)
        imprimir_resultados(resultados_ordenados)
    else:
        print("Nenhum dado válido foi carregado do arquivo. Encerrando o programa.")

if __name__ == "__main__":
    main()