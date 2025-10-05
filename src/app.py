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
import random

# Configuração de caminhos
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    from database import DatabaseCogitara
    DB_LOADED = True
except ImportError as e:
    st.error(f"❌ Erro ao carregar módulos: {e}")
    DB_LOADED = False
    
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
    .ia-response {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class IACogitaraAvancada:
    def __init__(self, db):
        self.db = db
        self.historico = []
        self.contexto_usuario = {}
    
    def processar_comando(self, comando):
        """Processa qualquer comando do usuário e executa ações"""
        comando_lower = comando.lower()
        
        # Análise de intenção
        if any(palavra in comando_lower for palavra in ['dashboard', 'painel', 'métricas', 'resumo']):
            return self.gerar_dashboard()
        
        elif any(palavra in comando_lower for palavra in ['venda', 'vendas', 'faturamento', 'receita']):
            return self.analisar_vendas(comando)
        
        elif any(palavra in comando_lower for palavra in ['cliente', 'clientes', 'satisfação', 'nps']):
            return self.analisar_clientes(comando)
        
        elif any(palavra in comando_lower for palavra in ['marketing', 'campanha', 'anúncio', 'investimento']):
            return self.analisar_marketing(comando)
        
        elif any(palavra in comando_lower for palavra in ['previsão', 'prever', 'futuro', 'tendência']):
            return self.gerar_previsao(comando)
        
        elif any(palavra in comando_lower for palavra in ['simular', 'cenário', 'e se', 'simulação']):
            return self.simular_cenario(comando)
        
        elif any(palavra in comando_lower for palavra in ['sentimento', 'feedback', 'opinião', 'reclamação']):
            return self.analisar_sentimento(comando)
        
        elif any(palavra in comando_lower for palavra in ['problema', 'erro', 'issue', 'bug']):
            return self.resolver_problema(comando)
        
        elif any(palavra in comando_lower for palavra in ['sugestão', 'ideia', 'recomendação', 'melhorar']):
            return self.gerar_sugestoes(comando)
        
        else:
            return self.resposta_geral(comando)
    
    def gerar_dashboard(self):
        """Gera dashboard completo"""
        metricas = self.db.get_metricas_principais()
        
        resposta = f"""
🎯 **DASHBOARD COGITARA IA - RESUMO EXECUTIVO**

📊 **MÉTRICAS PRINCIPAIS:**
• **Vendas**: R$ {metricas['total_vendas']:,.0f} ({metricas['num_vendas']} vendas)
• **Clientes**: {metricas['total_clientes']} ativos 
• **Satisfação**: {metricas['satisfacao_media']}/5.0 ⭐
• **Marketing**: R$ {metricas['investimento_marketing']:,.0f} investido

🚀 **STATUS GERAL:** Performance Excelente com crescimento de 12%

💡 **INSIGHTS IMEDIATOS:**
1. Produto A representa 45% do faturamento
2. Região Sul com crescimento de 25%
3. Oportunidade em expandir campanhas digitais

📈 **PRÓXIMOS PASSOS RECOMENDADOS:**
• Aumentar estoque do Produto A
• Expandir para mercado B2B
• Otimizar custo de aquisição
"""
        
        # Adicionar gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            vendas_produto = self.db.get_vendas_por_produto()
            fig = px.bar(vendas_produto, x='produto', y='total_vendas', 
                        title='📦 Vendas por Produto', color='produto')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            sentimentos = self.db.get_analise_sentimento()
            fig = px.pie(sentimentos, values='quantidade', names='sentimento',
                        title='😊 Análise de Sentimento')
            st.plotly_chart(fig, use_container_width=True)
        
        return resposta
    
    def analisar_vendas(self, comando):
        """Análise avançada de vendas"""
        metricas = self.db.get_metricas_principais()
        vendas_produto = self.db.get_vendas_por_produto()
        
        melhor_produto = vendas_produto.iloc[0]['produto']
        pior_produto = vendas_produto.iloc[-1]['produto']
        
        resposta = f"""
💰 **ANÁLISE DETALHADA DE VENDAS**

📈 **Performance:**
• Faturamento Total: R$ {metricas['total_vendas']:,.0f}
• Número de Vendas: {metricas['num_vendas']}
• Crescimento vs Mês Anterior: +12%

🏆 **Ranking de Produtos:**
1. **{melhor_produto}**: Líder em faturamento
2. **{vendas_produto.iloc[1]['produto']}**: Performance estável  
3. **{pior_produto}**: Necessita atenção

🎯 **Estratégias Recomendadas:**
• **Para {melhor_produto}**: Aumentar produção e criar bundles
• **Para {pior_produto}**: Reposicionamento ou promoções
• **Geral**: Focar em upsell com clientes existentes

📊 **Previsão Próximos 3 Meses:** +15% de crescimento
"""
        
        # Gráfico de tendência
        meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun']
        historico = [100, 120, 135, 148, 160, 175]
        previsao = [175, 190, 205, 220, 238, 255]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=meses, y=historico, name='Histórico', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=meses, y=previsao, name='Previsão', line=dict(color='red', dash='dash')))
        fig.update_layout(title='📈 Tendência de Vendas - Próximos 6 Meses')
        st.plotly_chart(fig, use_container_width=True)
        
        return resposta
    
    def analisar_clientes(self, comando):
        """Análise completa de clientes"""
        metricas = self.db.get_metricas_principais()
        
        resposta = f"""
👥 **ANÁLISE COMPLETA DA BASE DE CLIENTES**

📊 **Métricas Principais:**
• **Total de Clientes**: {metricas['total_clientes']} ativos
• **Satisfação Média**: {metricas['satisfacao_media']}/5.0
• **Taxa de Retenção**: 88% (Excelente)
• **Novos Clientes/Mês**: +15

😊 **Perfil do Cliente Ideal:**
• Empresas de 10-50 funcionários
• Setor: Tecnologia e Serviços
• Ticket Médio: R$ 2.500
• Frequência de Compra: Mensal

🎯 **Estratégias de Fidelização:**
1. Programa de recompensas para clientes recorrentes
2. Conteúdo exclusivo para clientes premium  
3. Atendimento personalizado 24/7
4. Pesquisa de satisfação contínua

💡 **Oportunidades Identificadas:**
• Upsell: 35% dos clientes podem migrar para plano superior
• Cross-sell: Produto B tem alta aceitação entre clientes atuais
"""
        return resposta
    
    def analisar_marketing(self, comando):
        """Análise de performance de marketing"""
        metricas = self.db.get_metricas_principais()
        
        resposta = f"""
📢 **ANÁLISE DE PERFORMANCE DE MARKETING**

💰 **Investimento e Retorno:**
• Total Investido: R$ {metricas['investimento_marketing']:,.0f}
• Conversões: {metricas['conversoes_marketing']}
• ROI: 3.2 (Cada R$1 retorna R$3.20)
• Custo por Aquisição: R$ 420

🏆 **Canais por Performance:**
1. **Email Marketing**: ROI 5.8 (Excelente)
2. **Google Ads**: ROI 4.1 (Bom)
3. **Redes Sociais**: ROI 2.3 (Regular)
4. **TV/Rádio**: ROI 1.8 (Revisar)

🎯 **Recomendações Estratégicas:**
• **Aumentar**: Orçamento em Email Marketing (+30%)
• **Otimizar**: Campanhas em Redes Sociais
• **Reduzir**: Investimento em TV/Rádio
• **Testar**: Novos canais como TikTok e Podcasts

📈 **Campanhas em Destaque:**
• "Black Friday": Conversão de 12%
• "Loyalty Program": Retenção de 92%
• "Webinar Series**: 45% de leads qualificados
"""
        return resposta
    
    def gerar_previsao(self, comando):
        """Gera previsões inteligentes"""
        metricas = self.db.get_metricas_principais()
        
        resposta = f"""
🔮 **PREVISÕES INTELIGENTES COGITARA IA**

📈 **Previsão de Vendas (Próximos 6 Meses):**
• Mês 1: R$ {metricas['total_vendas'] * 1.1:,.0f} (+10%)
• Mês 2: R$ {metricas['total_vendas'] * 1.18:,.0f} (+8%)  
• Mês 3: R$ {metricas['total_vendas'] * 1.25:,.0f} (+7%)
• Mês 4: R$ {metricas['total_vendas'] * 1.31:,.0f} (+6%)
• Mês 5: R$ {metricas['total_vendas'] * 1.36:,.0f} (+5%)
• Mês 6: R$ {metricas['total_vendas'] * 1.4:,.0f} (+4%)

🎯 **Confiança das Previsões:** 87%

⚠️ **Fatores de Risco Monitorados:**
• Concorrência aumentando preços
• Sazonalidade do setor
• Condições econômicas
• Comportamento do consumidor

💡 **Recomendações Baseadas na Previsão:**
1. Aumentar capacidade de produção em 15%
2. Estocar materiais para pico de demanda
3. Contratar equipe adicional para suporte
4. Desenvolver nova linha de produtos
"""
        return resposta
    
    def simular_cenario(self, comando):
        """Simula cenários complexos"""
        resposta = """
🎯 **SIMULADOR DE CENÁRIOS AVANÇADO**

Vou simular diferentes cenários para seu negócio:

📊 **Cenário 1: Aumento de 20% no Marketing**
• Investimento Adicional: R$ 10.000
• Vendas Adicionais: R$ 32.000
• ROI Esperado: 3.2
• **Recomendação**: ✅ ALTAMENTE RECOMENDADO

📊 **Cenário 2: Redução de 10% no Preço**
• Perda de Margem: R$ 15.000
• Aumento Volume: +25%
• Lucro Líquido: +R$ 8.500
• **Recomendação**: ✅ VIÁVEL

📊 **Cenário 3: Expansão para Nova Região**
• Investimento Inicial: R$ 50.000
• Retorno em 6 Meses: R$ 75.000
• ROI em 1 Ano: 2.5
• **Recomendação**: ⚠️ AVALIAR COM CAUTELA

📊 **Cenário 4: Novo Produto no Portfólio**
• Desenvolvimento: R$ 30.000
• Faturamento Anual: R$ 120.000
• Payback: 3 meses
• **Recomendação**: ✅ EXCELENTE OPORTUNIDADE

🎯 **MELHOR CENÁRIO**: Cenário 4 + Cenário 1
• ROI Combinado: 4.8
• Retorno Total em 1 Ano: R$ 200.000+
"""
        
        # Interface de simulação interativa
        st.subheader("🔄 Simulador Interativo")
        
        col1, col2 = st.columns(2)
        
        with col1:
            investimento = st.slider("Investimento em Marketing (R$)", 0, 50000, 10000)
            variacao_preco = st.slider("Variação no Preço (%)", -20, 20, 0)
        
        with col2:
            # Cálculo automático
            impacto_vendas = variacao_preco * -0.5 + (investimento/10000) * 8
            novas_vendas = 100000 * (1 + impacto_vendas/100)
            
            st.metric("Vendas Projetadas", f"R$ {novas_vendas:,.0f}")
            st.metric("ROI Esperado", f"{(impacto_vendas/100 * 100000)/investimento:.1f}" if investimento > 0 else "N/A")
        
        return resposta
    
    def analisar_sentimento(self, comando):
        """Análise de sentimentos dos clientes"""
        sentimentos = self.db.get_analise_sentimento()
        
        resposta = f"""
😊 **ANÁLISE DE SENTIMENTO DOS CLIENTES**

📊 **Distribuição de Sentimentos:**
• 😊 **Positivo**: {sentimentos[sentimentos['sentimento']=='positivo']['quantidade'].iloc[0] if not sentimentos[sentimentos['sentimento']=='positivo'].empty else 0} feedbacks
• 😐 **Neutro**: {sentimentos[sentimentos['sentimento']=='neutro']['quantidade'].iloc[0] if not sentimentos[sentimentos['sentimento']=='neutro'].empty else 0} feedbacks  
• 😡 **Negativo**: {sentimentos[sentimentos['sentimento']=='negativo']['quantidade'].iloc[0] if not sentimentos[sentimentos['sentimento']=='negativo'].empty else 0} feedbacks

⭐ **Satisfação Geral**: 4.2/5.0

🏆 **Pontos Fortes (Clientes Amam):**
• Atendimento rápido e eficiente
• Qualidade dos produtos
• Prazo de entrega
• Suporte pós-venda

⚠️ **Áreas de Melhoria:**
• Processo de devolução
• Comunicação de atrasos
• Documentação dos produtos

🎯 **Ações Recomendadas:**
1. Implementar chatbot para suporte 24/7
2. Criar programa de fidelidade
3. Melhorar comunicação de status
4. Pesquisas de satisfação mensais
"""
        
        # Gráfico de sentimentos
        fig = px.pie(sentimentos, values='quantidade', names='sentimento',
                    title='Distribuição de Sentimentos dos Clientes')
        st.plotly_chart(fig, use_container_width=True)
        
        return resposta
    
    def resolver_problema(self, comando):
        """Solução inteligente de problemas"""
        resposta = """
🔧 **ASSISTENTE DE SOLUÇÃO DE PROBLEMAS**

Identifiquei possíveis soluções para seu desafio:

🔄 **Metodologia de Resolução:**
1. **Análise da Causa Raiz**: Coleta de dados por 7 dias
2. **Teste A/B**: Implementar múltiplas soluções
3. **Métrica de Sucesso**: Definir KPIs claros
4. **Escalabilidade**: Aplicar solução vencedora

💡 **Soluções Comuns Efetivas:**

📉 **Problema: Queda nas Vendas**
• Solução: Campanha de remarketing + programa de fidelidade
• Tempo: 2-3 semanas
• Eficácia: 85%

😠 **Problema: Insatisfação de Clientes**
• Solução: Programa de recuperação + pesquisa de satisfação
• Tempo: 1-2 semanas  
• Eficácia: 90%

💰 **Problema: Margens Baixas**
• Solução: Revisão de precificação + otimização de custos
• Tempo: 4-6 semanas
• Eficácia: 75%

🔄 **Problema: Processos Ineficientes**
• Solução: Automação + treinamento da equipe
• Tempo: 4-8 semanas
• Eficácia: 80%

🎯 **Próximos Passos:**
1. Me conte mais detalhes sobre o problema específico
2. Coletarei dados relevantes
3. Proponho solução personalizada
4. Acompanho implementação
"""
        return resposta
    
    def gerar_sugestoes(self, comando):
        """Gera sugestões estratégicas"""
        resposta = """
💡 **SUGESTÕES ESTRATÉGICAS COGITARA IA**

Baseado na análise dos seus dados, aqui estão minhas recomendações:

🚀 **OPORTUNIDADES DE ALTO IMPACTO:**

🎯 **Expansão de Mercado:**
• Lançar produto no mercado B2B (potencial: +40% faturamento)
• Expandir para região Nordeste (crescimento: +25%)
• Parcerias estratégicas com empresas complementares

📈 **Otimização de Vendas:**
• Implementar programa de indicações (ROI: 5.8)
• Upsell para clientes existentes (potencial: +30% ticket médio)
• Bundle de produtos (aumento conversão: +15%)

💰 **Eficiência Operacional:**
• Automação de relatórios (economia: 20h/mês)
• Otimização de estoque (redução custos: 15%)
• Sistema de atendimento inteligente

🎨 **Inovação e Diferenciação:**
• Nova linha de produtos premium (margem: +25%)
• Programa de assinatura (receita recorrente)
• Conteúdo educativo (autoridade de marca)

📊 **Priorização Recomendada:**
1. Programa de indicações (rápido implementação, alto ROI)
2. Otimização de estoque (redução imediata de custos)  
3. Expansão B2B (crescimento sustentável)
4. Nova linha premium (diferenciação no mercado)

💬 **Precisa de mais detalhes sobre alguma sugestão? É só perguntar!**
"""
        return resposta
    
    def resposta_geral(self, comando):
        """Resposta para comandos gerais"""
        respostas = [
            f"""
🤖 **COGITARA IA - Seu Assistente de Negócios Inteligente**

Olá! Sou a COGITARA IA, sua especialista em análise de dados e estratégia de negócios.

🎯 **O que posso fazer por você:**

• 📊 **Analisar suas métricas** de vendas, clientes e marketing
• 🔮 **Fazer previsões** inteligentes sobre o futuro do seu negócio  
• 🎯 **Simular cenários** e calcular ROI de decisões
• 😊 **Analisar sentimentos** e satisfação dos clientes
• 💡 **Gerar sugestões** estratégicas personalizadas
• 🔧 **Resolver problemas** com soluções baseadas em dados

💬 **Experimente me perguntar coisas como:**
"Como estão minhas vendas?"
"Quais são minhas maiores oportunidades?"
"Simule um aumento de 20% no marketing"
"Analise a satisfação dos meus clientes"
"Quais problemas preciso resolver?"

Estou aqui para transformar seus dados em decisões inteligentes! 🚀
""",
            f"""
🎯 **COGITARA IA - Do Dado à Decisão**

Vejo que você tem interesse em melhorar seu negócio! Deixe-me mostrar como posso ajudar:

📈 **Análise em Tempo Real:** Monitoro todas as suas métricas principais
🎯 **Recomendações Ações:** Sugiro o que fazer baseado em dados
🔮 **Previsão Inteligente:** Antecipe tendências e oportunidades
💡 **Insights Estratégicos:** Identifico o que outros não veem

🚀 **Vamos começar? Me diga sobre:**
- Seus objetivos atuais
- Desafios que está enfrentando  
- Métricas que mais importam
- Áreas que quer melhorar

**Exemplos de comandos:**
"Mostre meu dashboard completo"
"Analise minha performance de vendas"  
"Quais são meus principais problemas?"
"Simule abrir uma nova filial"

Estou pronta para ajudar! 💪
"""
        ]
        return random.choice(respostas)

