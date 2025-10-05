import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sqlite3
import json
import warnings
import sys
import os

# Configuração de caminhos
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    from database import DatabaseCogitara
    from utils import IAGenerativa
    DB_LOADED = True
except ImportError as e:
    st.error(f"❌ Erro ao carregar módulos: {e}")
    DB_LOADED = False
    
    # Modo de emergência
    class DatabaseCogitara:
        def __init__(self, db_name="cogitara.db"):
            self.db_name = db_name
        def inserir_dados_exemplo(self):
            st.success("✅ Dados de exemplo carregados (modo simulação)")
            return True
        def get_metricas_principais(self):
            return {
                'total_vendas': 150000, 
                'num_vendas': 45,
                'total_clientes': 245, 
                'satisfacao_media': 4.2,
                'investimento_marketing': 50000,
                'conversoes_marketing': 120
            }
        def salvar_feedback(self, texto, tipo='geral', cliente_id=None, pontuacao=None):
            return True
        def get_analise_sentimento(self):
            return pd.DataFrame({
                'sentimento': ['positivo', 'neutro', 'negativo'],
                'quantidade': [15, 8, 5],
                'media_polaridade': [0.7, 0.1, -0.6]
            })
        def get_vendas_por_produto(self):
            return pd.DataFrame({
                'produto': ['Produto A', 'Produto B', 'Produto C'],
                'total_vendas': [75000, 50000, 25000]
            })
    
    class IAGenerativa:
        def processar_pergunta(self, pergunta, dados):
            return "🤖 Modo simulação ativado. Configure o banco de dados para respostas completas."

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
    .stAlert {
        border-radius: 10px;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .chat-user {
        background-color: #E3F2FD;
        border-left: 4px solid #2196F3;
    }
    .chat-assistant {
        background-color: #F3E5F5;
        border-left: 4px solid #9C27B0;
    }
</style>
""", unsafe_allow_html=True)

class CogitaraApp:
    def __init__(self):
        if DB_LOADED:
            self.db = DatabaseCogitara()
        else:
            self.db = DatabaseCogitara()
        
        self.ia = IAGenerativa()
    
    def dashboard_principal(self):
        st.markdown('<h1 class="main-header">🚀 COGITARA IA</h1>', unsafe_allow_html=True)
        st.markdown("**Do dado à decisão, com visão e precisão**")
        
        # Carregar métricas
        metricas = self.db.get_metricas_principais()
        
        # Métricas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📊 Vendas (30 dias)", f"R$ {metricas['total_vendas']:,.0f}",
                     delta=f"{metricas['num_vendas']} vendas")
        
        with col2:
            st.metric("👥 Clientes Ativos", f"{metricas['total_clientes']}",
                     delta="5 novos")
        
        with col3:
            st.metric("😊 Satisfação Média", f"{metricas['satisfacao_media']:.1f}/5.0",
                     delta="0.2")
        
        with col4:
            st.metric("📢 Marketing", f"R$ {metricas['investimento_marketing']:,.0f}",
                     delta=f"{metricas['conversoes_marketing']} conversões")
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de vendas por produto
            vendas_produto = self.db.get_vendas_por_produto()
            fig = px.bar(vendas_produto, x='produto', y='total_vendas', 
                        title='📦 Vendas por Produto', color='produto')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Gráfico de sentimentos
            sentimentos = self.db.get_analise_sentimento()
            fig = px.pie(sentimentos, values='quantidade', names='sentimento',
                        title='😊 Análise de Sentimento dos Clientes')
            st.plotly_chart(fig, use_container_width=True)
        
        # Status do sistema
        if not DB_LOADED:
            st.warning("🔧 Sistema em modo simulação - Algumas funcionalidades podem estar limitadas")

    def analise_preditiva(self):
        st.header("🔮 Análise Preditiva")
        
        if not DB_LOADED:
            st.info("📊 Modo demonstração - Conecte o banco de dados para análise completa")
        
        # Simulação de previsão
        meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun']
        historico = [120, 135, 148, 160, 175, 190]
        previsao = [190, 205, 220, 238, 255, 275]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=meses, y=historico, name='Histórico', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=meses, y=previsao, name='Previsão', line=dict(color='red', dash='dash')))
        
        fig.update_layout(title='Previsão de Vendas - Próximos 6 Meses')
        st.plotly_chart(fig)
        
        # Métricas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Crescimento Esperado", "15%")
        with col2:
            st.metric("Confiança da Previsão", "87%")
        with col3:
            st.metric("Melhor Produto", "Produto A")

    def simulador_cenarios(self):
        st.header("🎯 Simulador de Cenários 'E se...?'")
        
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
        
        from textblob import TextBlob
        
        # Análise de texto
        feedback = st.text_area("Digite o feedback do cliente:", 
                               "Produto excelente, entrega rápida e atendimento perfeito!")
        
        if st.button("Analisar Sentimento"):
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
            
            # Salvar no banco se disponível
            if DB_LOADED:
                try:
                    self.db.salvar_feedback(feedback, 'geral')
                    st.success("✅ Feedback salvo no banco de dados!")
                except:
                    st.info("💾 Banco de dados não disponível para salvar")
        
        # Análise consolidada
        st.subheader("📊 Análise Consolidada")
        sentimentos = self.db.get_analise_sentimento()
        
        if not sentimentos.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.pie(sentimentos, values='quantidade', names='sentimento',
                            title='Distribuição de Sentimentos')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.bar(sentimentos, x='sentimento', y='media_polaridade',
                            title='Intensidade Média dos Sentimentos')
                st.plotly_chart(fig, use_container_width=True)

    def modulo_chat_ia(self):
        st.header("💬 Assistente COGITARA IA")
        st.markdown("**Converse comigo e eu analisarei seus dados em tempo real!**")
        
        # Inicializar session state para chat
        if 'mensagens' not in st.session_state:
            st.session_state.mensagens = []
        
        # Exibir histórico do chat
        for mensagem in st.session_state.mensagens:
            with st.chat_message(mensagem["role"]):
                st.markdown(mensagem["content"])
        
        # Input do usuário
        if prompt := st.chat_input("Pergunte sobre vendas, clientes, marketing..."):
            # Adicionar mensagem do usuário
            st.session_state.mensagens.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Gerar resposta da IA
            with st.chat_message("assistant"):
                with st.spinner("🤖 Analisando dados e gerando insights..."):
                    # Carregar dados contextuais
                    metricas = self.db.get_metricas_principais()
                    
                    # Processar pergunta
                    resposta = self.ia.processar_pergunta(prompt, metricas)
                    
                    # Exibir resposta
                    st.markdown(resposta)
            
            # Adicionar resposta ao histórico
            st.session_state.mensagens.append({"role": "assistant", "content": resposta})
        
        # Sidebar com exemplos de perguntas
        st.sidebar.markdown("---")
        st.sidebar.subheader("💡 Exemplos para perguntar:")
        
        exemplos = [
            "Como estão minhas vendas?",
            "Qual é o melhor produto?",
            "Previsão para os próximos meses",
            "Como melhorar o marketing?",
            "Problemas com clientes",
            "Sugestões para crescer"
        ]
        
        for exemplo in exemplos:
            if st.sidebar.button(f"\"{exemplo}\"", key=exemplo):
                # Simular input do usuário
                st.session_state.mensagens.append({"role": "user", "content": exemplo})
                with st.chat_message("user"):
                    st.markdown(exemplo)
                
                # Gerar resposta
                with st.chat_message("assistant"):
                    with st.spinner("🤖 Analisando..."):
                        metricas = self.db.get_metricas_principais()
                        resposta = self.ia.processar_pergunta(exemplo, metricas)
                        st.markdown(resposta)
                
                st.session_state.mensagens.append({"role": "assistant", "content": resposta})
                st.rerun()
        
        # Botão para limpar histórico
        if st.sidebar.button("🗑️ Limpar Conversa"):
            st.session_state.mensagens = []
            self.ia.limpar_historico()
            st.rerun()

    def run(self):
        # Sidebar
        st.sidebar.title("🎛️ Painel COGITARA")
        st.sidebar.markdown("---")
        
        pagina = st.sidebar.selectbox(
            "Selecione a página:",
            ["🏠 Dashboard", "🔮 Análise Preditiva", "🎯 Simulador", "😊 Análise de Sentimento", "💬 Chat IA"]
        )
        
        st.sidebar.markdown("---")
        
        if DB_LOADED and st.sidebar.button("🔄 Carregar Dados Exemplo"):
            self.db.inserir_dados_exemplo()
            st.sidebar.success("Dados carregados!")
        elif not DB_LOADED:
            st.sidebar.warning("⚡ Modo Demonstração")
        
        st.sidebar.info("""
        **COGITARA IA**
        - 🔮 Análise Preditiva
        - 🎯 Simulador de Cenários  
        - 😊 Análise de Sentimento
        - 💬 Chat com IA
        - 📊 Dashboard em Tempo Real
        """)
        
        # Navegação
        if pagina == "🏠 Dashboard":
            self.dashboard_principal()
        elif pagina == "🔮 Análise Preditiva":
            self.analise_preditiva()
        elif pagina == "🎯 Simulador":
            self.simulador_cenarios()
        elif pagina == "😊 Análise de Sentimento":
            self.analise_sentimento()
        elif pagina == "💬 Chat IA":
            self.modulo_chat_ia()

# Executar app
if __name__ == "__main__":
    app = CogitaraApp()
    app.run()
