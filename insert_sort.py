class No:
    def __init__(self, dado):
        self.dado = dado
        self.proximo = None

class ListaLigada:
    def __init__(self):
        self.head = None

    def inserir_no_inicio(self, dado):
        novo_no = No(dado)
        novo_no.proximo = self.head
        self.head = novo_no

    def imprimir_lista(self):
        temp = self.head
        elementos = []
        while temp:
            elementos.append(str(temp.dado))
            temp = temp.proximo
        print(" -> ".join(elementos) if elementos else "Lista Vazia")

def insertion_sort_lista_ligada(lista_ligada):
    print("Iniciando o processo de ordenação...\n")
    
    lista_ordenada = ListaLigada()
    no_atual = lista_ligada.head
    
    while no_atual:
        proximo_no = no_atual.proximo
        inserir_ordenado(lista_ordenada, no_atual)
        no_atual = proximo_no
        
        print(f"Inserindo o elemento {no_atual.dado if no_atual else '(último)'}. Estado da lista ordenada:")
        lista_ordenada.imprimir_lista()

    return lista_ordenada

def inserir_ordenado(lista_ordenada, novo_no):
    if lista_ordenada.head is None or lista_ordenada.head.dado >= novo_no.dado:
        novo_no.proximo = lista_ordenada.head
        lista_ordenada.head = novo_no
    else:
        ponteiro = lista_ordenada.head
        while ponteiro.proximo is not None and ponteiro.proximo.dado < novo_no.dado:
            ponteiro = ponteiro.proximo
        
        novo_no.proximo = ponteiro.proximo
        ponteiro.proximo = novo_no

if __name__ == "__main__":
    
    minha_lista = ListaLigada()
    
    dados = [1, 4, 9, 3, 5, 2, 8]
    for dado in dados:
        minha_lista.inserir_no_inicio(dado)
    
    print("ESTRUTURA DE DADOS: LISTA LIGADA\n")
    print("Lista original, antes da ordenação:")
    minha_lista.imprimir_lista()
    print("\n" + "="*40 + "\n")
    
    lista_final_ordenada = insertion_sort_lista_ligada(minha_lista)
    
    print("\n" + "="*40 + "\n")
    print("PROCESSO FINALIZADO!\n")
    print("Lista final, após a ordenação:")
    lista_final_ordenada.imprimir_lista()