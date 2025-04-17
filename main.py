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
                ###EXEMPLO DE ENTREVISTA###

January I - Accusations of Forced Labor in the Construction of the BYD Plant in Brazil

Who made the report?	1

State Government's Perception of the Case	3

Federal Government’s Perception of the Case	4

Institutions Responsible for Investigations	7

Possible Legal Consequences for BYD and Jinjiang	8

Relationship Between BYD and Jinjiang	9

Who made the report?
The reports about the working conditions at Jinjiang Construction Brazil did not come from European or American automakers. 
According to a source from the state government of Bahia, which is directly involved with BYD, the Bahia Labor Public Prosecutor's Office (MPT-BA) started an investigation into the construction of the plant following complaints from residents of the city of Camaçari, where the plant is located. 
This source pointed out that the BYD plant is situated near the city center, in front of two important avenues, and residents frequently pass by the construction site.
Additionally, the source mentioned some dissatisfaction in the city regarding the hiring of Chinese workers at the plant, which might have contributed to the complaints.
The source said that both the state government and the Camaçari city hall had received complaints from residents about BYD’s hiring practices and those of its subcontractors; “various positions require English, technical training in specific areas, and the local workforce doesn’t have these qualifications. So, even in positions where BYD and its subcontractors hire Brazilians, these positions often go to people from Salvador (the state capital).” 
The source also stated that the state government is promoting professional training courses for the city’s residents to prepare them for technical roles at the factory.
It was reported that even during the construction phase of the plant, most of the workers at BYD and its subcontractors are Brazilian. Once production begins, the state government expects that 80% of the workforce will be Brazilian. “The Chinese workers at BYD will all be in technical roles or people who have been in Brazil for a while and will work under the CLT regime (CLT is the labor regime that governs employment relations in Brazil),” said the source, adding that this is why the state government believes “the population of the state and Camaçari will be very satisfied.”

State Government's Perception of the Case
The Bahia government source emphasized that there is “very good communication between the state government and BYD.” The source noted that Bahia’s governor, Jerônimo Rodrigues, believes BYD responded very quickly to the accusations of forced labor, and that the state government’s main concern now is the project’s timeline.
BYD’s plant is one of the major job-generating projects for Bahia, and the governor highly values it because it generates “jobs and revenue for the state.” 
The source was clear that the state’s feeling regarding the case is that “BYD is committed to making the necessary adjustments, and now it’s time to move forward and start production.”
The state source stated that before the issue, the plan was for production to begin in March. BYD is now studying how much the schedule will be delayed, but production is expected to begin sometime in the second half of the year.
“The state government is closely monitoring this (the schedule changes),” the source said, adding that the state’s interest is to start the work as soon as possible.
When asked if there was any friction between the state government and BYD over this case, the source explained that “there was concern from the state government about the progress of the work and the case itself, but because BYD responded quickly and severed ties with Jinjiang, these concerns were resolved. From an institutional perspective, the relationship remained very good.”
Asked about the fine’s amount, the source said that neither the Labor Public Prosecutor's Office of Bahia (MPT-BA) nor BYD have discussed this with the state government, and that based on conversations with company representatives, the main concern is not the financial aspect, but the potential reputational damage to BYD due to the fine.
Federal Government’s Perception of the Case
When asked about the Lula government’s view of the Jinjiang case, one of the key international relations advisors for the Workers' Party (PT) and a China expert reported that “during Xi Jinping's visit last year, it was said that China and Brazil are in the best moment of their relationship, it is a period of closer ties. In any relationship, when there’s a closer connection, some friction arises, and you need to have conversations to understand each other better. This problem with Jinjiang is largely due to cultural differences, and we saw a genuine interest from BYD in better understanding how things work here.”
According to the PT advisor, “Chinese companies coming to Brazil face a perception of risk problems. Many times because they have the support of the federal government and don’t understand Brazil’s political system and legislation, they think that with strong federal backing, they have great institutional security. In China, if you’re friends with Xi Jinping, he can make a call and resolve your issue, and they think it works the same way here.”
“Here [in Brazil], there is independence of the institutions. The Chinese have a hard time understanding that the Brazilian political and decision-making system is very decentralized. Lula cannot call the Public Prosecutor’s Office and say ‘look, the BYD factory is very important for Bahia, don’t create problems for them, or they might decide to invest less,’ that doesn’t happen here,” said the advisor.
The advisor also pointed out that the PT leadership believes this case has helped Chinese companies develop a better understanding of how the Brazilian political system functions. “There are rules that need to be followed, being friends with Lula won’t solve the problems.” 
The advisor emphasized that it’s common for Chinese companies in Brazil to disregard local laws, thinking they can resolve issues through Guanxi, even when repeatedly warned that this isn’t how things work in Brazil. 
Apart from these cultural and institutional differences, the advisor noted that despite the Brazilian government’s strong interest in attracting Chinese investment, there are criticisms within the government about the lack of multiplier effects from Chinese investments. There is a widespread criticism in the Brazilian public and private sector that when China invests abroad, the Chinese bring in their own raw materials and labor, which doesn’t create many jobs or generate significant revenue in the countries where the investments are made.
The advisor reported that for the BYD plant specifically, a significant presence of Brazilian workers was negotiated. “President Lula and Minister Rui Costa (former governor of Bahia, who negotiated the BYD factory in Camaçari) are pleased with the number of jobs the BYD factory will create in Bahia and the percentage of Brazilian workers once it’s fully operational, but it looks bad for a project that was announced as ‘job creation for Brazilians’ to be known for importing Chinese labor under conditions similar to slavery.”

