class Node:
    def __init__(self, numero):
        self.valor = numero
        self.next = None

class Lista:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_valor(self, valor):
        novo_no = Node(valor)

        if self.head is None:
            self.head = novo_no
            self.tail = novo_no
        else:
            self.tail.next = novo_no
            self.tail = novo_no


    def imprime_lista(self):
        if self.head is None:
            print("A lista está vazia.")
        else:
            no_atual = self.head
            while no_atual is not None:
                print(f"Valor: {no_atual.valor}")
                no_atual = no_atual.next


    def ordena_select(self):
 
        
        no_atual = self.head
        
        while no_atual:
            no_minimo = no_atual
            verificador = no_atual.next
            while verificador:
                if verificador.valor < no_minimo.valor:
                    no_minimo = verificador
                verificador = verificador.next 
    
        #atual.valor, proximo.valor = proximo.valor, atual.valor
            temp_data = no_atual.valor
            no_atual.valor = no_minimo.valor
            no_minimo.valor = temp_data




            no_atual = no_atual.next






lista_desordenada = [13, 95, 119, 184, 96, 102, 21, 48, 137, 57, 99, 5, 45, 170, 154, 146]
lista = Lista()
for numero in lista_desordenada:
    lista.add_valor(numero)

print("Lista Desordenada.")
lista.imprime_lista()
lista.ordena_select()
print("Lista Ordenada.")
lista.imprime_lista()