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

# Função principal do app
def main():
    st.title("📝 Gerador de Relatórios de Entrevista")
    st.markdown("""
    Este aplicativo transforma transcrições de entrevistas em relatórios estruturados.
    Cole o texto da entrevista abaixo e clique em "Gerar Relatório".
    """)
    
    # Área para inserção do texto da entrevista
    entrevista = st.text_area("Cole o texto da entrevista aqui:", height=300,
                             placeholder="Exemplo:\nEntrevistador: Qual seu principal desafio?\nEntrevistado: Nosso maior problema é...")
    
    # Opções de análise
    st.sidebar.header("Opções de Análise")
    nivel_detalhe = st.sidebar.selectbox("Nível de detalhe:", ["Resumido", "Detalhado", "Extremamente detalhado"])
    incluir_sumario = st.sidebar.checkbox("Incluir resumo executivo", value=True)
    incluir_topicos = st.sidebar.checkbox("Incluir tópicos-chave", value=True)
    incluir_insights = st.sidebar.checkbox("Incluir insights estratégicos", value=True)
    
    if st.button("Gerar Relatório"):
        if not entrevista:
            st.warning("Por favor, cole o texto da entrevista antes de gerar o relatório.")
        else:
            with st.spinner("Analisando a entrevista e gerando relatório..."):
                # Construir o prompt com base nas opções selecionadas
                prompt = f"""
                Analise a seguinte entrevista e gere um relatório profissional com base nos seguintes requisitos:
                
                - Nível de detalhe: {nivel_detalhe}
                - Incluir resumo executivo: {"Sim" if incluir_sumario else "Não"}
                - Incluir tópicos-chave: {"Sim" if incluir_topicos else "Não"}
                - Incluir insights estratégicos: {"Sim" if incluir_insights else "Não"}
                
                Texto da entrevista:
                {entrevista}
                
                Estruture o relatório da seguinte forma:
                
                1. [Só se solicitado] Resumo Executivo (máximo 1 parágrafo)
                2. Tópicos Principais Discutidos (lista com os principais assuntos)
                3. Pontos-Chave Identificados (destaque os pontos mais relevantes)
                4. [Só se solicitado] Insights Estratégicos (análise mais aprofundada)
                5. Recomendações ou Próximos Passos (sugestões baseadas na entrevista)
                
                Seja conciso mas completo, mantendo um tom profissional. Use marcadores para listas e destaque termos importantes em negrito quando apropriado.
                """
                
                # Gerar o relatório usando o Gemini
                try:
                    relatorio = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=[prompt]).text
                    
                    # Exibir o relatório
                    st.success("Relatório gerado com sucesso!")
                    st.markdown("---")
                    st.subheader("📋 Relatório da Entrevista")
                    st.markdown(relatorio)
                    
                    # Opção para baixar o relatório
                    st.download_button(
                        label="Baixar Relatório",
                        data=relatorio,
                        file_name="relatorio_entrevista.md",
                        mime="text/markdown"
                    )
                    
                except Exception as e:
                    st.error(f"Ocorreu um erro ao gerar o relatório: {str(e)}")

if __name__ == "__main__":
    main()
