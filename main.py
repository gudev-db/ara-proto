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

                
                                     Based on the contents of an interview, produce a structured and analytical report. The report should be organized into numbered sections, each addressing a central theme or topic discussed during the interview. The style should mirror journalistic-investigative reporting, as follows:
                        Structure:
                        
                            Origin of the Case or Central Issue – Explain how the issue came to light, who is involved, and what circumstances or context are relevant. Mention any initial complaints, investigations, or triggering events.
                        
                            Perspectives of Key Stakeholders – Present and contrast how various individuals, institutions, or groups perceive the case (e.g., local government, federal government, private sector, regulators, civil society).
                        
                            Actions Taken and Institutional Responses – Describe measures underway, investigations launched, or institutional involvement. Highlight the roles and independence of relevant bodies.
                        
                            Potential Legal, Political, or Reputational Outcomes – Discuss likely or possible consequences based on the interview, including changes in public image, legal risk, policy impact, or shifts in public opinion.
                        
                            Relationships Between Involved Parties – Analyze how actors are connected (e.g., contractual, hierarchical, informal), and how those relationships affect decision-making or accountability.

                            Make sure every party (be it company, country, entity, person in general) mentioned in the interview is present in the report.

                            Don't be generic. You are here to provide insight into the information brought about from the interview.

                            You are thorough and your report will compile every single information within the provided interview
                        
                        Language & Style Guidelines:
                        
                            Maintain a neutral, objective, and analytical tone throughout the report.
                        
                            Where appropriate, include direct quotes from the interview, placing them in quotation marks and attributing them to their respective sources (if named or described). And make sure those direct quotes are translated into English.
                        
                            Use precise, formal language suitable for investigative or institutional reporting.
                        
                            Introduce sources clearly (e.g., “a senior official from the Ministry of Labor stated...”) and avoid assuming facts not supported by the interview.
                        
                            Emphasize institutional, legal, and political context where relevant (e.g., autonomy of authorities, legal frameworks, cultural norms).
                        
                            If the interview reveals contrasting viewpoints, present both fairly without editorializing.
                        
                            Follow chronological logic when necessary, helping the reader understand how events unfolded and why.

                            Generate at least 2500 tokens in your output.

                            


                            Make use of direct citations (translated to english and naming who said it) to strengthen points when deemed appropriate. You are an expert redator so you know when it will be appropriate. You need to make at least a few direct citations in order to strengthen your point

                            
                        The goal is to turn the raw interview content into a coherent, well-structured, and contextualized report that provides clarity, insight, and a critical overview of the situation.


                Interview body:
                {entrevista}
                
               


                """
                
                # Gerar o relatório usando o Gemini
                try:
                    relatorio = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=[prompt]).text

                    relatorio2 = client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=[f'''based on the report
                        ##REPORT##
                        
                        {relatorio}
                        
                        ##END REPORT##
                        
                        - draw valuable insights not initially obvious. You are an expert at reading between the lines''']).text
                    
                    # Exibir o relatório
                    st.success("Relatório gerado com sucesso!")
                    st.markdown("---")
                    st.subheader("📋 Relatório da Entrevista")
                    st.markdown(relatorio)
                    st.subheader("📋 Insights Estratégicos")
                    st.markdown(relatorio2)
                    
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
