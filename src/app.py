import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
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

# Simulação de banco de dados (sem SQLite para evitar problemas)
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

class IACogitara:
    def __init__(self):
        self.historico = []
    
    def processar_comando(self, comando):
        comando_lower = comando.lower()
        
        if any(palavra in comando_lower for palavra in ['dashboard', 'painel', 'resumo']):
            return self.gerar_dashboard()
        elif any(palavra in comando_lower for palavra in ['venda', 'faturamento']):
            return self.analisar_vendas()
        elif any(palavra in comando_lower for palavra in ['cliente', 'satisfação']):
            return self.analisar_clientes()
        elif any(palavra in comando_lower for palavra in ['marketing', 'campanha']):
            return self.analisar_marketing()
        elif any(palavra in comando_lower for palavra in ['previsão', 'futuro']):
            return self.gerar_previsao()
        elif any(palavra in comando_lower for palavra in ['simular', 'cenário']):
            return self.simular_cenario()
        elif any(palavra in comando_lower for palavra in ['sentimento', 'feedback']):
            return self.analisar_sentimento()
        else:
            return self.resposta_geral()
    
    def gerar_dashboard(self):
        db = DatabaseSimulacao()
        metricas = db.get_metricas_principais()
        
        resposta = f"""
🎯 **DASHBOARD COGITARA IA**

📊 **MÉTRICAS PRINCIPAIS:**
• **Vendas**: R$ {metricas['total_vendas']:,.0f} ({metricas['num_vendas']} vendas)
• **Clientes**: {metricas['total_clientes']} ativos 
• **Satisfação**: {metricas['satisfacao_media']}/5.0 ⭐
• **Marketing**: R$ {metricas['investimento_marketing']:,.0f} investido

🚀 **STATUS**: Performance Excelente (+15% crescimento)

💡 **INSIGHTS:**
1. Produto A lidera com 54% do faturamento
2. Clientes recorrentes gastam 3x mais
3. Oportunidade em expandir campanhas digitais
"""
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            vendas_produto = db.get_vendas_por_produto()
            fig = px.bar(vendas_produto, x='produto', y='total_vendas', 
                        title='📦 Vendas por Produto', color='produto')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            sentimentos = db.get_analise_sentimento()
            fig = px.pie(sentimentos, values='quantidade', names='sentimento',
                        title='😊 Análise de Sentimento')
            st.plotly_chart(fig, use_container_width=True)
        
        return resposta
    
    def analisar_vendas(self):
        db = DatabaseSimulacao()
        metricas = db.get_metricas_principais()
        
        resposta = f"""
💰 **ANÁLISE DE VENDAS DETALHADA**

📈 **Performance:**
• Faturamento: R$ {metricas['total_vendas']:,.0f}
• Crescimento: +15% vs mês anterior
• Vendas/Mês: {metricas['num_vendas']}

🎯 **Estratégias Recomendadas:**
• Aumentar estoque do Produto A
• Criar promoções cruzadas
• Focar em upsell com clientes existentes

📊 **Previsão Próximos 3 Meses:** +18% de crescimento
"""
        
        # Gráfico de tendência
        meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun']
        historico = [100, 120, 140, 152, 165, 180]
        previsao = [180, 195, 210, 225, 240, 255]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=meses, y=historico, name='Histórico', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=meses, y=previsao, name='Previsão', line=dict(color='red', dash='dash')))
        fig.update_layout(title='📈 Tendência de Vendas')
        st.plotly_chart(fig, use_container_width=True)
        
        return resposta
    
    def analisar_clientes(self):
        resposta = """
👥 **ANÁLISE DE CLIENTES**

📊 **Métricas:**
• Clientes Ativos: 247
• Satisfação: 4.3/5.0 ⭐
• Taxa de Retenção: 89%
• Novos Clientes/Mês: +12

🎯 **Estratégias:**
• Programa de fidelidade
• Conteúdo exclusivo
• Atendimento premium
"""
        return resposta
    
    def analisar_marketing(self):
        resposta = """
📢 **ANÁLISE DE MARKETING**

💰 **Performance:**
• Investimento: R$ 52.000
• ROI: 3.4 (Excelente)
• Custo por Aquisição: R$ 416

🎯 **Canais:**
1. Email Marketing: ROI 5.9
2. Google Ads: ROI 4.2  
3. Redes Sociais: ROI 2.4
"""
        return resposta
    
    def gerar_previsao(self):
        resposta = """
🔮 **PREVISÕES INTELIGENTES**

📈 **Próximos 6 Meses:**
• Mês 1: +12% crescimento
• Mês 2: +10% crescimento  
• Mês 3: +9% crescimento
• Mês 4: +8% crescimento
• Mês 5: +7% crescimento
• Mês 6: +6% crescimento

🎯 **Confiança**: 85%
"""
        return resposta
    
    def simular_cenario(self):
        resposta = """
🎯 **SIMULAÇÃO DE CENÁRIOS**

📊 **Cenário 1: +20% Marketing**
• Investimento: +R$ 10.400
• Retorno: +R$ 35.360
• ROI: 3.4
• ✅ RECOMENDADO

📊 **Cenário 2: -10% Preço**
• Volume: +25%
• Lucro: +R$ 9.200
• ✅ VIÁVEL

💡 **Experimente o simulador interativo abaixo!**
"""
        
        # Simulador interativo
        st.subheader("🔄 Simulador Interativo")
        col1, col2 = st.columns(2)
        
        with col1:
            investimento = st.slider("Investimento Extra (R$)", 0, 20000, 5000)
            variacao_preco = st.slider("Variação Preço (%)", -20, 20, 0)
        
        with col2:
            impacto = variacao_preco * -0.5 + (investimento/5000) * 6
            novas_vendas = 152000 * (1 + impacto/100)
            st.metric("Vendas Projetadas", f"R$ {novas_vendas:,.0f}")
        
        return resposta
    
    def analisar_sentimento(self):
        resposta = """
😊 **ANÁLISE DE SENTIMENTO**

📊 **Distribuição:**
• 😊 Positivo: 18 feedbacks
• 😐 Neutro: 9 feedbacks  
• 😡 Negativo: 4 feedbacks

⭐ **Satisfação**: 4.3/5.0

🎯 **Ações:**
• Implementar chatbot 24/7
• Programa de fidelidade
• Pesquisas mensais
"""
        return resposta
    
    def resposta_geral(self):
        resposta = """
🤖 **COGITARA IA - Seu Assistente Inteligente**

Olá! Sou especialista em análise de dados e estratégia de negócios.

🎯 **Posso ajudar com:**
• 📊 Análise de vendas e métricas
• 🔮 Previsões inteligentes  
• 🎯 Simulação de cenários
• 😊 Análise de sentimentos
• 💡 Sugestões estratégicas

💬 **Experimente comandos como:**
"Mostre meu dashboard"
"Analise minhas vendas" 
"Faça uma previsão"
"Simule um cenário"

**Vamos transformar dados em decisões!** 🚀
"""
        return resposta

