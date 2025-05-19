import streamlit as st
from google import genai
import os

# Configuração do Gemini API
gemini_api_key = os.getenv("GEM_API_KEY")
client = genai.Client(api_key=gemini_api_key)

# Função para limpar o estado do Streamlit
def limpar_estado():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

# Formato padrão do relatório empresarial
formato_padrao = """
Com base na transcrição da reunião interna, produza um relatório executivo estruturado com foco em:
    
1. Contexto da Reunião
   - Objetivo e pauta principal
   - Participantes relevantes e seus departamentos
   - Data e duração

2. Principais Tópicos Discutidos
   - Lista dos assuntos abordados em ordem de importância
   - Síntese de cada tópico (3-5 pontos chave por assunto)
   - Decisões tomadas ou pendentes

3. Action Items (Itens de Ação)
   - Tarefas definidas na reunião
   - Responsáveis por cada ação
   - Prazos estabelecidos
   - Recursos necessários

4. Indicadores e Métricas
   - Dados relevantes apresentados
   - Análise de desempenho quando aplicável
   - Metas e benchmarks discutidos

5. Próximos Passos
   - Planejamento para próximas reuniões
   - Follow-ups agendados
   - Pendências a serem resolvidas

Diretrizes:
- Mantenha linguagem profissional mas acessível
- Destaque decisões e ações em negrito
- Use marcadores para melhor legibilidade
- Inclua citações diretas quando forem críticas
- Seja conciso mas completo (3-5 páginas no máximo)
- Priorize informações acionáveis
- Identifique claramente donos de tarefas
"""

# Função principal do app
def main():
    st.title("📊 Relatorios de Reuniões Internas")
    st.markdown("""
    Transforme transcrições de reuniões em relatórios executivos estruturados.
    Cole a transcrição abaixo e clique em "Gerar Relatório".
    """)
    
    # Área para inserção do texto
    transcricao = st.text_area("Cole a transcrição da reunião:", height=300,
                             placeholder="Exemplo:\nJoana (RH): Precisamos contratar 5 devs até Q3...\nCarlos (TI): Temos budget para 3 senior e 2 plenos...")
    
    # Opções de análise
    st.sidebar.header("Personalização")
    formato_personalizado = st.sidebar.text_area("Estrutura do Relatório", value=formato_padrao, height=400)
    observacoes = st.sidebar.text_area("Informações Adicionais", 
                                     placeholder="Ex: Focar nos prazos do projeto X\nIgnorar discussões sobre o café novo", 
                                     height=150)
    
    if st.button("Gerar Relatório Executivo"):
        if not transcricao:
            st.warning("Por favor, cole a transcrição da reunião.")
        else:
            with st.spinner("Processando a transcrição..."):
                prompt = f"""
                Gere um relatório executivo em português para gestão empresarial com base nesta transcrição:
                
                {formato_personalizado}
                
                Transcrição da reunião:
                {transcricao}
                
                Observações:
                {observacoes}
                """
                
                try:
                    # Primeira versão do relatório
                    relatorio = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=[prompt]).text

                    # Análise complementar
                    relatorio_analitico = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=[f'''Analise este relatório de reunião e identifique:
                        
                        1. Potenciais riscos não explicitados
                        2. Oportunidades não exploradas
                        3. Dependências críticas entre departamentos
                        4. Sugestões para melhorar eficiência
                        
                        Relatório:
                        {relatorio}
                        ''']).text
                    
                    # Exibir resultados
                    st.success("Relatório gerado com sucesso!")
                    st.markdown("---")
                    st.subheader("📋 Relatório Executivo")
                    st.markdown(relatorio)
                    
                    st.subheader("🔍 Análise Estratégica")
                    st.markdown(relatorio_analitico)
                    
                    # Opção para baixar
                    st.download_button(
                        label="Baixar Relatório",
                        data=f"# Relatório de Reunião\n\n{relatorio}\n\n## Análise Estratégica\n\n{relatorio_analitico}",
                        file_name="relatorio_reuniao.md",
                        mime="text/markdown"
                    )
                    
                except Exception as e:
                    st.error(f"Erro ao gerar relatório: {str(e)}")

if __name__ == "__main__":
    main()
