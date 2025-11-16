from distribui import Classico, Heroico, Aventureiro
from model.raca import Humano, Anao, Elfo
from classes import Guerreiro, Mago, Ladino
from personagem import Personagem

def escolher_distribuidor():
    print("\nEscolha o método de distribuição de atributos:")
    print("1 - Clássico")
    print("2 - Heroico")
    print("3 - Aventureiro")
    escolha = input("Digite sua escolha: ")

    if escolha == "1":
        return Classico()
    elif escolha == "2":
        return Heroico()
    elif escolha == "3":
        return Aventureiro()
    else:
        print("Opção inválida, usando Clássico por padrão.")
        return Classico()

def escolher_raca():
    print("\nEscolha a raça:")
    print("1 - Humano")
    print("2 - Anão")
    print("3 - Elfo")
    escolha = input("Digite sua escolha: ")

    if escolha == "1":
        return Humano()
    elif escolha == "2":
        return Anao()
    elif escolha == "3":
        return Elfo()
    else:
        print("Opção inválida, usando Humano por padrão.")
        return Humano()

def escolher_classe():
    print("\nEscolha a classe:")
    print("1 - Guerreiro")
    print("2 - Mago")
    print("3 - Ladino")
    escolha = input("Digite sua escolha: ")

    if escolha == "1":
        return Guerreiro()
    elif escolha == "2":
        return Mago()
    elif escolha == "3":
        return Ladino()
    else:
        print("Opção inválida, usando Guerreiro por padrão.")
        return Guerreiro()

def main():
    nome = input("Digite o nome do seu personagem: ")
    distribuidor = escolher_distribuidor()
    atributos = distribuidor.distribuir()
    raca = escolher_raca()
    classe = escolher_classe()
    personagem = Personagem(nome, atributos, raca, classe)
    personagem.exibir()

if __name__ == "__main__":
    main()
