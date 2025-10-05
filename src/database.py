import pandas as pd

class DatabaseSimulacao:
    def __init__(self):
        self.dados_carregados = False
    
    def carregar_dados_exemplo(self):
        self.dados_carregados = True
        return True
    
    def get_metricas_principais(self):
        return {
            'total_vendas': 152000,
            'num_vendas': 48,
            'total_clientes': 247,
            'satisfacao_media': 4.3,
            'investimento_marketing': 52000,
            'conversoes_marketing': 125
        }
    
    def get_vendas_por_produto(self):
        return pd.DataFrame({
            'produto': ['Produto A', 'Produto B', 'Produto C'],
            'total_vendas': [82000, 45000, 25000]
        })
    
    def get_analise_sentimento(self):
        return pd.DataFrame({
            'sentimento': ['positivo', 'neutro', 'negativo'],
            'quantidade': [18, 9, 4],
            'media_polaridade': [0.72, 0.08, -0.65]
        })
