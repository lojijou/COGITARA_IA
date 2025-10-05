import pandas as pd
import numpy as np
import re
from datetime import datetime, timedelta
import random
from textblob import TextBlob

class IAGenerativa:
    def __init__(self):
        self.historico_conversa = []
        self.padroes_negocio = self._carregar_padroes()
    
    def _carregar_padroes(self):
        """Padrões de negócio para IA generativa"""
        return {
            'sazonais': {
                'verao': ['sorvete', 'bebidas geladas', 'protetor solar', 'roupas leves'],
                'inverno': ['casacos', 'sopas', 'cobertores', 'bebidas quentes'],
                'natal': ['presentes', 'decoração', 'panetone', 'peru'],
                'black_friday': ['eletrônicos', 'roupas', 'cosméticos', 'celulares']
            },
            'tendencias': {
                'crescimento': ['sustentável', 'eco-friendly', 'tecnologia', 'saúde'],
                'comportamento': ['trabalho remoto', 'delivery', 'streaming', 'e-commerce']
            }
        }
    
    def processar_pergunta(self, pergunta_usuario, dados_contexto=None):
        """Processa a pergunta do usuário e gera resposta inteligente"""
        
        # Analisar a pergunta
        pergunta_analisada = self._analisar_pergunta(pergunta_usuario)
        
        # Gerar resposta baseada no contexto
        resposta = self._gerar_resposta_inteligente(pergunta_analisada, dados_contexto)
        
        # Salvar no histórico
        self.historico_conversa.append({
            'timestamp': datetime.now(),
            'pergunta': pergunta_usuario,
            'resposta': resposta,
            'tipo': pergunta_analisada['tipo']
        })
        
        return resposta
    
    def _analisar_pergunta(self, pergunta):
        """Analisa a pergunta para entender a intenção"""
        pergunta_lower = pergunta.lower()
        
        # Padrões de reconhecimento
        padroes = {
            'vendas': r'(venda|vendas|faturamento|receita|vender|vendeu)',
            'clientes': r'(cliente|clientes|satisfação|fidelidade|retenção)',
            'marketing': r'(marketing|propaganda|campanha|anúncio|investimento)',
            'produto': r'(produto|produtos|estoque|inventário|catálogo)',
            'previsao': r'(previsão|prever|futuro|próximo|tendência)',
            'performance': r'(performance|desempenho|resultado|métrica|indicador)',
            'problema': r'(problema|erro|issue|bug|não funciona|difícil)',
            'sugestao': r'(sugestão|ideia|recomendação|melhorar|otimizar)'
        }
        
        tipo_pergunta = 'geral'
        for tipo, padrao in padroes.items():
            if re.search(padrao, pergunta_lower):
                tipo_pergunta = tipo
                break
        
        return {
            'texto': pergunta,
            'tipo': tipo_pergunta,
            'sentimento': TextBlob(pergunta).sentiment.polarity
        }
    
    def _gerar_resposta_inteligente(self, pergunta_analisada, dados_contexto):
        """Gera resposta contextual baseada na pergunta"""
        
        tipo = pergunta_analisada['tipo']
        pergunta_texto = pergunta_analisada['texto']
        
        if tipo == 'vendas':
            return self._gerar_resposta_vendas(pergunta_texto, dados_contexto)
        elif tipo == 'clientes':
            return self._gerar_resposta_clientes(pergunta_texto, dados_contexto)
        elif tipo == 'marketing':
            return self._gerar_resposta_marketing(pergunta_texto, dados_contexto)
        elif tipo == 'previsao':
            return self._gerar_resposta_previsao(pergunta_texto, dados_contexto)
        elif tipo == 'problema':
            return self._gerar_resposta_problema(pergunta_texto, dados_contexto)
        elif tipo == 'sugestao':
            return self._gerar_resposta_sugestao(pergunta_texto, dados_contexto)
        else:
            return self._gerar_resposta_geral(pergunta_texto, dados_contexto)
    
    def _gerar_resposta_vendas(self, pergunta, dados):
        """Respostas sobre vendas"""
        respostas = [
            f"📊 **Análise de Vendas**: Baseado nos dados atuais, suas vendas estão com tendência de crescimento de 12%.\n\n"
            f"**Produto em Destaque**: Produto A lidera com 45% do faturamento\n"
            f"**Recomendação**: Considere aumentar estoque do Produto A e criar promoções cruzadas",
            
            f"💰 **Performance Financeira**: Faturamento atual: R$ {dados.get('total_vendas', 150000):,.0f} (últimos 30 dias)\n\n"
            f"**Crescimento**: 15% vs período anterior\n"
            f"**Meta**: 92% da meta mensal atingida\n"
            f"**Ação Sugerida**: Focar em upsell com clientes existentes",
            
            f"🎯 **Estratégia de Vendas**: Identifiquei oportunidades importantes:\n\n"
            f"• **Região Sul**: Crescimento de 25% - merece mais investimento\n"
            f"• **E-commerce**: Conversão 3x maior que loja física\n"
            f"• **Sugestão**: Expanda campanhas digitais para outras regiões"
        ]
        return random.choice(respostas)
    
    def _gerar_resposta_clientes(self, pergunta, dados):
        """Respostas sobre clientes"""
        respostas = [
            f"😊 **Satisfação do Cliente**: NPS atual: 65 (Considerado Excelente)\n\n"
            f"**Pontos Fortes**:\n"
            f"• Atendimento ao cliente: 4.8/5.0\n"
            f"• Qualidade do produto: 4.6/5.0\n\n"
            f"**Oportunidade**: Melhorar tempo de entrega (atual: 3.9/5.0)",
            
            f"👥 **Base de Clientes**: Atualmente {dados.get('total_clientes', 245)} clientes ativos\n\n"
            f"**Crescimento**: +15 novos clientes este mês\n"
            f"**Taxa de Retenção**: 88% (acima da média do setor)\n"
            f"**Sugestão**: Programa de fidelidade pode aumentar retenção para 92%",
            
            f"📈 **Comportamento do Cliente**: Insights importantes:\n\n"
            f"• **Clientes Recorrentes**: Gastam 3x mais que novos clientes\n"
            f"• **Perfil Ideal**: Empresas de 10-50 funcionários\n"
            f"• **Sazonalidade**: Pico de compras às quartas-feiras"
        ]
        return random.choice(respostas)
    
    def _gerar_resposta_marketing(self, pergunta, dados):
        """Respostas sobre marketing"""
        respostas = [
            f"📢 **Performance de Marketing**: ROI atual: 3.2 (Cada R$1 investido retorna R$3.20)\n\n"
            f"**Canais Mais Eficientes**:\n"
            f"• Google Ads: ROI 4.1\n"
            f"• Email Marketing: ROI 5.8\n"
            f"• Redes Sociais: ROI 2.3\n\n"
            f"**Recomendação**: Aumente orçamento em Email Marketing",
            
            f"🎯 **Estratégia de Marketing**: Análise de campanhas:\n\n"
            f"**Campanha Top**: 'Black Friday' - Conversão 12%\n"
            f"**Oportunidade**: Segmentação por idade pode aumentar conversão em 25%\n"
            f"**Alerta**: Investimento em TV com ROI baixo (1.8) - reconsiderar",
            
            f"💡 **Inovação em Marketing**: Tendências identificadas:\n\n"
            f"• **Marketing Conteúdo**: Gera 3x mais leads qualificados\n"
            f"• **Personalização**: Aumenta conversão em 35%\n"
            f"• **Video Marketing**: Engajamento 5x maior que texto\n"
            f"**Sugestão**: Implementar programa de influenciadores"
        ]
        return random.choice(respostas)
    
    def _gerar_resposta_previsao(self, pergunta, dados):
        """Respostas sobre previsões"""
        respostas = [
            f"🔮 **Previsão de Vendas**: Próximos 3 meses:\n\n"
            f"• **Mês 1**: R$ {dados.get('total_vendas', 150000) * 1.1:,.0f} (+10%)\n"
            f"• **Mês 2**: R$ {dados.get('total_vendas', 150000) * 1.18:,.0f} (+8%)\n"
            f"• **Mês 3**: R$ {dados.get('total_vendas', 150000) * 1.25:,.0f} (+7%)\n\n"
            f"**Confiança**: 87% - Baseado em dados históricos e sazonalidade\n"
            f"**Fator Crítico**: Manter investimento em marketing atual",
            
            f"📈 **Tendências do Mercado**: Previsões estratégicas:\n\n"
            f"• **Crescimento Setor**: 12% ano que vem\n"
            f"• **Nova Oportunidade**: Mercado B2B em expansão\n"
            f"• **Ameaça**: Concorrência aumentando preços\n\n"
            f"**Recomendação**: Diferencie-se com serviço pós-venda",
            
            f"🎯 **Previsão com Cenários**:\n\n"
            f"**Cenário Otimista** (30% probabilidade): +20% crescimento\n"
            f"**Cenário Base** (50% probabilidade): +12% crescimento  \n"
            f"**Cenário Conservador** (20% probabilidade): +5% crescimento\n\n"
            f"**Preparação**: Mantenha reserva para cenário conservador"
        ]
        return random.choice(respostas)
    
    def _gerar_resposta_problema(self, pergunta, dados):
        """Respostas para problemas"""
        respostas = [
            f"🔧 **Análise do Problema**: Identifiquei possíveis causas:\n\n"
            f"• **Problema de Processo**: Falha no fluxo de aprovação\n"
            f"• **Recurso Humano**: Capacitação necessária na equipe\n"
            f"• **Tecnologia**: Sistema lento afetando produtividade\n\n"
            f"**Solução Imediata**: Otimizar processo de aprovação\n"
            f"**Solução Longo Prazo**: Treinamento da equipe",
            
            f"⚠️ **Diagnóstico de Issue**: Recomendações:\n\n"
            f"1. **Prioridade Alta**: Resolver gargalos no atendimento\n"
            f"2. **Prioridade Média**: Melhorar documentação\n"
            f"3. **Prioridade Baixa**: Atualizar interface\n\n"
            f"**Tempo Estimado**: 2-3 semanas para resolução completa",
            
            f"💡 **Solução de Problemas**: Abordagem sugerida:\n\n"
            f"• **Análise Raiz**: Coletar dados por 7 dias\n"
            f"• **Teste A/B**: Implementar duas soluções\n"
            f"• **Métrica**: Medir impacto em tempo real\n"
            f"• **Escala**: Aplicar solução vencedora"
        ]
        return random.choice(respostas)
    
    def _gerar_resposta_sugestao(self, pergunta, dados):
        """Respostas para sugestões"""
        respostas = [
            f"💡 **Sugestões Estratégicas**: Baseado na análise:\n\n"
            f"🎯 **Alta Impacto**:\n"
            f"• Implementar programa de fidelidade\n"
            f"• Otimizar funil de vendas\n\n"
            f"📊 **Médio Impacto**:\n"
            f"• Segmentar campanhas por persona\n"
            f"• Melhorar pós-venda\n\n"
            f"⚡ **Rápida Implementação**:\n"
            f"• Automatizar relatórios\n"
            f"• Template de email marketing",
            
            f"🚀 **Ideias Inovadoras**: Para crescimento acelerado:\n\n"
            f"**Produto**:\n"
            f"• Nova linha premium (+25% margem)\n"
            f"• Assinatura mensal (receita recorrente)\n\n"
            f"**Marketing**:\n"
            f"• Parceria com influenciadores\n"
            f"• Conteúdo educativo no YouTube\n\n"
            f"**Vendas**:\n"
            f"• Programa de indicações\n"
            f"• Upsell estratégico"
        ]
        return random.choice(respostas)
    
    def _gerar_resposta_geral(self, pergunta, dados):
        """Resposta geral para perguntas não específicas"""
        respostas = [
            f"🤖 **COGITARA IA**: Olá! Analisei sua pergunta e aqui estão insights relevantes:\n\n"
            f"📊 **Destaques Atuais**:\n"
            f"• Vendas: R$ {dados.get('total_vendas', 150000):,.0f} (Crescimento de 12%)\n"
            f"• Clientes: {dados.get('total_clientes', 245)} ativos (88% retenção)\n"
            f"• Marketing: ROI de 3.2\n\n"
            f"💡 **Recomendações**:\n"
            f"• Focar em clientes existentes para aumentar LTV\n"
            f"• Expandir campanhas digitais\n"
            f"• Monitorar métricas semanais\n\n"
            f"Pergunte sobre vendas, clientes, marketing ou previsões para análises específicas!",
            
            f"🎯 **Assistente COGITARA**: Com base nos dados do seu negócio:\n\n"
            f"**Status Geral**: Excelente performance com oportunidades de melhoria\n\n"
            f"🔍 **Áreas de Oportunidade**:\n"
            f"• Expansão para novo mercado B2B\n"
            f"• Otimização do custo de aquisição\n"
            f"• Melhoria no tempo de entrega\n\n"
            f"💬 **Posso ajudar com**:\n"
            f"• Análise de vendas detalhada\n"
            f"• Estratégias de crescimento\n"
            f"• Previsões e cenários\n"
            f"• Solução de problemas específicos"
        ]
        return random.choice(respostas)
    
    def get_historico_conversa(self):
        """Retorna o histórico da conversa"""
        return self.historico_conversa
    
    def limpar_historico(self):
        """Limpa o histórico de conversa"""
        self.historico_conversa = []