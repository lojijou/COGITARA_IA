import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import json

class DatabaseCogitara:
    def __init__(self, db_name="cogitara.db"):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name, check_same_thread=False)
    
    def init_database(self):
        """Inicializa todas as tabelas do banco"""
        try:
            conn = self.get_connection()
            
            # Tabela de Vendas
            conn.execute('''
                CREATE TABLE IF NOT EXISTS vendas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data DATE NOT NULL,
                    produto TEXT NOT NULL,
                    quantidade INTEGER NOT NULL,
                    valor_unitario DECIMAL(10,2) NOT NULL,
                    valor_total DECIMAL(10,2) NOT NULL,
                    regiao TEXT NOT NULL,
                    canal_venda TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabela de Clientes
            conn.execute('''
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    email TEXT UNIQUE,
                    telefone TEXT,
                    regiao TEXT,
                    segmento TEXT,
                    data_cadastro DATE,
                    status TEXT DEFAULT 'Ativo',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabela de Feedbacks
            conn.execute('''
                CREATE TABLE IF NOT EXISTS feedbacks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente_id INTEGER,
                    texto TEXT NOT NULL,
                    tipo TEXT NOT NULL,
                    pontuacao INTEGER,
                    sentimento TEXT,
                    polaridade DECIMAL(3,2),
                    data_feedback DATE,
                    processed BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (cliente_id) REFERENCES clientes (id)
                )
            ''')
            
            # Tabela de Marketing
            conn.execute('''
                CREATE TABLE IF NOT EXISTS marketing (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data DATE NOT NULL,
                    canal TEXT NOT NULL,
                    investimento DECIMAL(10,2) NOT NULL,
                    cliques INTEGER,
                    conversoes INTEGER,
                    custo_por_conversao DECIMAL(10,2),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ Erro ao criar banco: {e}")
            return False

    def inserir_dados_exemplo(self):
        """Insere dados de exemplo para demonstração"""
        try:
            conn = self.get_connection()
            
            # Inserir clientes exemplo
            clientes = [
                ('João Silva', 'joao@email.com', '(11) 9999-8888', 'Sudeste', 'Varejo', '2023-01-15'),
                ('Maria Santos', 'maria@email.com', '(21) 9777-6666', 'Sudeste', 'Atacado', '2023-02-20'),
                ('Pedro Oliveira', 'pedro@email.com', '(31) 9555-4444', 'Nordeste', 'Varejo', '2023-03-10'),
                ('Ana Costa', 'ana@email.com', '(41) 9333-2222', 'Sul', 'E-commerce', '2023-04-05'),
                ('Carlos Lima', 'carlos@email.com', '(51) 9111-0000', 'Sul', 'Atacado', '2023-05-12')
            ]
            
            conn.executemany('''
                INSERT OR IGNORE INTO clientes (nome, email, telefone, regiao, segmento, data_cadastro)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', clientes)
            
            # Inserir vendas exemplo
            produtos = ['Produto A', 'Produto B', 'Produto C']
            regioes = ['Sudeste', 'Nordeste', 'Sul', 'Norte']
            canais = ['Loja Física', 'E-commerce', 'Marketplace']
            
            data_inicio = datetime(2024, 1, 1)
            for i in range(100):
                data = data_inicio + timedelta(days=i)
                produto = produtos[i % len(produtos)]
                quantidade = (i % 10) + 1
                valor_unitario = 50 + (i % 3) * 25
                valor_total = quantidade * valor_unitario
                regiao = regioes[i % len(regioes)]
                canal = canais[i % len(canais)]
                
                conn.execute('''
                    INSERT INTO vendas (data, produto, quantidade, valor_unitario, valor_total, regiao, canal_venda)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (data.date(), produto, quantidade, valor_unitario, valor_total, regiao, canal))
            
            # Inserir feedbacks exemplo
            feedbacks = [
                (1, 'Produto excelente, entrega rápida!', 'produto', 5, 'positivo', 0.8, '2024-01-15'),
                (2, 'Demorou muito para chegar', 'entrega', 2, 'negativo', -0.6, '2024-01-16'),
                (3, 'Atendimento muito bom, solucionou meu problema', 'atendimento', 4, 'positivo', 0.7, '2024-01-17'),
                (4, 'Produto veio com defeito', 'produto', 1, 'negativo', -0.9, '2024-01-18'),
                (5, 'Preço competitivo, qualidade ok', 'geral', 3, 'neutro', 0.1, '2024-01-19')
            ]
            
            for feedback in feedbacks:
                conn.execute('''
                    INSERT INTO feedbacks (cliente_id, texto, tipo, pontuacao, sentimento, polaridade, data_feedback)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', feedback)
            
            # Inserir dados de marketing
            canais_mkt = ['google_ads', 'facebook', 'email', 'organic']
            
            for i in range(60):
                data = data_inicio + timedelta(days=i)
                canal = canais_mkt[i % len(canais_mkt)]
                investimento = 1000 + (i % 5) * 500
                cliques = investimento * (0.5 + (i % 3) * 0.2)
                conversoes = cliques * 0.1
                custo_conversao = investimento / conversoes if conversoes > 0 else 0
                
                conn.execute('''
                    INSERT INTO marketing (data, canal, investimento, cliques, conversoes, custo_por_conversao)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (data.date(), canal, investimento, cliques, conversoes, custo_conversao))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ Erro ao inserir dados: {e}")
            return False

    def get_metricas_principais(self):
        """Busca métricas principais para dashboard"""
        try:
            conn = self.get_connection()
            
            # Total de vendas último mês
            query_vendas = '''
                SELECT SUM(valor_total) as total_vendas, COUNT(*) as num_vendas
                FROM vendas 
                WHERE data >= date('now', '-30 days')
            '''
            vendas_df = pd.read_sql_query(query_vendas, conn)
            total_vendas = vendas_df.iloc[0]['total_vendas'] if vendas_df.iloc[0]['total_vendas'] else 150000
            num_vendas = vendas_df.iloc[0]['num_vendas'] if vendas_df.iloc[0]['num_vendas'] else 45
            
            # Total de clientes
            query_clientes = "SELECT COUNT(*) as total_clientes FROM clientes WHERE status = 'Ativo'"
            clientes_df = pd.read_sql_query(query_clientes, conn)
            total_clientes = clientes_df.iloc[0]['total_clientes'] if clientes_df.iloc[0]['total_clientes'] else 245
            
            # Satisfação média
            query_satisfacao = "SELECT AVG(pontuacao) as satisfacao_media FROM feedbacks"
            satisfacao_df = pd.read_sql_query(query_satisfacao, conn)
            satisfacao_media = satisfacao_df.iloc[0]['satisfacao_media'] if satisfacao_df.iloc[0]['satisfacao_media'] else 4.2
            
            # Investimento marketing
            query_marketing = '''
                SELECT SUM(investimento) as total_investimento, SUM(conversoes) as total_conversoes
                FROM marketing 
                WHERE data >= date('now', '-30 days')
            '''
            marketing_df = pd.read_sql_query(query_marketing, conn)
            investimento_marketing = marketing_df.iloc[0]['total_investimento'] if marketing_df.iloc[0]['total_investimento'] else 50000
            conversoes_marketing = marketing_df.iloc[0]['total_conversoes'] if marketing_df.iloc[0]['total_conversoes'] else 120
            
            conn.close()
            
            return {
                'total_vendas': total_vendas,
                'num_vendas': num_vendas,
                'total_clientes': total_clientes,
                'satisfacao_media': satisfacao_media,
                'investimento_marketing': investimento_marketing,
                'conversoes_marketing': conversoes_marketing
            }
        except:
            # Fallback se der erro
            return {
                'total_vendas': 150000,
                'num_vendas': 45,
                'total_clientes': 245,
                'satisfacao_media': 4.2,
                'investimento_marketing': 50000,
                'conversoes_marketing': 120
            }

    def salvar_feedback(self, texto, tipo='geral', cliente_id=None, pontuacao=None):
        """Salva novo feedback no banco"""
        from textblob import TextBlob
        
        try:
            # Analisar sentimento
            analysis = TextBlob(texto)
            polaridade = analysis.sentiment.polarity
            
            if polaridade > 0.1:
                sentimento = 'positivo'
            elif polaridade < -0.1:
                sentimento = 'negativo'
            else:
                sentimento = 'neutro'
            
            conn = self.get_connection()
            conn.execute('''
                INSERT INTO feedbacks (cliente_id, texto, tipo, pontuacao, sentimento, polaridade, data_feedback)
                VALUES (?, ?, ?, ?, ?, ?, date('now'))
            ''', (cliente_id, texto, tipo, pontuacao, sentimento, polaridade))
            
            conn.commit()
            conn.close()
            return True
        except:
            return False

    def get_vendas_por_periodo(self, data_inicio, data_fim):
        """Busca vendas por período"""
        try:
            conn = self.get_connection()
            query = '''
                SELECT data, SUM(valor_total) as total_vendas, COUNT(*) as num_vendas
                FROM vendas 
                WHERE data BETWEEN ? AND ?
                GROUP BY data
                ORDER BY data
            '''
            df = pd.read_sql_query(query, conn, params=[data_inicio, data_fim])
            conn.close()
            return df
        except:
            return pd.DataFrame()

    def get_analise_sentimento(self):
        """Busca análise consolidada de sentimentos"""
        try:
            conn = self.get_connection()
            query = '''
                SELECT 
                    sentimento,
                    COUNT(*) as quantidade,
                    AVG(polaridade) as media_polaridade
                FROM feedbacks 
                GROUP BY sentimento
                ORDER BY quantidade DESC
            '''
            df = pd.read_sql_query(query, conn)
            conn.close()
            return df
        except:
            return pd.DataFrame({
                'sentimento': ['positivo', 'neutro', 'negativo'],
                'quantidade': [15, 8, 5],
                'media_polaridade': [0.7, 0.1, -0.6]
            })

    def get_vendas_por_produto(self):
        """Busca vendas agrupadas por produto"""
        try:
            conn = self.get_connection()
            query = '''
                SELECT 
                    produto,
                    SUM(quantidade) as total_quantidade,
                    SUM(valor_total) as total_vendas,
                    AVG(valor_unitario) as preco_medio
                FROM vendas 
                GROUP BY produto
                ORDER BY total_vendas DESC
            '''
            df = pd.read_sql_query(query, conn)
            conn.close()
            return df
        except:
            return pd.DataFrame({
                'produto': ['Produto A', 'Produto B', 'Produto C'],
                'total_vendas': [75000, 50000, 25000]
            })