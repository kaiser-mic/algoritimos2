class Turma:
    def __init__(self) -> None:
        self.alunos = []

    def inserir_aluno(self, nome, matricula, nota):
        novo_aluno = {"matricula": matricula, "nome": nome, "nota": nota }
        self.alunos.append(novo_aluno)
        print(f"Aluno {nome} inserido om sucesso! \n" )
    
    def lista_ordenada_matricula(self):
        self.alunos.sort