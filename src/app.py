import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sqlite3
import json
from textblob import TextBlob
import warnings
warnings.filterwarnings('ignore')

# Configuração da página
st.set_page_config(
    page_title="COGITARA IA - Do Dado à Decisão",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #F0F2F6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1E3A8A;
    }
</style>
""", unsafe_allow_html=True)

class DatabaseCogitara:
    def __init__(self, db_name="cogitara.db"):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def init_database(self):
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
        
        # Tabela de Feedbacks
        conn.execute('''
            CREATE TABLE IF NOT EXISTS feedbacks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                texto TEXT NOT NULL,
                tipo TEXT NOT NULL,
                pontuacao INTEGER,
                sentimento TEXT,
                polaridade DECIMAL(3,2),
                data_feedback DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()

    def inserir_dados_exemplo(self):
        conn = self.get_connection()
        
        # Inserir vendas exemplo
        produtos = ['Produto A', 'Produto B', 'Produto C']
        regioes = ['Sudeste', 'Nordeste', 'Sul']
        
        data_inicio = datetime(2023, 1, 1)
        for i in range(100):
            data = data_inicio + timedelta(days=i)
            produto = produtos[i % len(produtos)]
            quantidade = (i % 10) + 1
            valor_unitario = 50 + (i % 3) * 25
            valor_total = quantidade * valor_unitario
            regiao = regioes[i % len(regioes)]
            canal = 'E-commerce' if i % 2 == 0 else 'Loja Física'
            
            conn.execute('''
                INSERT INTO vendas (data, produto, quantidade, valor_unitario, valor_total, regiao, canal_venda)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (data.date(), produto, quantidade, valor_unitario, valor_total, regiao, canal))
        
        # Inserir feedbacks exemplo
        feedbacks = [
            ('Produto excelente, entrega rápida!', 'produto', 5, 'positivo', 0.8, '2024-01-15'),
            ('Demorou muito para chegar', 'entrega', 2, 'negativo', -0.6, '2024-01-16'),
            ('Atendimento muito bom!', 'atendimento', 4, 'positivo', 0.7, '2024-01-17'),
        ]
        
        for feedback in feedbacks:
            conn.execute('''
                INSERT INTO feedbacks (texto, tipo, pontuacao, sentimento, polaridade, data_feedback)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', feedback)
        
        conn.commit()
        conn.close()

class CogitaraApp:
    def __init__(self):
        self.db = DatabaseCogitara()
        
    def dashboard_principal(self):
        st.markdown('<h1 class="main-header">🚀 COGITARA IA</h1>', unsafe_allow_html=True)
        st.markdown("**Do dado à decisão, com visão e precisão**")
        
        # Métricas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📊 Vendas Totais", "R$ 150.000", "+12%")
        with col2:
            st.metric("😊 Satisfação", "4.2/5.0", "+0.3")
        with col3:
            st.metric("👥 Clientes", "245", "+8%")
        with col4:
            st.metric("🎯 Eficiência", "87%", "+5%")
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de vendas simulado
            datas = pd.date_range(start='2024-01-01', end='2024-01-31', freq='D')
            vendas = np.random.normal(5000, 1000, len(datas)).cumsum()
            df_vendas = pd.DataFrame({'Data': datas, 'Vendas': vendas})
            
            fig = px.line(df_vendas, x='Data', y='Vendas', title='📈 Tendência de Vendas')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Gráfico de produtos
            produtos = ['Produto A', 'Produto B', 'Produto C']
            vendas_prod = [45000, 35000, 25000]
            df_prod = pd.DataFrame({'Produto': produtos, 'Vendas': vendas_prod})
            
            fig = px.pie(df_prod, values='Vendas', names='Produto', title='📦 Vendas por Produto')
            st.plotly_chart(fig, use_container_width=True)

    def analise_preditiva(self):
        st.header("🔮 Análise Preditiva")
        
        # Simulação de previsão
        meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun']
        historico = [120, 135, 148, 160, 175, 190]
        previsao = [190, 205, 220, 238, 255, 275]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=meses, y=historico, name='Histórico', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=meses, y=previsao, name='Previsão', line=dict(color='red', dash='dash')))
        
        fig.update_layout(title='Previsão de Vendas - Próximos 6 Meses')
        st.plotly_chart(fig)
        
        # Métricas de previsão
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Crescimento Esperado", "15%")
        with col2:
            st.metric("Confiança da Previsão", "87%")
        with col3:
            st.metric("Melhor Produto", "Produto A")

    def simulador_cenarios(self):
        st.header("🎯 Simulador de Cenários")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Cenário Atual")
            vendas_atuais = st.number_input("Vendas Mensais (R$)", value=100000)
            custos_atuais = st.number_input("Custos Mensais (R$)", value=60000)
            margem_atual = (vendas_atuais - custos_atuais) / vendas_atuais * 100
            st.metric("Margem Atual", f"{margem_atual:.1f}%")
        
        with col2:
            st.subheader("🔄 Simular Mudanças")
            variacao_preco = st.slider("Variação no Preço (%)", -20, 20, 0)
            variacao_mkt = st.slider("Variação no Marketing (%)", -50, 100, 0)
            
            # Cálculo do novo cenário
            impacto_vendas = variacao_preco * -0.5 + variacao_mkt * 0.8
            novas_vendas = vendas_atuais * (1 + impacto_vendas/100)
            nova_margem = (novas_vendas - custos_atuais) / novas_vendas * 100
            
            st.metric("Novas Vendas", f"R$ {novas_vendas:,.0f}", 
                     delta=f"{((novas_vendas/vendas_atuais)-1)*100:.1f}%")
            st.metric("Nova Margem", f"{nova_margem:.1f}%")

    def analise_sentimento(self):
        st.header("😊 Análise de Sentimento")
        
        # Análise de texto
        feedback = st.text_area("Digite o feedback do cliente:")
        
        if st.button("Analisar Sentimento") and feedback:
            analysis = TextBlob(feedback)
            polaridade = analysis.sentiment.polarity
            
            if polaridade > 0.1:
                sentimento = "😊 POSITIVO"
                cor = "green"
            elif polaridade < -0.1:
                sentimento = "😡 NEGATIVO" 
                cor = "red"
            else:
                sentimento = "😐 NEUTRO"
                cor = "gray"
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Sentimento", sentimento)
            with col2:
                st.metric("Pontuação", f"{polaridade:.2f}")
            with col3:
                st.metric("Confiança", f"{(abs(polaridade)*100):.0f}%")
            
            # Recomendações
            if polaridade < 0:
                st.error("**🔍 Ação Recomendada:** Investigar causas e contatar o cliente.")
            else:
                st.success("**✅ Status:** Cliente satisfeito - manter qualidade.")

    def run(self):
        # Sidebar
        st.sidebar.image("https://via.placeholder.com/150x50/1E3A8A/FFFFFF?text=COGITARA", use_column_width=True)
        st.sidebar.title("Navegação")
        
        pagina = st.sidebar.selectbox(
            "Selecione a página:",
            ["🏠 Dashboard", "🔮 Análise Preditiva", "🎯 Simulador", "😊 Análise de Sentimento"]
        )
        
        st.sidebar.markdown("---")
        st.sidebar.info("""
        **COGITARA IA**
        - Análise Preditiva
        - Simulador de Cenários  
        - Análise de Sentimento
        - Dashboard em Tempo Real
        """)
        
        if st.sidebar.button("🔄 Carregar Dados Exemplo"):
            self.db.inserir_dados_exemplo()
            st.sidebar.success("Dados carregados!")
        
        # Navegação
        if pagina == "🏠 Dashboard":
            self.dashboard_principal()
        elif pagina == "🔮 Análise Preditiva":
            self.analise_preditiva()
        elif pagina == "🎯 Simulador":
            self.simulador_cenarios()
        elif pagina == "😊 Análise de Sentimento":
            self.analise_sentimento()

# Executar app
if __name__ == "__main__":
    app = CogitaraApp()
    app.run()