# ==============================================================================
# PÁGINA STREAMLIT: ANÁLISE DE COMPATIBILIDADE E APLICAÇÃO DE VAGA
# ==============================================================================

# --- SEÇÃO 0: IMPORTS ---
import streamlit as st
import pandas as pd
import joblib
import json
import os
from datetime import datetime
from utils import setup_page


# --- Configuração da Página ---
#st.set_page_config(page_title="Análise de Vaga", page_icon="📊", layout="wide")


# Configura a página e a barra lateral
setup_page(__file__)


# --- Constante para o caminho da base de dados ---
DATABASE_PATH = "prospects_database.csv"

# ==============================================================================
# SEÇÃO 1: FUNÇÕES AUXILIARES
# ==============================================================================

@st.cache_resource
def carregar_artefatos():
    """Carrega os artefatos salvos (pipeline do modelo, lista de vagas e descrições)."""
    # (Código da função inalterado)
    try:
        pipeline = joblib.load("models/decision_model.pkl")
        with open("models/vagas_disponiveis.json", 'r', encoding='utf-8') as f:
            lista_vagas = json.load(f)
        with open("models/descricoes_vagas.json", 'r', encoding='utf-8') as f:
            descricoes = json.load(f)
        return pipeline, lista_vagas, descricoes
    except FileNotFoundError:
        st.error("Arquivos do modelo não encontrados! Por favor, execute 'treinamento_modelo.py' primeiro.")
        return None, None, None

def salvar_aplicacao(data):
    """Salva os dados da aplicação do candidato em um arquivo CSV."""
    # (Código da função inalterado)
    df_aplicacao = pd.DataFrame([data])
    if not os.path.exists(DATABASE_PATH):
        df_aplicacao.to_csv(DATABASE_PATH, index=False, sep=';', encoding='utf-8-sig')
    else:
        df_aplicacao.to_csv(DATABASE_PATH, mode='a', header=False, index=False, sep=';', encoding='utf-8-sig')

# ==============================================================================
# SEÇÃO 2: LAYOUT DA PÁGINA E INTERFACE DO USUÁRIO
# ==============================================================================

st.markdown("# Análise de Compatibilidade Candidato-Vaga")
st.sidebar.header("Análise de Vaga")
st.markdown("---")

model_pipeline, vagas_disponiveis, descricoes_vagas = carregar_artefatos()

if model_pipeline and vagas_disponiveis and descricoes_vagas:
    st.info("Bem-vindo(a)! Preencha o formulário abaixo para aplicar para uma de nossas vagas e veja sua compatibilidade instantaneamente.")
    
    with st.form(key='application_form'):
        
        # --- SEÇÃO REORGANIZADA 1: DADOS PESSOAIS ---
        st.subheader("1. Seus Dados Pessoais")
        col_pessoal1, col_pessoal2 = st.columns(2)
        with col_pessoal1:
            nome_candidato = st.text_input("Nome Completo*")
        with col_pessoal2:
            email_candidato = st.text_input("E-mail*")
        
        linkedIn_candidato = st.text_input("Perfil do LinkedIn (opcional)")        
        
        st.markdown("---")
        
        # --- SEÇÃO REORGANIZADA 2: VAGA DE INTERESSE ---
        st.subheader("2. Vaga de Interesse")
        vaga_selecionada = st.selectbox(
            'Para qual vaga você deseja aplicar?*',
            options=sorted(vagas_disponiveis)
        )
        if vaga_selecionada:
            with st.expander("📝Ver Descrição da Vaga", expanded=False):
                st.markdown(descricoes_vagas.get(vaga_selecionada, "Descrição não disponível."))

        st.markdown("---")

        # --- SEÇÃO REORGANIZADA 3: PERFIL PROFISSIONAL ---
        st.subheader("3. Seu Perfil Profissional")
        col1, col2 = st.columns(2)
        with col1:
            nivel_profissional = st.selectbox('Nível Profissional*', ['Júnior', 'Pleno', 'Sênior', 'Especialista', 'Desconhecido'], index=1)
            nivel_ingles = st.selectbox('Nível de Inglês*', ['Básico', 'Intermediário', 'Avançado', 'Fluente', 'Desconhecido'], index=1)
        with col2:
            nivel_academico = st.selectbox('Nível Acadêmico*', ['Ensino Médio', 'Técnico', 'Superior Incompleto', 'Superior Completo', 'Pós-graduação', 'Mestrado', 'Doutorado', 'Desconhecido'], index=3)
            nivel_espanhol = st.selectbox('Nível de Espanhol*', ['Básico', 'Intermediário', 'Avançado', 'Fluente', 'Não possuo', 'Desconhecido'], index=4)
        
        # --- CAMPO DE TEXTO UNIFICADO ---
        texto_candidato = st.text_area(
            "Resumo Profissional e Habilidades*",
            height=300,
            placeholder="Cole aqui as informações mais relevantes do seu currículo. Destaque suas experiências, tecnologias que domina, projetos que participou e seu objetivo profissional."
        )

        st.caption("Campos com * são obrigatórios.")
        submit_button = st.form_submit_button(label='Enviar Aplicação e Ver Compatibilidade')

    if submit_button:
        if not nome_candidato or not email_candidato or not texto_candidato:
            st.warning("Por favor, preencha todos os campos obrigatórios (*).")
        else:
            with st.spinner('Processando sua aplicação...'):
                # Monta o DataFrame para o modelo
                input_data_model = {
                    'texto_completo': f"{vaga_selecionada} {texto_candidato}", # Usa o texto unificado
                    'perfil_vaga.nivel profissional': nivel_profissional,
                    'perfil_vaga.nivel_academico': nivel_academico,
                    'perfil_vaga.nivel_ingles': nivel_ingles,
                    'formacao_e_idiomas.nivel_academico': nivel_academico,
                    'formacao_e_idiomas.nivel_ingles': nivel_ingles,
                    'formacao_e_idiomas.nivel_espanhol': nivel_espanhol,
                }
                input_df = pd.DataFrame([input_data_model])
                
                # Gera o score de compatibilidade
                probabilidade = model_pipeline.predict_proba(input_df)[0][1]
                score_compatibilidade = int(probabilidade * 100)
                
                # Prepara os dados para salvar na base (incluindo LinkedIn)
                application_data_to_save = {
                    "data_aplicacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "nome_candidato": nome_candidato,
                    "email_candidato": email_candidato,
                    "linkedin_candidato": linkedIn_candidato, # <-- CAMPO NOVO AQUI
                    "vaga_aplicada": vaga_selecionada,
                    "score_compatibilidade": score_compatibilidade,
                    "nivel_profissional": nivel_profissional,
                    "nivel_academico": nivel_academico,
                    "nivel_ingles": nivel_ingles,
                    "nivel_espanhol": nivel_espanhol,
                    "resumo_cv": texto_candidato, # Usa o texto unificado
                }
                
                # Salva os dados no arquivo CSV
                salvar_aplicacao(application_data_to_save)
                
                st.success(f"Obrigado, {nome_candidato}! Sua aplicação para a vaga '{vaga_selecionada}' foi recebida com sucesso.")
                st.metric(label="Seu percentual de Compatibilidade com a Vaga é:", value=f"{score_compatibilidade}%")
                st.progress(score_compatibilidade)
                st.markdown("Boa sorte no processo! 🍀 Estamos na torcida por você.🎊")
                st.balloons()