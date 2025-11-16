import random
import json
import os
from .raca import Raca # Importa Raca do mesmo módulo
from .classes import Classe # Importa Classe do mesmo módulo

class Personagem:
    """Classe que representa o personagem, incluindo atributos e detalhes da ficha."""
    
    def __init__(self, nome, raca: Raca, classe: Classe, atributos=None):
        """
        Inicializa o Personagem.
        Atributos é opcional, usado para métodos de rolagem com distribuição (Heroico/Aventureiro).
        """
        self.nome = nome
        self.raca = raca
        self.classe = classe
        self.atributos = atributos if atributos is not None else {}
        self.modificadores = {}
        self.pontos_de_vida_max = 0
        self.pontos_de_vida_atuais = 0
        self.protecao = 10
        self.movimento = None
        self.infravisao = None
        self.alinhamento = None
        self.habilidades_raca = None
        self.dado_de_vida = None
        self.habilidades_classe = None

    # --- MÉTODOS DE ROLAGEM E ATRIBUIÇÃO ---

    def _rolar_atributo_individual(self, metodo="Aventureiro"):
        """Rola UM valor de atributo (3d6 ou 4d6k3)."""
        if metodo == "Heroico":
            # 4d6, remove o menor (Heroico)
            rolagens = [random.randint(1, 6) for _ in range(4)]
            rolagens.sort() 
            return sum(rolagens[1:]) # Soma os 3 maiores
        else: 
            return sum(random.randint(1, 6) for _ in range(3)) 

    def _rolar_atributos_para_distribuir(self, metodo):
        """Rola 6 valores e os retorna em uma lista para o usuário distribuir."""
        # Cria uma lista de 6 valores, chamando a função individual 6 vezes
        valores = [self._rolar_atributo_individual(metodo) for _ in range(6)]
        
        # Ordena do maior para o menor (prática comum em Old Dragon)
        valores.sort(reverse=True) 
        
        # Retorna a lista de 6 inteiros
        return valores
        
    def _calcular_modificador(self, valor):
        """Calcula modificador OldDragon (<=8 é -1, 9-12 é 0, >=13 é 1)."""
        if valor <= 8: 
            return -1
        if valor <= 12: 
            return 0
        if valor >= 13: 
            return 1
        return 0 # Valor padrão

    def gerar_atributos_classico(self):
        """Rola 3d6 em ordem para os 6 atributos (Clássico)."""
        nomes_atributos = ["FOR", "DES", "CON", "INT", "SAB", "CAR"]
        for atr in nomes_atributos:
            # Rola 3d6 (Método Aventureiro) para cada atributo na ordem
            valor = self._rolar_atributo_individual(metodo="Aventureiro")
            self.atributos[atr] = valor
            self.modificadores[atr] = self._calcular_modificador(valor)

    # --- MÉTODOS DE PREENCHIMENTO DE FICHA ---
    
    def gerar_detalhes_ficha(self):
        """Preenche os detalhes da ficha com base na Raça e Classe."""
        # Detalhes da Raça
        self.movimento = self.raca.movimento
        self.infravisao = self.raca.infravisao
        self.alinhamento = self.raca.alinhamento
        self.habilidades_raca = self.raca.habilidades
        
        # Detalhes da Classe
        self.dado_de_vida = self.classe.dado_de_vida
        self.habilidades_classe = self.classe.habilidades
        
        # Cálculo de PV (Assumindo Nível 1)
        # Old Dragon PV: Dado de Vida + Modificador de CON
        # Simplificação: Usaremos apenas o valor máximo do dado (ex: 8 para d8)
        
        # Extrai o número do dado de vida (ex: "1d8" -> 8)
        pv_base = int(self.dado_de_vida.split('d')[-1]) if 'd' in self.dado_de_vida else 4 
        mod_con = self.modificadores.get('CON', 0)
        
        self.pontos_de_vida_max = pv_base + mod_con
        # PV Mínimo de 1
        if self.pontos_de_vida_max < 1:
            self.pontos_de_vida_max = 1
            
        self.pontos_de_vida_atuais = self.pontos_de_vida_max
        
        # Proteção (Assumindo 10 + DES, sem armadura)
        mod_des = self.modificadores.get('DES', 0)
        self.protecao = 10 + mod_des

    # --- MÉTODO DE SALVAMENTO ---

    def salvar_em_json(self):
        """Salva a ficha do personagem em um arquivo JSON."""
        # Cria um dicionário com os dados a serem salvos
        dados_salvar = {
            "nome": self.nome,
            "raca": self.raca.nome,
            "classe": self.classe.nome,
            "atributos": self.atributos,
            "modificadores": self.modificadores,
            "pontos_de_vida_max": self.pontos_de_vida_max,
            "pontos_de_vida_atuais": self.pontos_de_vida_atuais,
            "protecao": self.protecao,
            "movimento": self.movimento,
            "infravisao": self.infravisao,
            "alinhamento": self.alinhamento,
            "habilidades_raca": self.habilidades_raca,
            "dado_de_vida": self.dado_de_vida,
            "habilidades_classe": self.habilidades_classe,
        }
        
        # Nome do arquivo baseado no nome do personagem
        nome_arquivo = f"{self.nome.lower().replace(' ', '_')}.json"
        
        # Salva o arquivo na raiz do projeto
        caminho_arquivo = os.path.join(os.getcwd(), nome_arquivo)
        
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            # Garante que o JSON seja legível
            json.dump(dados_salvar, f, ensure_ascii=False, indent=4)
            
        print(f"\n[SUCESSO] Personagem '{self.nome}' salvo em {nome_arquivo}")

    def __dict__(self):
        """Retorna o objeto como um dicionário para o Flask/Jinja2."""
        return {
            "nome": self.nome,
            "raca": self.raca.nome,
            "classe": self.classe.nome,
            "atributos": self.atributos,
            "modificadores": self.modificadores,
            "pontos_de_vida_max": self.pontos_de_vida_max,
            "pontos_de_vida_atuais": self.pontos_de_vida_atuais,
            "protecao": self.protecao,
            "movimento": self.movimento,
            "infravisao": self.infravisao,
            "alinhamento": self.alinhamento,
            "habilidades_raca": self.habilidades_raca,
            "dado_de_vida": self.dado_de_vida,
            "habilidades_classe": self.habilidades_classe,
        }