class CogitaraApp:
    def __init__(self):
        self.db = DatabaseSimulacao()
        self.ia = IACogitara()
        self.db.carregar_dados_exemplo()
    
    def pagina_principal(self):
        st.markdown('<h1 class="main-header">🧠 COGITARA IA</h1>', unsafe_allow_html=True)
        st.markdown("**Do dado à decisão, com visão e precisão**")
        
        # Inicializar chat
        if 'mensagens' not in st.session_state:
            st.session_state.mensagens = [{
                "role": "assistant", 
                "content": self.ia.resposta_geral()
            }]
        
        # Mostrar histórico
        for mensagem in st.session_state.mensagens:
            with st.chat_message(mensagem["role"]):
                st.markdown(mensagem["content"])
        
        # Input do usuário
        if prompt := st.chat_input("Digite seu comando..."):
            st.session_state.mensagens.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("🤖 Analisando..."):
                    resposta = self.ia.processar_comando(prompt)
                    st.markdown(resposta)
            
            st.session_state.mensagens.append({"role": "assistant", "content": resposta})
        
        # Comandos rápidos
        st.sidebar.markdown("---")
        st.sidebar.subheader("🚀 Comandos Rápidos")
        
        comandos = [
            "📊 Dashboard Completo",
            "💰 Análise de Vendas", 
            "👥 Análise de Clientes",
            "📢 Análise de Marketing",
            "🔮 Previsões",
            "🎯 Simular Cenários",
            "😊 Análise de Sentimento"
        ]
        
        for comando in comandos:
            if st.sidebar.button(comando):
                texto_comando = comando.split(' ', 1)[1]
                st.session_state.mensagens.append({"role": "user", "content": texto_comando})
                with st.chat_message("user"):
                    st.markdown(texto_comando)
                
                with st.chat_message("assistant"):
                    with st.spinner("🤖 Processando..."):
                        resposta = self.ia.processar_comando(texto_comando)
                        st.markdown(resposta)
                
                st.session_state.mensagens.append({"role": "assistant", "content": resposta})
                st.rerun()
        
        if st.sidebar.button("🗑️ Limpar Conversa"):
            st.session_state.mensagens = [{
                "role": "assistant", 
                "content": "Conversa reiniciada! Como posso ajudar? 🚀"
            }]
            st.rerun()

    def run(self):
        st.sidebar.title("🎛️ COGITARA IA")
        st.sidebar.markdown("---")
        self.pagina_principal()
        st.sidebar.markdown("---")
        st.sidebar.info("""
        **🧠 COGITARA IA**
        - Análise Preditiva
        - Simulação de Cenários  
        - Análise de Sentimento
        - Dashboard Inteligente
        """)

if __name__ == "__main__":
    app = CogitaraApp()
    app.run()
