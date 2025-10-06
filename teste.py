import requests
import time # Usaremos para pequenas pausas e evitar sobrecarregar a API

# Desativar avisos de segurança (opcional, para uma saída mais limpa)
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def obter_resultados_megasena():
    """
    Busca os resultados de todos os sorteios da Mega-Sena, consultando um a um.
    Este método é mais lento, mas se adapta à nova API da Caixa.
    """
    base_url = "https://servicebus2.caixa.gov.br/portaldeloterias/api/megasena"
    
    print("Buscando dados do último sorteio para iniciar...")
    
    try:
        # 1. Obter o número do último concurso
        response_ultimo = requests.get(base_url, verify=False, timeout=10)
        if response_ultimo.status_code != 200:
            print(f"Não foi possível obter o número do último concurso. Status: {response_ultimo.status_code}")
            return []
            
        dados_ultimo_concurso = response_ultimo.json()
        ultimo_concurso = dados_ultimo_concurso.get('numero')

        if not ultimo_concurso:
            print("Não foi possível determinar o número do último concurso na resposta da API.")
            return []
            
        print(f"Último concurso encontrado: {ultimo_concurso}. Buscando todos os resultados...")
        
        # 2. Iterar do primeiro ao último concurso
        todos_os_resultados = []
        for i in range(1, ultimo_concurso + 1):
            # Imprime o progresso na mesma linha
            print(f"Buscando concurso {i}/{ultimo_concurso}...", end='\r')
            
            url_concurso = f"{base_url}/{i}"
            
            try:
                response = requests.get(url_concurso, verify=False, timeout=5)
                
                if response.status_code == 200:
                    sorteio = response.json()
                    # Verifica se o sorteio tem as dezenas (alguns antigos podem falhar)
                    if 'listaDezenas' in sorteio:
                        dezenas_str = sorteio['listaDezenas']
                        dezenas_int = sorted([int(dezena) for dezena in dezenas_str])
                        
                        todos_os_resultados.append({
                            'concurso': sorteio['numero'],
                            'numeros': dezenas_int
                        })
                # Pequena pausa para não sobrecarregar o servidor da Caixa
                time.sleep(0.05) 
                        
            except requests.exceptions.RequestException:
                # Se um concurso falhar, apenas o ignora e continua
                continue
        
        print(f"\nBusca finalizada! {len(todos_os_resultados)} sorteios encontrados.")
        return todos_os_resultados

    except requests.exceptions.RequestException as e:
        print(f"\nOcorreu um erro de conexão: {e}")
        return []
    except KeyError as e:
        print(f"\nErro ao processar os dados. A estrutura do JSON pode ter mudado. Chave não encontrada: {e}")
        return []


def counting_sort_por_coluna(dados, coluna_idx):
    """
    Função auxiliar do Radix Sort. Ordena os dados com base em uma "coluna"
    específica das dezenas (de 0 a 5) usando o Counting Sort.
    """
    tamanho = len(dados)
    max_valor = 60
    
    saida = [None] * tamanho
    contagem = [0] * (max_valor + 1)

    for i in range(tamanho):
        numero_na_coluna = dados[i]['numeros'][coluna_idx]
        contagem[numero_na_coluna] += 1

    for i in range(1, max_valor + 1):
        contagem[i] += contagem[i-1]

    i = tamanho - 1
    while i >= 0:
        sorteio_atual = dados[i]
        numero_na_coluna = sorteio_atual['numeros'][coluna_idx]
        
        posicao_final = contagem[numero_na_coluna] - 1
        saida[posicao_final] = sorteio_atual
        contagem[numero_na_coluna] -= 1
        i -= 1

    return saida

def radix_sort_megasena(dados):
    """
    Ordena uma lista de resultados da Mega-Sena usando o algoritmo Radix Sort.
    """
    print("Iniciando ordenação com Radix Sort...")
    
    for coluna_idx in range(5, -1, -1):
        # A mensagem de progresso foi removida daqui para não poluir a tela
        dados = counting_sort_por_coluna(dados, coluna_idx)
        
    print("Ordenação finalizada!")
    return dados

def apresentar_resultados(dados_ordenados):
    """
    Exibe os resultados ordenados no formato solicitado.
    """
    print("\n--- Resultados da Mega-Sena Ordenados ---\n")
    for sorteio in dados_ordenados:
        numeros_formatados = [f"{num:02d}" for num in sorteio['numeros']]
        string_numeros = ", ".join(numeros_formatados)
        print(f"[{string_numeros}] - {sorteio['concurso']}")

# --- Bloco Principal de Execução ---
if __name__ == "__main__":
    todos_os_sorteios = obter_resultados_megasena()
    
    if todos_os_sorteios:
        sorteios_ordenados = radix_sort_megasena(todos_os_sorteios)
        apresentar_resultados(sorteios_ordenados)