Institutions Responsible for Investigations
The main institution responsible for the investigation is the Bahia Labor Public Prosecutor’s Office, as the plant is being constructed in that state.
It is important to note that the Brazilian judiciary is extremely powerful, and its representatives are often referred to as “lords of power.” 
The Labor Public Prosecutor’s Office has seen a decline in power since the labor reform of 2017, which reduced its authority. The Labor Public Prosecutor's Office of Bahia (MPT-BA) views this investigation as an opportunity to regain prominence.
Prosecutor Bernardo Guimarães is leading the investigation.
According to the head of Guimarães’ office, the investigation is ongoing, and various government institutions are actively monitoring it, including the Labor Public Prosecutor's Office of Bahia (MPT-BA), the Ministry of Labor and Employment (MTE), and the Federal Police (PF). 
The Labor Public Prosecutor's Office of Bahia (MPT-BA) and the Federal Police (PF) have a high degree of autonomy from both the federal and state governments. 
The Federal Police (PF) has already investigated and even arrested President Lula in 2018. It’s impossible for Lula to call these institutions and request that they adopt a more favorable stance toward BYD or Jinjiang.

Possible Legal Consequences for BYD and Jinjiang
In communication with a senior official from the Ministry of Labor and Employment (MTE) regarding the case, she stated that “the investigation could conclude by the fifth month of its execution,” meaning it should wrap up by the end of April at the latest. 
The official said that Jinjiang will likely be included in the “List of Employers Who Have Subjugated Workers to Conditions Similar to Slavery,” which is published on the Ministry’s official website. This list, commonly known as the “dirty list,” is not a penalty or fine but serves to publicly draw attention to companies that have been investigated and judged by labor inspection authorities for using forced labor. 
BYD will not be included on this list, as it was the contracting company. 
However, being on this list harms a company’s public reputation and leads to closer scrutiny by labor inspection authorities.
Both Jinjiang and BYD will be fined. The fine amounts are still being determined, and both the head of the prosecutor’s office and the Ministry of Labor and Employment (MTE) official stated they could not comment on the specific amount.

Relationship Between BYD and Jinjiang
BYD's CEO for the Americas, Stella Lee, warned BYD’s global headquarters in China that hiring Jinjiang would bring problems for BYD in Brazil due to labor issues. She did everything she could to prevent Jinjiang from coming to Brazil. 
It’s important to note that any executive with experience in the Brazilian market would know that hiring a company like Jinjiang would cause issues with local legislation. 
The person responsible for civil engineering at BYD in China is the nephew of the owner, and despite Lee’s opposition, he decided to hire Jinjiang anyway.
Because Lee strongly opposed the hiring of Jinjiang, she faced no consequences within BYD for the actions of the subcontractor.

                ###FIM DE EXEMPLO###
                
                Siga o exemplo à risca.

                Analise a seguinte entrevista e gere um relatório profissional com base nos seguintes requisitos:
                
                - Nível de detalhe: {nivel_detalhe}
                - Incluir resumo executivo: {"Sim" if incluir_sumario else "Não"}
                - Incluir tópicos-chave: {"Sim" if incluir_topicos else "Não"}
                - Incluir insights estratégicos: {"Sim" if incluir_insights else "Não"}
                
                Texto da entrevista:
                {entrevista}
                
                Estruture o relatório da seguinte forma:
                

                1. Escreva em inglês e siga o exemplo à risca em termos de formato e forma de escrita.

                
                
                Seja conciso mas completo, mantendo um tom profissional. Use marcadores para listas e destaque termos importantes em negrito quando apropriado.
                Escreva em inglês bem completo.


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
