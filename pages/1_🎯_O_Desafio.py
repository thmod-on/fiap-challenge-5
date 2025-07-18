# pages/1_🎯_O_Desafio.py

import streamlit as st
from utils import setup_page

# Configura a página e a barra lateral
setup_page(__file__)

# O restante do código da página permanece o mesmo...
st.markdown("# O Desafio: IA no Recrutamento e Seleção")
st.sidebar.header("O Desafio") # Opcional, para destacar a página atual

st.markdown(
    """
    A **Decision**, empresa especializada em alocação de talentos de TI (bodyshop), 
    enfrenta o desafio constante de encontrar o candidato ideal para cada vaga de forma 
    rápida e precisa.
    """
)

st.subheader("Dores Atuais do Processo")
st.markdown(
    """
    O processo atual, embora eficaz, possui pontos de atrito que podem comprometer a qualidade e agilidade da seleção:
    - **Falta de Padronização em Entrevistas:** Diferentes abordagens podem levar à perda de informações valiosas sobre os candidatos.
    - **Dificuldade em Medir Engajamento:** É um desafio identificar o real interesse e motivação do candidato durante as primeiras etapas.
    - **Agilidade vs. Qualidade:** A pressa para preencher vagas pode levar a saltar etapas cruciais, como entrevistas detalhadas, resultando em um "match" de menor qualidade.
    """
)

st.subheader("Nossa Proposta de Solução")
st.markdown(
    """
    Para solucionar essas dores, propomos um **MVP (Minimum Viable Product)** que utiliza Machine Learning 
    para otimizar a triagem inicial de candidatos.
    
    Construímos um modelo preditivo treinado com o histórico de contratações da Decision. 
    Este modelo aprendeu os padrões de perfis de candidatos que tiveram sucesso no passado, 
    analisando uma combinação de:
    
    1.  **Informações Estruturadas:** Nível de experiência, formação acadêmica, proficiência em idiomas, etc.
    2.  **Informações Não Estruturadas:** Currículos, descrições de atividades, conhecimentos técnicos e comentários de recrutadores.
    
    O resultado é uma **ferramenta de análise de compatibilidade** que calcula um "score" de aderência entre um novo candidato e uma vaga específica.
    
    > **Navegue até a página 'Análise de Compatibilidade' para ver a solução em ação!**
    """
)