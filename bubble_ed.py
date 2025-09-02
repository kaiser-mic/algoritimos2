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

    def ordena_bubble(self):
        if self.head is None or self.head.next is None:
            return
    
        fim = None
    
        while fim != self.head:
            atual = self.head
            trocou = False
    
            while atual.next != fim:
                proximo = atual.next
                if atual.valor > proximo.valor:
                    atual.valor, proximo.valor = proximo.valor, atual.valor
                    trocou = True
    
                atual = atual.next
    
            fim = atual
    
            if not trocou:
                break

    # def ordena_bubble(self):
    #     if self.head is None or self.head.next is None:
    #         return

    #     trocou = True
    #     while trocou:
    #         trocou = False
    #         atual = self.head

    #         while atual.next is not None:
    #             proximo = atual.next
    #             if atual.valor > proximo.valor:
    #                 atual.valor, proximo.valor = proximo.valor, atual.valor
    #                 trocou = True
    #             atual = atual.next



lista_desordenada = [13, 95, 119, 184, 96, 102, 21, 48, 137, 57, 99, 5, 45, 170, 154, 146]
lista = Lista()
for numero in lista_desordenada:
    lista.add_valor(numero)

print("Lista Desordenada.")
lista.imprime_lista()
lista.ordena_bubble()
print("Lista Ordenada.")
lista.imprime_lista()

