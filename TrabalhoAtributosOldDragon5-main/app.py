import json
from flask import Flask, render_template, request, redirect, url_for
import os
import random

# Importa as classes Raça, Classe e Personagem
from model.personagem import Personagem
from model.raca import Raca
from model.classes import Classe

app = Flask(__name__)

# Instâncias de Raça
racas = {
    'Humano': Raca('Humano', 9, 'Não', 'Qualquer', ['Versatilidade']),
    'Elfo': Raca('Elfo', 9, 'Sim (Visão na Penumbra)', 'Caótico', ['Conhecimento Mágico', 'Sentidos Aguçados']),
    'Anão': Raca('Anão', 6, 'Sim (Visão no Escuro)', 'Leal', ['Resistência a Veneno', 'Sentidos Aguçados']),
    'Halfling': Raca('Halfling', 6, 'Não', 'Leal', ['Ataque Furtivo', 'Sorte dos Halflings']),
}

# Instâncias de Classe
classes = {
    'Guerreiro': Classe('Guerreiro', '1d8', ['Lâmina parte Serpentes', 'Rigidez Voraz']),
    'Mago': Classe('Mago', '1d4', ['Magias (Nível 1)']),
    'Ladino': Classe('Ladino', '1d6', ['Ataque Furtivo', 'Esconder nas Sombras']),
    'Clérigo': Classe('Clérigo', '1d6', ['Cura', 'Expulsar Mortos-Vivos']),
}


# --- ROTAS PRINCIPAIS ---

@app.route('/')
def pagina_inicial():
    """Renderiza a página inicial com o formulário."""
    # Passa as chaves de raças e classes para o HTML
    return render_template('index.html', racas=racas.keys(), classes=classes.keys())

@app.route('/criar-personagem', methods=['POST'])
def criar_personagem():
    """
    Processa os dados do formulário inicial.
    Redireciona para o resultado (Clássico) ou para a distribuição (Aventureiro/Heroico).
    """
    # Coleta os dados do formulário
    nome = request.form.get('nome')
    raca_nome = request.form.get('raca')
    classe_nome = request.form.get('classe')
    metodo = request.form.get('metodo')
    
    # Validações básicas
    if not all([nome, raca_nome, classe_nome, metodo]):
        return "Erro: Todos os campos devem ser preenchidos.", 400

    # Cria a instância base
    raca = racas.get(raca_nome)
    classe = classes.get(classe_nome)
    personagem = Personagem(nome=nome, raca=raca, classe=classe)

    if metodo == 'Classico':
        # Método Clássico rola e salva na hora
        personagem.gerar_atributos_classico()
        personagem.gerar_detalhes_ficha()
        personagem.salvar_em_json()
        
        # Redireciona para a página de resultado
        return render_template('resultado.html', personagem=personagem.__dict__())
        
    else:
        # Métodos Heroico/Aventureiro rolam 6 valores para distribuir
        valores_rolados = personagem._rolar_atributos_para_distribuir(metodo)
        
        # Envia os dados básicos e os valores rolados para a página de distribuição
        return render_template('distribuir.html', 
                               nome=nome, 
                               raca=raca_nome, 
                               classe=classe_nome, 
                               valores=valores_rolados)

@app.route('/salvar-distribuicao', methods=['POST'])
def salvar_distribuicao():
    """
    Recebe os dados da distribuição de atributos e salva o personagem.
    """
    
    try:
        # 1. Coleta os dados básicos e os atributos
        nome = request.form.get('nome')
        raca_nome = request.form.get('raca')
        classe_nome = request.form.get('classe')
        
        # Converte os valores dos atributos para inteiros
        atributos = {
            'FOR': int(request.form.get('FOR')),
            'DES': int(request.form.get('DES')),
            'CON': int(request.form.get('CON')),
            'INT': int(request.form.get('INT')),
            'SAB': int(request.form.get('SAB')),
            'CAR': int(request.form.get('CAR'))
        }
        
        # 2. Verifica se todos os dados essenciais estão presentes
        if not all([nome, raca_nome, classe_nome]):
             raise ValueError("Dados essenciais (Nome, Raça ou Classe) não foram recebidos.")

        # 3. Recria os objetos Raça e Classe
        raca = racas.get(raca_nome)
        classe = classes.get(classe_nome)
        
        if not raca or not classe:
            raise ValueError("Raça ou Classe inválida encontrada no formulário.")
            
        # 4. Cria a instância Personagem com os atributos distribuídos
        personagem = Personagem(nome=nome, raca=raca, classe=classe, atributos=atributos)
        
        # 5. Finaliza a criação e salva
        personagem.gerar_detalhes_ficha()
        personagem.salvar_em_json() # AQUI A FUNÇÃO QUE SALVA O JSON É CHAMADA
        
        # 6. Redireciona para a página de resultado
        return render_template('resultado.html', personagem=personagem.__dict__())

    except Exception as e:
        # Imprime o erro no console do terminal para ajudar no debug
        print(f"ERRO CRÍTICO NA ROTA SALVAR_DISTRIBUICAO: {e}")
        # Retorna uma mensagem de erro mais informativa no navegador
        return f"Erro ao salvar distribuição: {e}", 500

if __name__ == '__main__':
    # Configuração de debug e porta
    app.run(debug=True)