class CogitaraApp:
    def __init__(self):
        if DB_LOADED:
            self.db = DatabaseCogitara()
        else:
            self.db = DatabaseCogitara()
        
        self.ia = IACogitaraAvancada(self.db)
    
    def pagina_principal_ia(self):
        """Página principal focada na IA"""
        st.markdown('<h1 class="main-header">🧠 COGITARA IA</h1>', unsafe_allow_html=True)
        st.markdown("**Seu assistente inteligente para decisões de negócio**")
        
        # Inicializar session state para chat
        if 'mensagens' not in st.session_state:
            # Mensagem de boas-vindas inicial
            st.session_state.mensagens = [
                {
                    "role": "assistant", 
                    "content": """
🤖 **COGITARA IA - Seu Assistente de Negócios Inteligente**

Olá! Sou a COGITARA IA, especialista em análise de dados e estratégia de negócios. 

🎯 **Posso ajudar você com:**

• 📊 **Análise completa** das suas métricas de negócio
• 🔮 **Previsões inteligentes** sobre vendas e crescimento  
• 🎯 **Simulação de cenários** e cálculo de ROI
• 😊 **Análise de sentimentos** dos clientes
• 💡 **Sugestões estratégicas** personalizadas
• 🔧 **Solução de problemas** com dados

💬 **Pergunte algo como:**
"Como estão minhas vendas?"
"Quais são minhas maiores oportunidades?" 
"Simule um aumento de 20% no marketing"
"Analise a satisfação dos meus clientes"

**Estou pronta para transformar seus dados em decisões inteligentes!** 🚀
"""
                }
            ]
        
        # Exibir histórico do chat
        for mensagem in st.session_state.mensagens:
            with st.chat_message(mensagem["role"]):
                st.markdown(mensagem["content"])
        
        # Input do usuário
        if prompt := st.chat_input("Digite seu comando ou pergunta..."):
            # Adicionar mensagem do usuário
            st.session_state.mensagens.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Gerar resposta da IA
            with st.chat_message("assistant"):
                with st.spinner("🤖 Analisando dados e gerando resposta..."):
                    # Processar comando com a IA avançada
                    resposta = self.ia.processar_comando(prompt)
                    
                    # Exibir resposta
                    st.markdown(resposta)
            
            # Adicionar resposta ao histórico
            st.session_state.mensagens.append({"role": "assistant", "content": resposta})
        
        # Sidebar com atalhos
        st.sidebar.markdown("---")
        st.sidebar.subheader("🚀 Comandos Rápidos")
        
        comandos_rapidos = [
            "📊 Mostrar dashboard completo",
            "💰 Analisar performance de vendas", 
            "👥 Ver análise de clientes",
            "📢 Review de marketing",
            "🔮 Fazer previsões",
            "🎯 Simular cenários",
            "😊 Analisar sentimentos",
            "💡 Gerar sugestões"
        ]
        
        for comando in comandos_rapidos:
            if st.sidebar.button(comando):
                comando_texto = comando.split(' ', 1)[1]  # Remove o emoji
                st.session_state.mensagens.append({"role": "user", "content": comando_texto})
                with st.chat_message("user"):
                    st.markdown(comando_texto)
                
                with st.chat_message("assistant"):
                    with st.spinner("🤖 Processando..."):
                        resposta = self.ia.processar_comando(comando_texto)
                        st.markdown(resposta)
                
                st.session_state.mensagens.append({"role": "assistant", "content": resposta})
                st.rerun()
        
        # Botão para limpar conversa
        if st.sidebar.button("🗑️ Limpar Conversa"):
            st.session_state.mensagens = [
                {
                    "role": "assistant", 
                    "content": "Conversa reiniciada! Como posso ajudar você hoje? 🚀"
                }
            ]
            st.rerun()

    def run(self):
        # Sidebar
        st.sidebar.title("🎛️ COGITARA IA")
        st.sidebar.markdown("---")
        
        # Sempre mostrar página da IA (única página agora)
        self.pagina_principal_ia()
        
        st.sidebar.markdown("---")
        
        if DB_LOADED and st.sidebar.button("🔄 Carregar Dados Exemplo"):
            self.db.inserir_dados_exemplo()
            st.sidebar.success("Dados de exemplo carregados!")
        
        st.sidebar.info("""
        **🧠 COGITARA IA**
        - Análise Preditiva Avançada
        - Simulação de Cenários
        - Análise de Sentimento  
        - Sugestões Estratégicas
        - Solução de Problemas
        - Dashboard Inteligente
        """)

# Executar app
if __name__ == "__main__":
    app = CogitaraApp()
    app.run()
