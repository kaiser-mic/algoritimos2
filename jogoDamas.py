"""
Jogo de Damas - Versão Completa com Tkinter
Criado do zero com interface gráfica moderna
Funcionalidades: Promoção a Dama, Voo da Dama, Captura Múltipla
(Versão sem o desenho da árvore de jogadas)
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext
import math
from abc import ABC


class Peca(ABC):
    id_peca = 0

    @classmethod
    def gerar_id(cls):
        cls.id_peca += 1
        return cls.id_peca


class Jogada:
    def __init__(self, origem: tuple, destino: tuple, tipo: str):
        self.id_jogada = Peca.gerar_id()
        self.origem = origem
        self.destino = destino
        self.tipo = tipo
        self.filho_esquerdo = None
        self.filho_direito = None


class ArvoreDeJogadas:
    def __init__(self):
        self.raiz = None

    def inserir_jogada(self, nova_jogada: Jogada):
        if self.raiz is None:
            self.raiz = nova_jogada
        else:
            self._inserir(self.raiz, nova_jogada)

    def _inserir(self, atual: Jogada, nova_jogada: Jogada):
        if atual.destino == nova_jogada.origem:
            if nova_jogada.tipo == 'movimento':
                if atual.filho_esquerdo is None:
                    atual.filho_esquerdo = nova_jogada
                else:
                    self._inserir(atual.filho_esquerdo, nova_jogada)
            elif nova_jogada.tipo == 'captura':
                if atual.filho_direito is None:
                    atual.filho_direito = nova_jogada
                else:
                    self._inserir(atual.filho_direito, nova_jogada)
        else:
            if atual.filho_esquerdo:
                self._inserir(atual.filho_esquerdo, nova_jogada)
            if atual.filho_direito:
                self._inserir(atual.filho_direito, nova_jogada)

    def exibir_in_ordem(self):
        def _in_ordem(no):
            if no:
                _in_ordem(no.filho_esquerdo)
                print(f"{no.tipo.upper()}: {no.origem} → {no.destino}")
                _in_ordem(no.filho_direito)

        _in_ordem(self.raiz)

    def buscar_por_destino(self, destino: tuple) -> Jogada:
        def _buscar(no):
            if no is None:
                return None
            if no.destino == destino:
                return no
            return _buscar(no.filho_esquerdo) or _buscar(no.filho_direito)

        return _buscar(self.raiz)

    def caminho_agressivo(self):
        caminho = []
        atual = self.raiz
        while atual:
            caminho.append(f"{atual.tipo.upper()}: {atual.origem} → {atual.destino}")
            atual = atual.filho_direito
        for passo in caminho:
            print(passo)


class JogoDamas:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎮 Jogo de Damas")
        self.root.geometry("1000x700")
        self.root.configure(bg='#1a1a1a')

        self.tabuleiro = [[None for _ in range(8)] for _ in range(8)]
        self.jogador = 'P'
        self.jogada_origem = None
        self.jogada_destino = None
        self.tipo_jogada = "movimento"
        self.peca_capturada_coord = None
        self.peca_em_captura_multipla = None

        self.arvore = ArvoreDeJogadas()
        self.todas_jogadas = []

        self.inicializar_tabuleiro()
        self.criar_interface()
        self.atualizar_display()

    def inicializar_tabuleiro(self):
        for linha in range(3):
            for coluna in range(8):
                if (linha + coluna) % 2 == 1:
                    self.tabuleiro[linha][coluna] = 'P'

        for linha in range(5, 8):
            for coluna in range(8):
                if (linha + coluna) % 2 == 1:
                    self.tabuleiro[linha][coluna] = 'B'

    def criar_interface(self):
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        board_frame = tk.Frame(main_frame, bg='#2d2d2d', relief=tk.RAISED, bd=3)
        board_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))

        title_label = tk.Label(board_frame, text="🎯 TABULEIRO DE DAMAS",
                                 font=('Arial', 18, 'bold'),
                                 bg='#2d2d2d', fg='white')
        title_label.pack(pady=15)

        self.board_canvas = tk.Canvas(board_frame, width=400, height=400,
                                        bg='#f8f9fa', relief=tk.SUNKEN, bd=3)
        self.board_canvas.pack(pady=15)
        self.board_canvas.bind("<Button-1>", self.on_board_click)

        controls_frame = tk.Frame(board_frame, bg='#2d2d2d')
        controls_frame.pack(pady=15)

        self.btn_movimento = tk.Button(controls_frame, text="📝 MOVIMENTO",
                                         command=lambda: self.set_tipo_jogada("movimento"),
                                         bg='#4CAF50', fg='blue', font=('Arial', 12, 'bold'),
                                         relief=tk.RAISED, bd=2, padx=15, pady=8)
        self.btn_movimento.pack(side=tk.LEFT, padx=8)

        self.btn_captura = tk.Button(controls_frame, text="⚔️ CAPTURA",
                                       command=lambda: self.set_tipo_jogada("captura"),
                                       bg='#f44336', fg='blue', font=('Arial', 12, 'bold'),
                                       relief=tk.RAISED, bd=2, padx=15, pady=8)
        self.btn_captura.pack(side=tk.LEFT, padx=8)

        self.status_label = tk.Label(board_frame, text="",
                                       font=('Arial', 14, 'bold'),
                                       bg='#2d2d2d', fg='#ffeb3b')
        self.status_label.pack(pady=10)

        # Frame do Log (anteriormente 'tree_frame')
        log_frame = tk.Frame(main_frame, bg='#2d2d2d', relief=tk.RAISED, bd=3)
        log_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Título do Log
        log_title = tk.Label(log_frame, text="📜 LOG DE JOGADAS",
                                font=('Arial', 18, 'bold'),
                                bg='#2d2d2d', fg='white')
        log_title.pack(pady=15)

        # Botões
        tree_buttons_frame = tk.Frame(log_frame, bg='#2d2d2d')
        tree_buttons_frame.pack(pady=15)

        self.btn_arvore_completa = tk.Button(tree_buttons_frame, text="📊 TODAS JOGADAS",
                                               command=self.mostrar_arvore_completa,
                                               bg='#2196F3', fg='blue', font=('Arial', 11, 'bold'),
                                               relief=tk.RAISED, bd=2, padx=12, pady=6)
        self.btn_arvore_completa.pack(side=tk.LEFT, padx=8)

        # Área de texto
        self.info_text = scrolledtext.ScrolledText(log_frame, height=8, width=45,
                                                   bg='#1a1a1a', fg='white',
                                                   font=('Consolas', 10))
        # Fazer o log preencher o espaço restante
        self.info_text.pack(pady=15, padx=15, fill=tk.BOTH, expand=True)

        self.set_tipo_jogada("movimento")

    def desenhar_tabuleiro(self):
        self.board_canvas.delete("all")

        cell_size = 50
        start_x = 10
        start_y = 10

        for linha in range(8):
            for coluna in range(8):
                x1 = start_x + coluna * cell_size
                y1 = start_y + linha * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                if (linha + coluna) % 2 == 0:
                    cor = '#f8f9fa'
                else:
                    cor = '#2c3e50'

                self.board_canvas.create_rectangle(x1, y1, x2, y2,
                                                   fill=cor, outline='#34495e', width=2)

                peca = self.tabuleiro[linha][coluna]
                if peca:
                    centro_x = x1 + cell_size // 2
                    centro_y = y1 + cell_size // 2
                    raio = cell_size // 3

                    if peca in ('P', 'PD'):
                        cor_peca = '#e74c3c'
                        cor_borda = '#c0392b'
                    else:
                        cor_peca = '#f39c12'
                        cor_borda = '#d68910'

                    self.board_canvas.create_oval(centro_x - raio, centro_y - raio,
                                                    centro_x + raio, centro_y + raio,
                                                    fill=cor_peca, outline=cor_borda, width=3)
                    
                    if peca in ('PD', 'BD'):
                        self.board_canvas.create_text(centro_x, centro_y,
                                                      text="👑",
                                                      font=('Arial', 14), fill='white')

                coord_text = f"{linha},{coluna}"
                self.board_canvas.create_text(x1 + 8, y1 + 8, text=coord_text,
                                                font=('Arial', 8), fill='#7f8c8d')

        if self.jogada_origem:
            linha, coluna = self.jogada_origem
            x1 = start_x + coluna * cell_size
            y1 = start_y + linha * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size

            self.board_canvas.create_rectangle(x1, y1, x2, y2,
                                                 outline='#ffeb3b', width=5)

    # --- MÉTODOS desenhar_arvore e _desenhar_no_arvore REMOVIDOS ---

    def on_board_click(self, event):
        cell_size = 50
        start_x = 10
        start_y = 10

        coluna = (event.x - start_x) // cell_size
        linha = (event.y - start_y) // cell_size

        if 0 <= linha < 8 and 0 <= coluna < 8:
            if self.jogada_origem is None:
                peca = self.tabuleiro[linha][coluna]
                if peca:
                    cor_peca = 'P' if peca in ('P', 'PD') else 'B'
                    
                    if cor_peca == self.jogador:
                        self.jogada_origem = (linha, coluna)
                        self.atualizar_display()
                        self.info_text.insert(tk.END, f"✅ Origem selecionada: ({linha}, {coluna})\n")
                    else:
                        self.info_text.insert(tk.END, f"❌ Peça do adversário!\n")
                else:
                    self.info_text.insert(tk.END, f"❌ Casa vazia ou não é seu jogador\n")
            else:
                self.jogada_destino = (linha, coluna)
                self.executar_jogada()

    def executar_jogada(self):
        if self.jogada_origem and self.jogada_destino:
            origem_linha, origem_coluna = self.jogada_origem
            destino_linha, destino_coluna = self.jogada_destino

            if self.validar_jogada():
                peca = self.tabuleiro[origem_linha][origem_coluna]
                self.tabuleiro[origem_linha][origem_coluna] = None
                self.tabuleiro[destino_linha][destino_coluna] = peca

                if peca == 'P' and destino_linha == 7:
                    peca = 'PD'
                    self.tabuleiro[destino_linha][destino_coluna] = 'PD'
                    self.info_text.insert(tk.END, f"👑 PROMOÇÃO! Peça Preta virou Dama!\n")
                elif peca == 'B' and destino_linha == 0:
                    peca = 'BD'
                    self.tabuleiro[destino_linha][destino_coluna] = 'BD'
                    self.info_text.insert(tk.END, f"👑 PROMOÇÃO! Peça Branca virou Dama!\n")

                if self.tipo_jogada == 'captura':
                    if self.peca_capturada_coord:
                        l_cap, c_cap = self.peca_capturada_coord
                        self.tabuleiro[l_cap][c_cap] = None
                        self.info_text.insert(tk.END, f"⚔️ Peça em ({l_cap}, {c_cap}) capturada!\n")
                    else:
                        self.info_text.insert(tk.END, f"⚠️ Erro na captura: Coordenadas não encontradas.\n")

                jogada = Jogada(self.jogada_origem, self.jogada_destino, self.tipo_jogada)
                self.arvore.inserir_jogada(jogada)
                self.todas_jogADAS.append(jogada)

                self.info_text.insert(tk.END,
                                      f"✅ Jogada executada: {self.tipo_jogada.upper()} de {self.jogada_origem} para {self.jogada_destino}\n")

                if self.tipo_jogada == 'captura':
                    novas_capturas = self._buscar_capturas_disponiveis(destino_linha, destino_coluna)
                    
                    if novas_capturas:
                        self.info_text.insert(tk.END, "🔥 CAPTURA MÚLTIPLA! Realize a próxima.\n")
                        self.peca_em_captura_multipla = (destino_linha, destino_coluna)
                        self.jogada_origem = (destino_linha, destino_coluna)
                        self.jogada_destino = None
                        self.set_tipo_jogada("captura")
                        self.atualizar_display()
                    else:
                        self.info_text.insert(tk.END, "Turno finalizado.\n")
                        self.jogador = 'B' if self.jogador == 'P' else 'P'
                        self.limpar_selecao()
                        self.atualizar_display()
                else:
                    self.jogador = 'B' if self.jogador == 'P' else 'P'
                    self.limpar_selecao()
                    self.atualizar_display()

                self.verificar_fim_jogo()
            
            else:
                self.info_text.insert(tk.END, f"❌ Jogada inválida!\n")
                
                if self.peca_em_captura_multipla:
                    self.jogada_destino = None
                    self.info_text.insert(tk.END, f"❗️ Deve completar a captura de {self.jogada_origem}\n")
                    self.atualizar_display()
                else:
                    self.limpar_selecao()
    
    def _buscar_capturas_disponiveis(self, l_origem, c_origem):
        origem_original = self.jogada_origem
        destino_original = self.jogada_destino
        tipo_original = self.tipo_jogada

        peca = self.tabuleiro[l_origem][c_origem]
        if not peca:
            return []

        capturas_possiveis = []
        
        direcoes_passos = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for step_l, step_c in direcoes_passos:
            if peca == 'P' and step_l < 0: continue
            if peca == 'B' and step_l > 0: continue

            if peca in ('P', 'B'):
                distancias = [2]
            else:
                distancias = range(2, 8)

            for dist in distancias:
                l_dest = l_origem + (step_l * dist)
                c_dest = c_origem + (step_c * dist)
                
                self.jogada_origem = (l_origem, c_origem)
                self.jogada_destino = (l_dest, c_dest)
                self.tipo_jogada = 'captura'

                if 0 <= l_dest < 8 and 0 <= c_dest < 8:
                    if self.validar_jogada():
                        capturas_possiveis.append((l_dest, c_dest))
                        if peca in ('P', 'B'):
                            break
                else:
                    break

        self.jogada_origem = origem_original
        self.jogada_destino = destino_original
        self.tipo_jogada = tipo_original

        return capturas_possiveis

    def validar_jogada(self):
        self.peca_capturada_coord = None
        
        origem_linha, origem_coluna = self.jogada_origem
        destino_linha, destino_coluna = self.jogada_destino

        peca = self.tabuleiro[origem_linha][origem_coluna]

        if not (0 <= destino_linha < 8 and 0 <= destino_coluna < 8):
            return False

        if (destino_linha + destino_coluna) % 2 == 0:
            return False

        if self.tabuleiro[destino_linha][destino_coluna] is not None:
            return False

        delta_linha = abs(destino_linha - origem_linha)
        delta_coluna = abs(destino_coluna - origem_coluna)

        if delta_linha != delta_coluna or delta_linha == 0:
            return False

        if peca in ('P', 'B'):
            direcao = destino_linha - origem_linha
            if peca == 'P' and direcao < 0: return False
            if peca == 'B' and direcao > 0: return False

            if self.tipo_jogada == 'movimento':
                if delta_linha == 1:
                    return True
            
            elif self.tipo_jogada == 'captura':
                if delta_linha == 2:
                    meio_linha = (origem_linha + destino_linha) // 2
                    meio_coluna = (origem_coluna + destino_coluna) // 2
                    adversario = self.tabuleiro[meio_linha][meio_coluna]

                    if adversario is None: return False
                    
                    cor_adversario = 'P' if adversario in ('P', 'PD') else 'B'
                    if cor_adversario != self.jogador:
                        self.peca_capturada_coord = (meio_linha, meio_coluna)
                        return True
        
        elif peca in ('PD', 'BD'):
            step_linha = 1 if destino_linha > origem_linha else -1
            step_coluna = 1 if destino_coluna > origem_coluna else -1

            pecas_no_caminho = []
            pecas_amigas_no_caminho = 0

            l, c = origem_linha + step_linha, origem_coluna + step_coluna
            while l != destino_linha:
                peca_no_caminho = self.tabuleiro[l][c]
                if peca_no_caminho:
                    cor_peca = 'P' if peca_no_caminho in ('P', 'PD') else 'B'
                    if cor_peca == self.jogador:
                        pecas_amigas_no_caminho += 1
                    else:
                        pecas_no_caminho.append((l, c))
                
                l += step_linha
                c += step_coluna

            if self.tipo_jogada == 'movimento':
                if pecas_amigas_no_caminho == 0 and len(pecas_no_caminho) == 0:
                    return True
            
            elif self.tipo_jogada == 'captura':
                if pecas_amigas_no_caminho > 0:
                    return False
                
                if len(pecas_no_caminho) == 1:
                    self.peca_capturada_coord = pecas_no_caminho[0]
                    return True

        return False

    def set_tipo_jogada(self, tipo):
        self.tipo_jogada = tipo
        if tipo == "movimento":
            self.btn_movimento.configure(bg='#45a049', relief=tk.SUNKEN)
            self.btn_captura.configure(bg='#f44336', relief=tk.RAISED)
        else:
            self.btn_movimento.configure(bg='#4CAF50', relief=tk.RAISED)
            self.btn_captura.configure(bg='#da190b', relief=tk.SUNKEN)

    def limpar_selecao(self):
        self.jogada_origem = None
        self.jogada_destino = None
        self.peca_capturada_coord = None
        self.peca_em_captura_multipla = None
        self.atualizar_display()

    def mostrar_arvore_completa(self):
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, "🌳 TODAS AS JOGADAS REALIZADAS:\n")
        self.info_text.insert(tk.END, "=" * 50 + "\n")

        if self.todas_jogadas:
            for i, jogada in enumerate(self.todas_jogadas, 1):
                self.info_text.insert(tk.END, f"{i}. {jogada.tipo.upper()}: {jogada.origem} → {jogada.destino}\n")

            self.info_text.insert(tk.END, f"\n📊 Total de jogadas: {len(self.todas_jogadas)}\n")
        else:
            self.info_text.insert(tk.END, "Nenhuma jogada realizada ainda.\n")

    def verificar_fim_jogo(self):
        pretas = sum(1 for linha in self.tabuleiro for casa in linha if casa in ('P', 'PD'))
        brancas = sum(1 for linha in self.tabuleiro for casa in linha if casa in ('B', 'BD'))

        if pretas == 0:
            messagebox.showinfo("🏆 Fim de Jogo!", "Brancas venceram!\nTodas as peças pretas foram capturadas!")
            self.root.quit()
        elif brancas == 0:
            messagebox.showinfo("🏆 Fim de Jogo!", "Pretas venceram!\nTodas as peças brancas foram capturadas!")
            self.root.quit()

    def atualizar_display(self):
        self.desenhar_tabuleiro()
        # A chamada self.desenhar_arvore() foi removida daqui

        pretas = sum(1 for linha in self.tabuleiro for casa in linha if casa in ('P', 'PD'))
        brancas = sum(1 for linha in self.tabuleiro for casa in linha if casa in ('B', 'BD'))
        
        cor_jogador = "Pretas" if self.jogador == 'P' else "Brancas"
        status_text = f"🎯 Jogador: {cor_jogador} | Pretas (Vermelho): {pretas} | Brancas (Laranja): {brancas}"
        self.status_label.configure(text=status_text)

    def executar(self):
        self.root.mainloop()


if __name__ == "__main__":
    jogo = JogoDamas()
    jogo.executar()
